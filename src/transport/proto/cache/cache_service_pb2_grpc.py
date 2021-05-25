# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from src.transport.proto.cache import cache_service_pb2 as cache_dot_cache__service__pb2


class CacheServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Get = channel.unary_unary(
                '/cache_transport.CacheService/Get',
                request_serializer=cache_dot_cache__service__pb2.CacheGetQuery.SerializeToString,
                response_deserializer=cache_dot_cache__service__pb2.CacheGetResponse.FromString,
                )
        self.Put = channel.unary_unary(
                '/cache_transport.CacheService/Put',
                request_serializer=cache_dot_cache__service__pb2.CachePutQuery.SerializeToString,
                response_deserializer=cache_dot_cache__service__pb2.CachePutResponse.FromString,
                )
        self.Pop = channel.unary_unary(
                '/cache_transport.CacheService/Pop',
                request_serializer=cache_dot_cache__service__pb2.CachePopQuery.SerializeToString,
                response_deserializer=cache_dot_cache__service__pb2.CachePopResponse.FromString,
                )
        self.Delete = channel.unary_unary(
                '/cache_transport.CacheService/Delete',
                request_serializer=cache_dot_cache__service__pb2.CacheDeleteQuery.SerializeToString,
                response_deserializer=cache_dot_cache__service__pb2.CacheStatsResponse.FromString,
                )
        self.Wipe = channel.unary_unary(
                '/cache_transport.CacheService/Wipe',
                request_serializer=cache_dot_cache__service__pb2.CacheWipeQuery.SerializeToString,
                response_deserializer=cache_dot_cache__service__pb2.CacheWipeResponse.FromString,
                )
        self.Stats = channel.unary_unary(
                '/cache_transport.CacheService/Stats',
                request_serializer=cache_dot_cache__service__pb2.CacheStatsQuery.SerializeToString,
                response_deserializer=cache_dot_cache__service__pb2.CacheStatsResponse.FromString,
                )


class CacheServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Get(self, request, context):
        """Gets the cacheable's value at key position, if it exists
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Put(self, request, context):
        """Caches a k:v pair in the cache
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Pop(self, request, context):
        """Pops cacheable at key position
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete(self, request, context):
        """Deletes a cacheable at key position
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Wipe(self, request, context):
        """Deletes all cacheables, keeps stats
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Stats(self, request, context):
        """Gets cache stats
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CacheServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=cache_dot_cache__service__pb2.CacheGetQuery.FromString,
                    response_serializer=cache_dot_cache__service__pb2.CacheGetResponse.SerializeToString,
            ),
            'Put': grpc.unary_unary_rpc_method_handler(
                    servicer.Put,
                    request_deserializer=cache_dot_cache__service__pb2.CachePutQuery.FromString,
                    response_serializer=cache_dot_cache__service__pb2.CachePutResponse.SerializeToString,
            ),
            'Pop': grpc.unary_unary_rpc_method_handler(
                    servicer.Pop,
                    request_deserializer=cache_dot_cache__service__pb2.CachePopQuery.FromString,
                    response_serializer=cache_dot_cache__service__pb2.CachePopResponse.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=cache_dot_cache__service__pb2.CacheDeleteQuery.FromString,
                    response_serializer=cache_dot_cache__service__pb2.CacheStatsResponse.SerializeToString,
            ),
            'Wipe': grpc.unary_unary_rpc_method_handler(
                    servicer.Wipe,
                    request_deserializer=cache_dot_cache__service__pb2.CacheWipeQuery.FromString,
                    response_serializer=cache_dot_cache__service__pb2.CacheWipeResponse.SerializeToString,
            ),
            'Stats': grpc.unary_unary_rpc_method_handler(
                    servicer.Stats,
                    request_deserializer=cache_dot_cache__service__pb2.CacheStatsQuery.FromString,
                    response_serializer=cache_dot_cache__service__pb2.CacheStatsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cache_transport.CacheService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CacheService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cache_transport.CacheService/Get',
            cache_dot_cache__service__pb2.CacheGetQuery.SerializeToString,
            cache_dot_cache__service__pb2.CacheGetResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Put(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cache_transport.CacheService/Put',
            cache_dot_cache__service__pb2.CachePutQuery.SerializeToString,
            cache_dot_cache__service__pb2.CachePutResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Pop(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cache_transport.CacheService/Pop',
            cache_dot_cache__service__pb2.CachePopQuery.SerializeToString,
            cache_dot_cache__service__pb2.CachePopResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cache_transport.CacheService/Delete',
            cache_dot_cache__service__pb2.CacheDeleteQuery.SerializeToString,
            cache_dot_cache__service__pb2.CacheStatsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Wipe(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cache_transport.CacheService/Wipe',
            cache_dot_cache__service__pb2.CacheWipeQuery.SerializeToString,
            cache_dot_cache__service__pb2.CacheWipeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Stats(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cache_transport.CacheService/Stats',
            cache_dot_cache__service__pb2.CacheStatsQuery.SerializeToString,
            cache_dot_cache__service__pb2.CacheStatsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
