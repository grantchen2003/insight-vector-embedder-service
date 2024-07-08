from abc import ABC, abstractmethod


class BaseDatabase(ABC):
    @abstractmethod
    def connect(cls) -> None:
        pass

    @abstractmethod
    def close(cls) -> None:
        pass

    @abstractmethod
    def save_file_component_vector_embeddings(
        cls, file_component_vector_embeddings: list[dict]
    ) -> list[int]:
        pass

    @abstractmethod
    def get_similar_file_component_ids(
        cls, repository_id: str, vector_embedding: list[float], limit: int
    ) -> list[int]:
        pass

    @abstractmethod
    def delete_file_component_vector_embeddings_by_repository_id(cls, repository_id: str) -> None:
        pass