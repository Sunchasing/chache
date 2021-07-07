import datetime
import time
from src.chache import Chache


class Market:

    def __init__(self):
        self.stability = [5, 9, 32, 100]

    @Chache.sized_func_cache(datetime.datetime.now(), 5, 5)
    def get_market_stability(self, market: int):
        return self.stability[market]

    @Chache.sized_func_cache(expiry=datetime.datetime.now(), max_size=2, cleaning_frequency_s=5)
    def get_market_volatility(self, market: int):
        return self.stability[::-1][market]


def main():
    market = Market()
    print(market.get_market_volatility(0))
    print(market.get_market_volatility.cache.stats())
    print(market.get_market_stability(0))
    print(market.get_market_stability.cache.stats())
    time.sleep(8)
    print(market.get_market_stability.cache.stats())


if __name__ == "__main__":
    main()
