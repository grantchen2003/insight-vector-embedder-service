import logging
from concurrent.futures import ThreadPoolExecutor
from google.protobuf import empty_pb2

from vector_embedder_service.protobufs import (
    vector_embedder_service_pb2,
    vector_embedder_service_pb2_grpc,
)
from vector_embedder_service import database
from vector_embedder_service.services import file_components_service
from vector_embedder_service.utils import SourceCodeSummarizer, UniversalSentenceEncoder


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

class VectorEmbedderService(vector_embedder_service_pb2_grpc.VectorEmbedderService):
    def CreateFileComponentVectorEmbeddings(self, request, _):
        def get_file_component_vector_embedding(file_component):
            content_summary = SourceCodeSummarizer.summarize_source_code(
                file_component["content"]
            )

            content_vector_embedding = UniversalSentenceEncoder.vector_embed_sentence(
                content_summary
            )

            return {
                "file_component_id": file_component["id"],
                "repository_id": file_component["repository_id"],
                "content_summary": content_summary,
                "vector_embedding": content_vector_embedding,
            }

        logger.info("received CreateFileComponentVectorEmbeddings request")

        file_components = file_components_service.get_file_components(
            request.file_component_ids
        )

        with ThreadPoolExecutor() as executor:
            file_component_vector_embeddings = list(
                executor.map(get_file_component_vector_embedding, file_components)
            )

        db = database.get_singleton_instance()

        file_component_vector_embedding_ids = db.save_file_component_vector_embeddings(
            file_component_vector_embeddings
        )

        return vector_embedder_service_pb2.CreateFileComponentVectorEmbeddingsResponse(
            file_component_vector_embedding_ids=file_component_vector_embedding_ids
        )

    def GetSimilarFileComponentIds(self, request, _):
        logger.info("received GetSimilarFileComponentIds request")

        query_vector_embedding = UniversalSentenceEncoder.vector_embed_sentence(
            request.query
        )

        db = database.get_singleton_instance()

        file_component_ids = db.get_similar_file_component_ids(
            request.repository_id, query_vector_embedding, request.limit
        )

        return vector_embedder_service_pb2.GetSimilarFileComponentIdsResponse(
            file_component_ids=file_component_ids
        )

    def DeleteFileComponentVectorEmbeddingsByRepositoryId(self, request, _):
        logger.info("received DeleteFileComponentVectorEmbeddingsByRepositoryId request")

        db = database.get_singleton_instance()

        db.delete_file_component_vector_embeddings_by_repository_id(
            request.repository_id
        )

        return empty_pb2.Empty()

    def DeleteFileComponentVectorEmbeddingsByRepositoryIdAndFileComponentIds(
        self, request, _
    ):
        logger.info(
            "received DeleteFileComponentVectorEmbeddingsByRepositoryIdAndFileComponentIds request"
        )

        db = database.get_singleton_instance()

        db.delete_file_component_vector_embeddings_by_repository_id_and_file_component_ids(
            request.repository_id, list(request.file_component_ids)
        )

        return empty_pb2.Empty()
