
from src.cache_lib import Cache

@Cache.func_cache # TODO: add functionallity to set timed cache
def pancakes(x, y, z):
    print('called')
    print(x+y+z)


def main():
    pancakes(1,5,4)
    pancakes(2,2,4)
    pancakes(1,5,4)


if __name__ == "__main__":
    main()
