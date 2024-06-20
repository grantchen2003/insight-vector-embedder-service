import concurrent, grpc, os

from vector_embedder_service.handlers import VectorEmbedderService
from vector_embedder_service.protobufs import vector_embedder_service_pb2_grpc


def start() -> None:
    server = grpc.server(
        concurrent.futures.ThreadPoolExecutor(),
        options=[("grpc.max_receive_message_length", -1)],
    )

    vector_embedder_service_pb2_grpc.add_VectorEmbedderServiceServicer_to_server(
        VectorEmbedderService(), server
    )

    address = f"{os.environ['DOMAIN']}:{os.environ['PORT']}"
    server.add_insecure_port(address)
    print(f"starting vector embedder service on {address}")
    server.start()
    server.wait_for_termination()