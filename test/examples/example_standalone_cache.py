import datetime
import math

from src.chache import Chache


@Chache.sized_func_cache(datetime.datetime.now(), 5, 5)
def isr(x: float):
    return x ** (-1 / 2)


def main():
    isr(math.pi)
    print(isr.cache.stats())
    isr(math.pi)
    print(isr.cache.stats())


if __name__ == "__main__":
    main()
