from vector_embedder_service.protobufs import (
    vector_embedder_service_pb2,
    vector_embedder_service_pb2_grpc,
)

from vector_embedder_service import utils

from vector_embedder_service.services import summarizer_service


class VectorEmbedderService(vector_embedder_service_pb2_grpc.VectorEmbedderService):
    def BatchVectorEmbedFileComponents(self, request, _):
        print("received BatchVectorEmbedFileComponents request")

        file_component_summaries = summarizer_service.get_file_component_summaries(
            request.file_component_ids
        )

        file_component_vector_embeddings = []

        for file_component_summary in file_component_summaries:
            vector_embedding = utils.Word2VecEmbedder.vector_embed_sentence(
                file_component_summary.summary
            )
            file_component_vector_embeddings.append(
                {
                    "file_component_id": file_component_summary["id"],
                    "vector_embedding": vector_embedding,
                }
            )

        return vector_embedder_service_pb2.FileComponentVectorEmbeddings(
            file_component_vector_embeddings=file_component_vector_embeddings
        )
