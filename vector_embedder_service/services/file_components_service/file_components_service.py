import grpc, os

from .pb import file_components_service_pb2, file_components_service_pb2_grpc


def get_file_components(file_component_ids: list[int]) -> list[dict]:
    file_components_service_address = os.environ.get("FILE_COMPONENTS_SERVICE_ADDRESS")
    
    with grpc.insecure_channel(file_components_service_address) as channel:
        stub = file_components_service_pb2_grpc.FileComponentsServiceStub(channel)
        
        request = file_components_service_pb2.FileComponentIds(
            file_component_ids=file_component_ids
        )
        
        response = stub.GetFileComponents(request)
        
        return [
            {
                "id": file_component.id,
                "user_id": file_component.user_id,
                "file_path": file_component.file_path,
                "start_line": file_component.start_line,
                "end_line": file_component.end_line,
                "content": file_component.content,
            }
            for file_component in response.file_components
        ]
        
        