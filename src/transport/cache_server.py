from src.cache_lib import Cache
from src.cacheables import NOTEXISTS
from src.transport.proto.cache.cache_service_pb2 import *
from src.transport.proto.cache.cache_service_pb2_grpc import CacheServiceServicer
from utils import NumberType


class CacheServer(CacheServiceServicer):

    def __init__(self, max_size: int, cleaning_frequency_s: NumberType):
        self.cache = Cache(max_size, cleaning_frequency_s)

    def Get(self, request: CacheGetQuery, _) -> CacheGetResponse:
        cache_get = self.cache.get(request.key)
        exists = cache_get is NOTEXISTS
        get_response = CacheGetResponse(exists, cache_get)
        print(f'Get method invoked with key={request.key}, hit={exists}')
        return get_response

    #TODO: Do the rest when you wake up at 4 AM, okay? Okay.
    def Stats(self, request: CacheStatsResponse, _) -> CacheStatsResponse:
        return CacheStatsResponse(self.cache.stats())
