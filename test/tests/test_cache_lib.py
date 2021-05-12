import unittest
from parameterized import parameterized
from src.cache_lib import Cache
from src.cacheables import ICacheable, NOTEXISTS, new_cacheable
from utils import NumberType
import datetime as dt
import threading
import time
from typing import Text, Dict, Any, Union, NoReturn, KeysView, ValuesView, ItemsView, Callable


class TestCache(unittest.TestCase):

    def setUp(self) -> Any:
        self.max_size = 3
        self.cleaning_freq = 120
        self.cache = Cache(max_size=self.max_size, cleaning_frequency_s=self.cleaning_freq)

    def test_init(self) -> NoReturn:
        self.assertTrue(self.cache.cleaner_thread.is_alive())

    def test_max_size_and_lru_rules(self):
        last_added_value = self.max_size + 1
        for x in range(last_added_value):
            self.cache.put(str(x), x)

        self.assertEqual(str(last_added_value - 1), self.cache.mru)
        self.assertLessEqual(self.cache.size, last_added_value)
        self.assertEqual(self.cache.lru, "1")

    def test_operations(self):

        gettable_key = "flowers"
        gettable_value = "pot"
        new_gettable_key = "bees"
        new_gettable_value = "knees"
        self.assertEqual(self.cache.get(gettable_key), NOTEXISTS)
        self.cache.put(gettable_key, gettable_value)
        self.assertEqual(self.cache.get(gettable_key), gettable_value)

        self.cache.put(new_gettable_key, new_gettable_value)
        self.assertEqual(self.cache.data.get(gettable_key).next_key, new_gettable_key)
        self.assertEqual(self.cache.data.get(new_gettable_key).previous_key, gettable_key)
        self.cache.pop(gettable_key)

        got_stats = self.cache.stats()
        self.assertEqual(got_stats.get("misses"), 1)
        self.assertEqual(got_stats.get("hits"), 2)
        self.assertEqual(got_stats.get("accesses"), 3)
        self.assertEqual(self.cache.data.get(new_gettable_key).next_key, None)
        self.assertEqual(self.cache.data.get(new_gettable_key).previous_key, None)
