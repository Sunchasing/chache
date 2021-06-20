from typing import Any

from google.protobuf.internal.well_known_types import Any
from grpc import Channel, insecure_channel

from src.transport.proto.cache.cache_service_pb2 import *
from src.transport.proto.cache.cache_service_pb2_grpc import CacheServiceStub
from utils.logging import info


class CacheClient:

    def __init__(self, stub: CacheServiceStub, channel: Channel):
        self._client = stub
        self._channel = channel
        info('Started cache client')

    def __del__(self):
        info('Stopped cache client')

    @classmethod
    def initialize_client(cls, port: int) -> 'CacheClient':
        channel = insecure_channel(f'localhost:{port}')
        stub = CacheServiceStub(channel=channel)
        return CacheClient(channel=channel, stub=stub)

    def get(self, key: Any) -> Any:
        info(f'Trying to get value for key={key}')
        request = CacheGetQuery(key=key)
        response = self._client.Get(request)
        return response.found, response.cacheable_value  # i hate my life

    def put(self, key: Any, value: Any, expiry: float = None) -> bool:
        info(f'Trying to put value for key={key}, value={value}, expiry={expiry}')
        # if expiry:
        request = CachePutQuery(key=key, value=value, expiry=expiry)
        # else:
        #     request = CachePutQuery(key=key, value=value)
        response = self._client.Put(request)
        return response.put_success

    def pop(self, key: Any) -> Any:
        info(f'Trying to pop value for key={key}')
        request = CachePopQuery(key=key)
        response = self._client.Pop(request)
        return response.cacheable_value, response.deleted

    def delete(self, key: Any) -> bool:
        info(f'Trying to delete for key={key}')
        request = CacheDeleteQuery(key=key)
        response = self._client.Delete(request)
        return response.deleted

    def wipe(self) -> int:
        info('Trying to wipe cache')
        request = CacheWipeQuery()
        response = self._client.Wipe(request)
        return response.entries_wiped

    def stats(self) -> Any:
        info('Trying to get cache stats')
        request = CacheStatsQuery()
        response = self._client.Stats(request)
        return response.current_stats
