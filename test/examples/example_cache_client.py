from datetime import datetime

from src.transport.cache_client import CacheClient


def _wait_enter():
    input('Press enter to exit')
    exit(0)


def main():
    client = CacheClient.initialize_client(port=8080)
    cached_value = 'hi whats up guys its scarce here back with another video on leafy'
    cached_key = '7'
    print(client.get(cached_key))
    print(client.put(cached_key, cached_value))
    print(client.get(cached_key))
    print(client.stats())
    print(client.keys())
    print(client.keys(r'8'))
    print(client.resize(3))
    client.put('55', '55', datetime.now().timestamp() + 6.9)
    print(client.get_cacheable_stats('7'))
    print(client.keys())
    print(client.stats())


if __name__ == '__main__':
    main()
    _wait_enter()
