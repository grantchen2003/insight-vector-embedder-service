from typing import Optional

from .base_source_code_summarizer import BaseSourceCodeSummarizer
from .cohere_source_code_summarizer import CohereSourceCodeSummarizer


singleton_instance: Optional[BaseSourceCodeSummarizer] = None


def get_singleton_instance() -> BaseSourceCodeSummarizer:
    global singleton_instance
    if singleton_instance is None:
        singleton_instance = CohereSourceCodeSummarizer()

    return singleton_instance