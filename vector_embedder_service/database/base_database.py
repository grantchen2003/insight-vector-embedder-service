from abc import ABC, abstractmethod


class BaseDatabase(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def save_file_component_vector_embeddings(
        self, file_component_vector_embeddings: list[dict]
    ) -> list[int]:
        pass
