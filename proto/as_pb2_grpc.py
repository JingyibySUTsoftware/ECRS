# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import as_pb2 as as__pb2


class ASServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.as_call = channel.unary_unary(
                '/as.ASService/as_call',
                request_serializer=as__pb2.ASRequest.SerializeToString,
                response_deserializer=as__pb2.ASResponse.FromString,
                )


class ASServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def as_call(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ASServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'as_call': grpc.unary_unary_rpc_method_handler(
                    servicer.as_call,
                    request_deserializer=as__pb2.ASRequest.FromString,
                    response_serializer=as__pb2.ASResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'as.ASService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ASService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def as_call(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/as.ASService/as_call',
            as__pb2.ASRequest.SerializeToString,
            as__pb2.ASResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
