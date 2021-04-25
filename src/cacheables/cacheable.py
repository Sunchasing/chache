from src.cacheables.cacheable_interface import ICacheable


class Cacheable(ICacheable):
    expires = False

    def __init__(self, value):
        super().__init__(value)
        self.mem_size = 0.0
        self.value_mem_size = 0.0

    def get(self):
        self.hits += 1
        return self.value

    def stats(self):
        return {
            "hits": self.hits,
            "mem_size": self.mem_size,
            "val_size": self.value_mem_size,
            "expiry": None
            }

    def _compute_mem_sizes(self):
        ...
