import datetime
from google.protobuf import empty_pb2

from vector_embedder_service.protobufs import (
    vector_embedder_service_pb2,
    vector_embedder_service_pb2_grpc,
)
from vector_embedder_service import database
from vector_embedder_service.services import file_components_service
from vector_embedder_service.utils import (
    source_code_summarizer,
    UniversalSentenceEncoder,
)


def print_with_timestamp(message):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y/%m/%d %H:%M:%S")
    print(f"{timestamp} {message}")


class VectorEmbedderService(vector_embedder_service_pb2_grpc.VectorEmbedderService):
    def CreateFileComponentVectorEmbeddings(self, request, _):
        print_with_timestamp("received CreateFileComponentVectorEmbeddings request")

        file_components = file_components_service.get_file_components(
            request.file_component_ids
        )

        content_summaries = (
            source_code_summarizer.get_singleton_instance().summarize_source_code_list(
                [file_component["content"] for file_component in file_components]
            )
        )

        content_vector_embeddings = [
            UniversalSentenceEncoder.vector_embed_sentence(content_summary)
            for content_summary in content_summaries
        ]

        file_component_vector_embeddings = [
            {
                "file_component_id": file_component["id"],
                "repository_id": file_component["repository_id"],
                "content_summary": content_summary,
                "vector_embedding": content_vector_embedding,
            }
            for file_component, content_summary, content_vector_embedding in zip(
                file_components, content_summaries, content_vector_embeddings
            )
        ]

        db = database.get_singleton_instance()

        file_component_vector_embedding_ids = db.save_file_component_vector_embeddings(
            file_component_vector_embeddings
        )

        return vector_embedder_service_pb2.CreateFileComponentVectorEmbeddingsResponse(
            file_component_vector_embedding_ids=file_component_vector_embedding_ids
        )

    def GetSimilarFileComponentIds(self, request, _):
        print_with_timestamp("received GetSimilarFileComponentIds request")

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
        print_with_timestamp("received DeleteFileComponentVectorEmbeddingsByRepositoryId request")

        db = database.get_singleton_instance()

        db.delete_file_component_vector_embeddings_by_repository_id(
            request.repository_id
        )

        return empty_pb2.Empty()

    def DeleteFileComponentVectorEmbeddingsByRepositoryIdAndFileComponentIds(
        self, request, _
    ):
        print_with_timestamp(
            "received DeleteFileComponentVectorEmbeddingsByRepositoryIdAndFileComponentIds request"
        )

        db = database.get_singleton_instance()

        db.delete_file_component_vector_embeddings_by_repository_id_and_file_component_ids(
            request.repository_id, list(request.file_component_ids)
        )

        return empty_pb2.Empty()
