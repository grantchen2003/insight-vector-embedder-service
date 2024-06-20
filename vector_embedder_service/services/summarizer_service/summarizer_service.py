
from typing import TypedDict


class FileComponentSummary(TypedDict):
    id: int
    file_component_id: int
    summary: str

def get_file_component_summaries(file_component_ids: list[int]) -> list[FileComponentSummary]:
    return []