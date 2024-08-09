import cohere, os, time
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

        while True:
            try:
                response = cls._client.generate(
                    model="command",
                    prompt="Semantically summarize this source code into 1 sentence: "
                    + source_code,
                )
                return response.generations[0].text.strip()

            except cohere.errors.TooManyRequestsError:
                pass
