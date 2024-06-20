# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from . import vector_embedder_service_pb2 as vector__embedder__service__pb2

GRPC_GENERATED_VERSION = '1.64.1'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in vector_embedder_service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class VectorEmbedderServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.BatchVectorEmbedFileComponents = channel.unary_unary(
                '/VectorEmbedderService/BatchVectorEmbedFileComponents',
                request_serializer=vector__embedder__service__pb2.BatchVectorEmbedFileComponentsRequest.SerializeToString,
                response_deserializer=vector__embedder__service__pb2.FileComponentVectorEmbeddings.FromString,
                _registered_method=True)


class VectorEmbedderServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def BatchVectorEmbedFileComponents(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_VectorEmbedderServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'BatchVectorEmbedFileComponents': grpc.unary_unary_rpc_method_handler(
                    servicer.BatchVectorEmbedFileComponents,
                    request_deserializer=vector__embedder__service__pb2.BatchVectorEmbedFileComponentsRequest.FromString,
                    response_serializer=vector__embedder__service__pb2.FileComponentVectorEmbeddings.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'VectorEmbedderService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('VectorEmbedderService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class VectorEmbedderService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def BatchVectorEmbedFileComponents(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/VectorEmbedderService/BatchVectorEmbedFileComponents',
            vector__embedder__service__pb2.BatchVectorEmbedFileComponentsRequest.SerializeToString,
            vector__embedder__service__pb2.FileComponentVectorEmbeddings.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
