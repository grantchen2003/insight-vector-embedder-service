from abc import ABC, abstractmethod


class BaseSourceCodeSummarizer(ABC):
    @abstractmethod
    def initialize(cls) -> None:
        pass
    
    @abstractmethod
    def summarize_source_code(cls, source_code: str) -> str:
        pass