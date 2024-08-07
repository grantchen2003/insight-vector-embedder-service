import chromadb, os

from vector_embedder_service.utils import Batchifier

class ChromaDb:
    _client = None
    _conn = None
    _MAX_NUM_ITEMS_PER_WRITE = 5461

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
        if not file_component_vector_embeddings:
            return []
        
        ids = []
        embeddings = []
        metadatas = []
        for file_component_vector_embedding in file_component_vector_embeddings:
            ids.append(f"id{str(file_component_vector_embedding["file_component_id"])}")
            embeddings.append(file_component_vector_embedding["vector_embedding"])
            metadatas.append(
                {
                    "repository_id": file_component_vector_embedding["repository_id"],
                    "file_component_id": file_component_vector_embedding[
                        "file_component_id"
                    ],
                    "content_summary": file_component_vector_embedding["content_summary"]
                }
            )
            
        embeddings_batches = Batchifier.batchify(embeddings, cls._MAX_NUM_ITEMS_PER_WRITE)
        metadatas_batches = Batchifier.batchify(metadatas, cls._MAX_NUM_ITEMS_PER_WRITE)
        ids_batches = Batchifier.batchify(ids, cls._MAX_NUM_ITEMS_PER_WRITE)
        
        for embeddings, metadatas, ids in zip(embeddings_batches, metadatas_batches, ids_batches):
            cls._collection.add(embeddings=embeddings, metadatas=metadatas, ids=ids)
        
        return ids

    @classmethod
    def get_similar_file_component_ids(cls, repository_id: str, vector_embedding: list[float], limit: int) -> list[int]:
        results = cls._collection.query(
            query_embeddings=[vector_embedding],
            n_results=limit,
            where={"repository_id": repository_id}
        )
        
        return [result["file_component_id"] for result in results["metadatas"][0]][:limit]
    
    @classmethod
    def delete_file_component_vector_embeddings_by_repository_id(cls, repository_id: str) -> None:
        embedding_ids = cls._collection.get(where = {"repository_id": repository_id})["ids"]
        
        embedding_id_batches = Batchifier.batchify(embedding_ids, cls._MAX_NUM_ITEMS_PER_WRITE)
        
        for embedding_id_batch in embedding_id_batches:
            cls._collection.delete(ids=embedding_id_batch)
        
    @classmethod
    def delete_file_component_vector_embeddings_by_repository_id_and_file_component_ids(cls, repository_id: str, file_component_ids: list[int]) -> None:
        if not file_component_ids:
            return
        
        embedding_ids = cls._collection.get(where={
            "$and": [
                {"repository_id": repository_id},
                {"file_component_id": {"$in": file_component_ids}}
            ]
        })["ids"]

        embedding_id_batches = Batchifier.batchify(embedding_ids, cls._MAX_NUM_ITEMS_PER_WRITE)
        
        for embedding_id_batch in embedding_id_batches:
            cls._collection.delete(ids=embedding_id_batch)
