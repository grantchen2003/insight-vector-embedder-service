from vector_embedder_service.protobufs import (
    vector_embedder_service_pb2,
    vector_embedder_service_pb2_grpc,
)

from vector_embedder_service import database, utils
from vector_embedder_service.services import file_components_service


class VectorEmbedderService(vector_embedder_service_pb2_grpc.VectorEmbedderService):
    def CreateFileComponentVectorEmbeddings(self, request, _):
        print("received CreateFileComponentVectorEmbeddings request")

        file_components = file_components_service.get_file_components(
            request.file_component_ids
        )

        file_component_vector_embeddings = [
            {
                "file_component_id": file_component["id"],
                "user_id": file_component["user_id"],
                "vector_embedding": utils.CodeBert.vector_embed(
                    file_component["content"]
                ),
            }
            for file_component in file_components
        ]

        db = database.get_singleton_instance()

        file_component_vector_embedding_ids = db.save_file_component_vector_embeddings(
            file_component_vector_embeddings
        )

        return vector_embedder_service_pb2.CreateFileComponentVectorEmbeddingsResponse(
            file_component_vector_embedding_ids=file_component_vector_embedding_ids
        )

    def GetSimilarFileComponentIds(self, request, _):
        print("received GetSimilarFileComponentIds request")

        query_vector_embedding = utils.CodeBert.vector_embed(request.query)

        db = database.get_singleton_instance()

        file_component_ids = db.get_similar_file_component_ids(
            request.user_id, query_vector_embedding, request.limit
        )

        return vector_embedder_service_pb2.GetSimilarFileComponentIdsResponse(
            file_component_ids=file_component_ids
        )
