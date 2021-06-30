from src.chache import Chache


@Chache.sized_func_cache(None, 10, 102)
def pancakes(x, y, z):
    print(x+y+z)


@Chache.sized_func_cache(None, None, 102)
def pound_cakes(x, y, z):
    print(x+y+z)

def main():
    pancakes(1, 5, 4)
    pancakes(2, 2, 4)
    pancakes(1, 5, 4)
    print(pancakes.cache.stats())
    pound_cakes(1, 5, 4)
    pound_cakes(2, 2, 4)
    pound_cakes(1, 5, 4)
    print(pound_cakes.get_cacheable_stats((1, 5, 4)))


if __name__ == "__main__":
    main()
