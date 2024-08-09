import cohere, os, time, requests
from .base_source_code_summarizer import BaseSourceCodeSummarizer


class CohereSourceCodeSummarizer(BaseSourceCodeSummarizer):
    _client = None

    @classmethod
    def initialize(cls) -> None:
        if os.getenv("COHERE_API_KEY") is None:
            return

        cls._client = cohere.Client(os.getenv("COHERE_API_KEY"))

    @classmethod
    def summarize_source_code(cls, source_code: str) -> str:
        if cls._client is None:
            return "placeholder for source code summary"

        url = "https://api.cohere.com/v1/chat"
        headers = {
            "Authorization": f'Bearer {os.getenv("COHERE_API_KEY")}',
            "Content-Type": "application/json",
        }
        data = {
            "message": f"In exactly 1 sentence, semantically summarize the following source code. Do not include any additional phrases or polite expressions:\n{source_code}",
            "max_tokens": 50,
        }

        max_retries = 5
        retry_delay = 2  # Initial delay in seconds

        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                return response.json()["text"].strip()
            
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    if attempt < max_retries - 1:
                        print(f"Rate limit exceeded. Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                    else:
                        raise Exception("Max retries reached. Aborting.") from e
                else:
                    raise e
