from src.transport.proto.cache.cache_service_pb2 import (
    CacheQuery,
    CacheStats,
    CacheQueryResponse,
    CacheStatsResponse
)

from src.transport.proto.cache.cache_service_pb2_grpc import (
    CacheService,
    CacheServiceServicer,
    CacheServiceStub,
    add_CacheServiceServicer_to_server
)
