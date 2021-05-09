
from src.cache_lib import Cache


@Cache.sized_func_cache(None, 10, 102)
def pancakes(x, y, z):
    print(x+y+z)


@Cache.sized_func_cache(None, 10, 102)
def pound_cakes(x, y, z):
    print(x+y+z)

def main():
    pancakes(1, 5, 4)
    pancakes(2, 2, 4)
    pancakes(1, 5, 4)
    print(pancakes.cache_stats)
    print(pancakes)
    pound_cakes(1, 5, 4)
    pound_cakes(2, 2, 4)
    pound_cakes(1, 5, 4)
    print(pound_cakes.cache_stats)
    print(pound_cakes)
    pancakes(1, 5, 4)
    pancakes(2, 2, 4)
    pancakes(1, 5, 4)
    print(pancakes.cache_stats)
    print(pancakes)
    pound_cakes(1, 5, 4)
    pound_cakes(2, 2, 4)
    pound_cakes(1, 5, 4)
    print(pound_cakes.cache_stats)
    print(pound_cakes)


if __name__ == "__main__":
    main()
