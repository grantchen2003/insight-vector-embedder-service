from .base_database import BaseDatabase


class PostgreSql(BaseDatabase):
    # TODO
    def connect(self) -> None:
        pass

    # TODO
    def close(self) -> None:
        pass

    # TODO
    def save_file_component_vector_embeddings(
        self, file_component_vector_embeddings: list[dict]
    ) -> list[int]:
        return [1, 2, 3]
