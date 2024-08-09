import json, openai, os, time, uuid
from concurrent.futures import ThreadPoolExecutor

from .base_source_code_summarizer import BaseSourceCodeSummarizer
from vector_embedder_service import utils
from vector_embedder_service.utils.batchifier import Batchifier


class OpenAiSourceCodeSummarizer(BaseSourceCodeSummarizer):
    _client = None

    @classmethod
    def initialize(cls) -> None:
        if os.getenv("OPEN_AI_API_KEY") is None:
            return

        cls._client = openai.OpenAI(api_key=os.environ.get("OPEN_AI_API_KEY"))

    @classmethod
    def summarize_source_code_list(cls, source_code_list: list[str]) -> list[str]:
        '''
        Bottom of https://platform.openai.com/docs/guides/batch/rate-limits
        
        middle of https://platform.openai.com/docs/guides/rate-limits:
        Batch API queue limits are calculated based on the total number of input tokens queued for a given model. 
        Tokens from pending batch jobs are counted against your queue limit. 
        Once a batch job is completed, its tokens are no longer counted against that model's limit.
        '''
        source_code_batches = Batchifier.batchify(source_code_list, 100)

        with ThreadPoolExecutor() as executor:
            return utils.flatten_list(
                list(
                    executor.map(
                        cls._summarize_source_code_list_batch, source_code_batches
                    )
                )
            )

    @classmethod
    def _summarize_source_code_list_batch(
        cls, source_code_list: list[str]
    ) -> list[str]:
        requests = [
            {
                "custom_id": str(i),
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-3.5-turbo-0125",
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Semantically summarize this source code into 1 sentence: '{source_code}'",
                        }
                    ],
                },
            }
            for i, source_code in enumerate(source_code_list)
        ]
        
        directory = 'openai_batch_temp'
        file_path = os.path.join(directory, f'{uuid.uuid4()}.jsonl')
        
        os.makedirs(directory, exist_ok=True)

        with open(file_path, "w") as file:
            for request in requests:
                file.write(json.dumps(request) + "\n")

        with open(file_path, "rb") as file:
            batch_input_file = cls._client.files.create(
                file=file, purpose="batch"
            )
            
        os.remove(file_path)

        batch_input_file_id = batch_input_file.id

        batch = cls._client.batches.create(
            input_file_id=batch_input_file_id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
        )

        while True:
            batch = cls._client.batches.retrieve(batch.id)
            if batch.status == "completed":
                break
            time.sleep(1)

        file_response = cls._client.files.content(batch.output_file_id)

        source_code_summaries = [""] * len(source_code_list)
        for response in file_response.text.strip().split("\n"):
            response = json.loads(response)
            source_code_summaries[int(response["custom_id"])] = response["response"][
                "body"
            ]["choices"][0]["message"]["content"]
        
        return source_code_summaries

    @classmethod
    def _summarize_source_code(cls, source_code: str) -> str:
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
