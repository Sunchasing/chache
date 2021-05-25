from src.cacheables.cacheable_interface import ICacheable


class Cacheable(ICacheable):
    expires = False

    def __init__(self, value):
        super().__init__(value)

    def get_value(self):
        self.hits += 1
        return self.value

    def stats(self):
        return {
            "hits": self.hits,
            "expiry": None
        }

    @property
    def __name(self):  # pragma: no cover
        return "Cacheable"
