import pickle
import re
import threading
from concurrent.futures.thread import ThreadPoolExecutor

import grpc

from src.chache import Chache
from src.cacheables import NOTEXISTS
from src.transport.proto.cache.cache_service_pb2 import *
from src.transport.proto.cache.cache_service_pb2_grpc import CacheServiceServicer, add_CacheServiceServicer_to_server
from utils import NumberType
from utils.logging import *


class CacheService(CacheServiceServicer):

    def __init__(self, max_size: int, cleaning_frequency_s: NumberType):
        self.cache = Chache(max_size, cleaning_frequency_s)
        info('Started cache service')

    def __del__(self):
        info('Stopped cache service')

    def Get(self, request: CacheGetQuery, _) -> CacheGetResponse:
        cache_get = self.cache.get(request.key)
        exists = cache_get is not NOTEXISTS
        if not exists:
            cache_get = pickle.dumps(cache_get)

        get_response = CacheGetResponse(found=exists, cacheable_value=cache_get)
        info(f"Get method invoked with key={request.key}, hit={exists}")
        return get_response

    def Put(self, request: CachePutQuery, _) -> CachePutResponse:

        # expiry is unix timestamp to be converted to datetime
        actual_expiry = datetime.datetime.fromtimestamp(request.expiry)

        cache_put = self.cache.put(request.key, request.value, actual_expiry)
        put_response = CachePutResponse(put_success=cache_put)
        info(f"Put method invoked with key={request.key}, expiry={actual_expiry}, success={cache_put}")
        return put_response

    def Pop(self, request: CachePopQuery, _) -> CachePopResponse:
        cache_pop, deleted = self.cache.pop(request.key)
        cache_pop = None if cache_pop is NOTEXISTS else cache_pop
        pop_response = CachePopResponse(cacheable_value=cache_pop, deleted=deleted)
        info(f"Put method invoked with key={request.key}, success={deleted}")
        return pop_response

    def Delete(self, request: CacheDeleteQuery, _) -> CacheDeleteResponse:
        deleted = self.cache.delete(request.key)
        delete_response = CacheDeleteResponse(deleted=deleted)
        info(f"Delete method invoked with key={request.key}, success={deleted}")
        return delete_response

    def Wipe(self, _: CacheWipeQuery, __) -> CacheWipeResponse:
        wiped = self.cache.wipe()
        wipe_response = CacheWipeResponse(entries_wiped=wiped)
        info(f"Wipe method invoked, entries_wiped={wiped}")
        return wipe_response

    def Stats(self, _: CacheStatsResponse, __) -> CacheStatsResponse:
        cache_stats = self.cache.stats()
        serialized_stats = pickle.dumps(cache_stats)
        stats_response = CacheStatsResponse(current_stats=serialized_stats)
        info(f"Stats method invoked")
        return stats_response

    def CacheableStats(self, request: CacheableStatsQuery, _) -> CacheableStatsResponse:
        cacheable_stats = self.cache.get_cacheable_stats(request.key)
        serialized_cacheable_stats = pickle.dumps(cacheable_stats)
        cacheable_stats_response = CacheableStatsResponse(cacheable_stats=serialized_cacheable_stats)
        return cacheable_stats_response

    def Resize(self, request: CacheResizeQuery, _) -> CacheResizeResponse:
        deleted_keys: int = self.cache.resize(request.new_size)
        resize_response = CacheResizeResponse(num_deleted_items=deleted_keys)
        return resize_response

    def Keys(self, request: CacheKeysQuery, _) -> CacheKeysResponse:
        cache_keys = self.cache.keys()

        if request.regex_match_string:
            cache_keys = [key for key in cache_keys if re.search(request.regex_match_string, key)]
        else:
            cache_keys = list(cache_keys)

        cache_keys_response = CacheKeysResponse(cache_keys=cache_keys)

        return cache_keys_response


def start_server(service: CacheService, port: int, max_workers: int = 10) -> grpc.Server:
    server = grpc.server(ThreadPoolExecutor(max_workers=max_workers))
    add_CacheServiceServicer_to_server(server=server, servicer=service)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    threading.Thread(target=server.wait_for_termination, daemon=True).start()
    return server
