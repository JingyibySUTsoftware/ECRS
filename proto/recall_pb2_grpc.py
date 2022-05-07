# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import recall_pb2 as recall__pb2


class RecallServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.recall = channel.unary_unary(
                '/recall.RecallService/recall',
                request_serializer=recall__pb2.RecallRequest.SerializeToString,
                response_deserializer=recall__pb2.RecallResponse.FromString,
                )


class RecallServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def recall(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RecallServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'recall': grpc.unary_unary_rpc_method_handler(
                    servicer.recall,
                    request_deserializer=recall__pb2.RecallRequest.FromString,
                    response_serializer=recall__pb2.RecallResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'recall.RecallService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RecallService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def recall(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/recall.RecallService/recall',
            recall__pb2.RecallRequest.SerializeToString,
            recall__pb2.RecallResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)