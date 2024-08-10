import json, openai, os, time, uuid
from concurrent.futures import ThreadPoolExecutor

from .base_source_code_summarizer import BaseSourceCodeSummarizer
from vector_embedder_service import utils


class OpenAiSourceCodeSummarizer(BaseSourceCodeSummarizer):
    _MAX_NUM_REQUESTS_PER_BATCH = 50_000
    _MAX_BYTES_PER_BATCH_FILE = 100_000_000
    _client = None

    @classmethod
    def initialize(cls) -> None:
        if os.getenv("OPEN_AI_API_KEY") is None:
            return

        cls._client = openai.OpenAI(api_key=os.environ.get("OPEN_AI_API_KEY"))

    @classmethod
    def summarize_source_code_list(cls, source_code_list: list[str]) -> list[str]:
        request_batches = cls._get_request_batches(source_code_list)

        with ThreadPoolExecutor() as executor:
            return utils.flatten_list(
                list(
                    executor.map(cls._summarize_source_code_list_batch, request_batches)
                )
            )

    @classmethod
    def _get_request_batches(cls, source_code_list: list[str]) -> list[list[str]]:
        request_batches = []

        request_batch = []
        file_size_bytes = 0

        for source_code in source_code_list:
            request = {
                "custom_id": str(len(request_batch)),
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

            request_size_bytes = len(json.dumps(request).encode("utf-8")) + 1

            if (
                len(request_batch) + 1 > cls._MAX_NUM_REQUESTS_PER_BATCH
                or file_size_bytes + request_size_bytes > cls._MAX_BYTES_PER_BATCH_FILE
            ):
                request_batches.append(request_batch)
                request_batch = []
                file_size_bytes = 0

            request_batch.append(request)
            file_size_bytes += request_size_bytes

        if request_batch:
            request_batches.append(request_batch)

        return request_batches

    @classmethod
    def _upload_batch_input_file(cls, request_batch: list[str]):
        directory = "openai_batch_temp"
        file_path = os.path.join(directory, f"{uuid.uuid4()}.jsonl")

        os.makedirs(directory, exist_ok=True)

        with open(file_path, "w") as file:
            file.write(
                "\n".join(json.dumps(request) for request in request_batch) + "\n"
            )

        with open(file_path, "rb") as file:
            batch_input_file = cls._client.files.create(file=file, purpose="batch")

        os.remove(file_path)

        return batch_input_file

    @classmethod
    def _create_batch(cls, batch_input_file):
        while True:
            batch = cls._client.batches.create(
                input_file_id=batch_input_file.id,
                endpoint="/v1/chat/completions",
                completion_window="24h",
            )

            while True:
                batch = cls._client.batches.retrieve(batch.id)

                if batch.status == "completed":
                    return batch

                elif batch.status == "failed":
                    time.sleep(5)
                    break

                time.sleep(1)

    @classmethod
    def _extract_code_summaries_from_response(
        cls, request_batch, file_response
    ) -> list[str]:
        source_code_summaries = [""] * len(request_batch)

        for response in file_response.text.strip().split("\n"):
            response = json.loads(response)
            source_code_summaries[int(response["custom_id"])] = response["response"][
                "body"
            ]["choices"][0]["message"]["content"]

        return source_code_summaries

    @classmethod
    def _summarize_source_code_list_batch(cls, request_batch: list[str]) -> list[str]:
        batch_input_file = cls._upload_batch_input_file(request_batch)

        batch = cls._create_batch(batch_input_file)

        file_response = cls._client.files.content(batch.output_file_id)

        return cls._extract_code_summaries_from_response(request_batch, file_response)

    # @classmethod
    # def _summarize_source_code(cls, source_code: str) -> str:
    #     if cls._client is None:
    #         return "placeholder for source code summary"

    #     response = cls._client.chat.completions.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {
    #                 "role": "user",
    #                 "content": "Semantically summarize this source code into 1 sentence: "
    #                 + source_code,
    #             }
    #         ],
    #     )

    #     return response.choices[0].message.content.strip("\n").strip()
