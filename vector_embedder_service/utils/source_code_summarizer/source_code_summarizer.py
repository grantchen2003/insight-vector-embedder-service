from typing import Optional

from .base_source_code_summarizer import BaseSourceCodeSummarizer
from .open_ai_source_code_summarizer import OpenAiSourceCodeSummarizer


singleton_instance: Optional[BaseSourceCodeSummarizer] = None


def get_singleton_instance() -> BaseSourceCodeSummarizer:
    global singleton_instance
    if singleton_instance is None:
        singleton_instance = OpenAiSourceCodeSummarizer()

    return singleton_instance