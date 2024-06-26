import chromadb, os


class ChromaDb:
    _client = None
    _conn = None

    @classmethod
    def connect(cls) -> None:
        cls._client = chromadb.PersistentClient(os.environ.get("CHROMADB_PATH"))
        cls._collection = cls._client.get_or_create_collection(
            name="file_component_vector_embeddings"
        )

    def close(self) -> None:
        pass

    @classmethod
    def save_file_component_vector_embeddings(
        cls, file_component_vector_embeddings: list[dict]
    ) -> list[int]:
        ids = []
        embeddings = []
        metadatas = []
        for file_component_vector_embedding in file_component_vector_embeddings:
            ids.append(f"id{str(file_component_vector_embedding["file_component_id"])}")
            embeddings.append(file_component_vector_embedding["vector_embedding"])
            metadatas.append(
                {
                    "user_id": file_component_vector_embedding["user_id"],
                    "file_component_id": file_component_vector_embedding[
                        "file_component_id"
                    ],
                }
            )

        cls._collection.add(embeddings=embeddings, metadatas=metadatas, ids=ids)
        
        return ids

    @classmethod
    def get_similar_file_component_ids(cls, user_id: str, vector_embedding: list[float], limit: int) -> list[int]:
        results = cls._collection.query(
            query_embeddings=[vector_embedding],
            n_results=limit,
            where={"user_id": user_id}
        )
        
        return [result["file_component_id"] for result in results["metadatas"][0]]