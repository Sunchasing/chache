
from src.cache_lib import Cache


def main():
    party = "party"
    cache = Cache(max_size=2)
    cache.put(("a pot of gold",), 0)
    cache.put(("forest",), "fire")
    print(cache.lru)
    print(cache.mru)
    print(cache.get(("forest",)))
    print(f'putting {cache.put(("pancake",), party)}')
    print(f'lru: {cache.lru}')
    print(cache.get(("a pot of gold",)))
    print(cache.stats())

if __name__ == "__main__":
    main()
