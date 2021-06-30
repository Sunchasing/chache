import unittest
from typing import Text, Any, NoReturn

from src.chache import Chache
from src.cacheables import NOTEXISTS


class TestCache(unittest.TestCase):

    def setUp(self) -> Any:
        self.max_size = 3
        self.cleaning_freq = 120
        self.cache = Chache(max_size=self.max_size, cleaning_frequency_s=self.cleaning_freq)

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

        # Tests the get() method when we have and don't have a cached value
        self.assertEqual(self.cache.get(gettable_key), NOTEXISTS)
        self.cache.put(gettable_key, gettable_value)
        self.assertEqual(self.cache.get(gettable_key), gettable_value)

        # Tests the put() method and the linking between cacheables
        self.cache.put(new_gettable_key, new_gettable_value)
        self.assertEqual(self.cache.data.get(gettable_key).next_key, new_gettable_key)
        self.assertEqual(self.cache.data.get(new_gettable_key).previous_key, gettable_key)
        self.cache.pop(gettable_key)

        # Tests the stats() method for the cache and if it's properly updating
        got_stats = self.cache.stats()
        self.assertEqual(got_stats.get("misses"), 1)
        self.assertEqual(got_stats.get("hits"), 2)
        self.assertEqual(got_stats.get("accesses"), 3)
        self.assertEqual(self.cache.data.get(new_gettable_key).next_key, None)
        self.assertEqual(self.cache.data.get(new_gettable_key).previous_key, None)

    def test_decorator(self):
        @Chache.sized_func_cache(expiry=None, max_size=2, cleaning_frequency_s=10)
        def testable_function(arr: Text) -> Text:
            return arr[-1]

        testable_function('horse')
        testable_function('eels')
        testable_function('maniac')

        # Tests the proper linking when Cache is used as a decorator
        self.assertEqual(testable_function.cache.data[('maniac',)].previous_key, ('eels',))

        # Tests the stats() method when Cache is used as a decorator
        maniac_stats = testable_function.cache.data[('maniac',)].stats()
        self.assertEqual(maniac_stats['hits'], 0)
        self.assertEqual(maniac_stats['expiry'], None)
        testable_function('maniac')
        maniac_stats = testable_function.cache.data[('maniac',)].stats()
        self.assertEqual(maniac_stats['hits'], 1)
        self.assertEqual(maniac_stats['expiry'], None)

        # Tests the get_cacheable_stats() method when Cache is used as a decorator
        eels_stats = testable_function.cache.get_cacheable_stats(('eels',))
        self.assertEqual(eels_stats, {'expiry': None, 'hits': 0})

        # Tests the wipe() method when Cache is used as a decorator
        before_wipe_stats = testable_function.cache.stats()
        testable_function.cache.wipe()
        self.assertEqual(testable_function.cache.stats(), before_wipe_stats)
        self.assertEqual(testable_function.cache.size, 0)

        # Tests the resize() method when Cache is used as a decorator
        self.assertEqual(testable_function.cache.max_size, 2)
        testable_function.cache.resize(15)
        self.assertEqual(testable_function.cache.max_size, 15)
