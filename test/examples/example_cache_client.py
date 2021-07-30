import math

from src.transport.cache_client import CacheClient


def _wait_enter():
    input('Press enter to exit')
    exit(0)


def main():
    client = CacheClient.initialize_client(port=8080)
    cached_value = math.pi ** (-1 / 2)
    cached_key = 'remove the brackets from the value and it will still work'
    client.put(cached_key, cached_value)
    got_value, found = client.get(cached_key)
    print(client.stats())
    print(got_value, found)


if __name__ == '__main__':
    main()
    _wait_enter()
