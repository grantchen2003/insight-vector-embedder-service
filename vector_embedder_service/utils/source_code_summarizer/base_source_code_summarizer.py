from abc import ABC, abstractmethod


class BaseSourceCodeSummarizer(ABC):
    @abstractmethod
    def initialize(cls) -> None:
        pass
    
    @abstractmethod
    def summarize_source_code_list(cls, source_code_list: list[str]) -> list[str]:
        pass