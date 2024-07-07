import os

from openai import OpenAI


class SourceCodeSummarizer:
    _client = None

    @classmethod
    def initialize(cls) -> None:
        cls._client = OpenAI(api_key=os.environ.get("OPEN_AI_API_KEY"))

    @classmethod
    def summarize_source_code(cls, source_code: str) -> str:
        return "hi"
        # response = cls._client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {
        #             "role": "user",
        #             "content": "Semantically summarize this source code into 1 sentence: "
        #             + source_code,
        #         }
        #     ],
        # )

        # return response.choices[0].message.content.strip("\n").strip()
