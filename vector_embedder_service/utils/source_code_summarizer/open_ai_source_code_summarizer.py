import openai, os
from .base_source_code_summarizer import BaseSourceCodeSummarizer


class OpenAi(BaseSourceCodeSummarizer):
    _client = None

    @classmethod
    def initialize(cls) -> None:
        if os.getenv("OPEN_AI_API_KEY") is None:
            return

        cls._client = openai.OpenAI(api_key=os.environ.get("OPEN_AI_API_KEY"))

    @classmethod
    def summarize_source_code(cls, source_code: str) -> str:
        if cls._client is None:
            return "placeholder for source code summary"

        response = cls._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": "Semantically summarize this source code into 1 sentence: "
                    + source_code,
                }
            ],
        )

        return response.choices[0].message.content.strip("\n").strip()
