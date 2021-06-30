import pickle
from typing import Tuple, Text, Any, Dict, List

from grpc import Channel, insecure_channel

from src.transport.proto.cache.cache_service_pb2 import *
from src.transport.proto.cache.cache_service_pb2_grpc import CacheServiceStub
from utils import NumberType
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

    def get(self, key: Text) -> Tuple[Any, bool]:
        info(f'Trying to get value for key={key}')
        request = CacheGetQuery(key=key)
        response = self._client.Get(request)
        deserialized_response = pickle.loads(response.cacheable_value)
        return deserialized_response, response.found  # i no longer hate my life

    def put(self, key: Text, value: Any, expiry: float = None) -> bool:
        info(f'Trying to put value for key={key}, value={value}, expiry={expiry}')
        serialized_value = pickle.dumps(value)
        request = CachePutQuery(key=key, value=serialized_value, expiry=expiry)
        response = self._client.Put(request)
        return response.put_success

    def pop(self, key: Text) -> Tuple[Any, bool]:
        info(f'Trying to pop value for key={key}')
        request = CachePopQuery(key=key)
        response = self._client.Pop(request)
        deserialized_response = pickle.loads(response.cacheable_value)
        return deserialized_response, response.deleted

    def delete(self, key: Text) -> bool:
        info(f'Trying to delete for key={key}')
        request = CacheDeleteQuery(key=key)
        response = self._client.Delete(request)
        return response.deleted

    def wipe(self) -> int:
        info('Trying to wipe cache')
        request = CacheWipeQuery()
        response = self._client.Wipe(request)
        return response.entries_wiped

    def stats(self) -> Dict[Text, NumberType]:
        info('Trying to get cache stats')
        request = CacheStatsQuery()
        response = self._client.Stats(request)
        deserialized_response = pickle.loads(response.current_stats)
        return deserialized_response

    def get_cacheable_stats(self, key: Text) -> Dict[Text, NumberType]:
        info(f'Trying to get cacheable stats with key={key}')
        request = CacheableStatsQuery(key=key)
        response = self._client.CacheableStats(request)
        deserialized_response = pickle.loads(response.cacheable_stats)
        return deserialized_response

    def resize(self, new_size: int) -> int:
        info(f'Trying to resize cache with new_size={new_size}')
        request = CacheResizeQuery(new_size=new_size)
        response = self._client.Resize(request)
        return response.num_deleted_items

    def keys(self, regex_match_string: Text = None) -> List[Text]:
        info(f'Trying to get cache keys' + (f' matching_regex={regex_match_string}' if regex_match_string else ''))
        request = CacheKeysQuery(regex_match_string=regex_match_string)
        response = self._client.Keys(request)
        return response.cache_keys
