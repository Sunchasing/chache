import datetime
import unittest
from typing import Text, Any, NoReturn

from src.cacheables import NOTEXISTS, new_cacheable
from src.chache import Chache


class TestCache(unittest.TestCase):

    def setUp(self) -> Any:
        self.max_size = 3
        self.cleaning_freq = 3
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
        cache_reply = self.cache.data.get(gettable_key).next_key
        self.assertEqual(cache_reply, new_gettable_key)
        cache_reply = self.cache.data.get(new_gettable_key).previous_key
        self.assertEqual(cache_reply, gettable_key)
        cache_reply = self.cache.put(new_gettable_key, new_gettable_value)
        self.assertEqual(cache_reply, False)

        # Tests the pop() method
        self.cache.pop(gettable_key)
        cache_reply = self.cache.get(gettable_key)
        self.assertEqual(cache_reply, NOTEXISTS)

        # Tests the stats() method for the cache and if it's properly updating
        got_stats = self.cache.stats()
        self.assertEqual(got_stats.get("misses"), 2)
        self.assertEqual(got_stats.get("hits"), 2)
        self.assertEqual(got_stats.get("accesses"), 4)
        self.assertEqual(self.cache.data.get(new_gettable_key).next_key, None)
        self.assertEqual(self.cache.data.get(new_gettable_key).previous_key, None)

    def test_update(self):
        # Tests the update() method and proper updating
        self.cache.put("bees", "no thank you")
        updated_gettable_time = datetime.datetime.now()
        missing_key = 'sanction Mars'
        missing_value = 'new spaceship who dis'
        update_success = self.cache.update("bees", "sand", updated_gettable_time)
        self.assertEqual(update_success, True)
        update_value = self.cache.get("bees")
        self.assertEqual(update_value, "sand")
        updated = self.cache.update(missing_key, missing_value, updated_gettable_time)
        self.assertEqual(updated, False)
        self.cache.update("bees", "sand", updated_gettable_time)

    def test_resize(self):
        # Tests the resize() method
        self.cache.put('kek', 'w')
        self.cache.put('kappa', 'pride')
        self.assertEqual(self.cache.max_size, 3)
        self.cache.resize(15)
        self.assertEqual(self.cache.max_size, 15)
        num_deleted_on_resized = self.cache.resize(1)
        self.assertEqual(self.cache.max_size, 1)
        self.assertEqual(num_deleted_on_resized, 1)

    def test__get_hashable_key(self):
        # Tests hashing to string

        hash_list = ['yes', 'no']
        hash_set = {'banana'}
        hash_tuple = ('borgir')

        cache_reply = self.cache._get_hashable_key(hash_list)
        self.assertEqual(cache_reply, str(hash_list))

        cache_reply = self.cache._get_hashable_key(hash_set)
        self.assertEqual(cache_reply, str(hash_set))

        cache_reply = self.cache._get_hashable_key(hash_tuple)
        self.assertEqual(cache_reply, str(hash_tuple))


    def test_decorator(self):

        @Chache.sized_func_cache(expiry=None, max_size=2, cleaning_frequency_s=10)
        def testable_function(arr: Text) -> Text:
            return 'yes'

        testable_function('no')

        # Tests if the decorator has injected a cache into the function
        self.assertIsInstance(testable_function.cache, Chache)

        # @Chache.sized_func_cache(expiry=None, max_size=2, cleaning_frequency_s=10)
        # def testable_function(arr: Text) -> Text:
        #     return arr[-1]
        #
        #
        #
        # testable_function('horse')
        # testable_function('eels')
        # testable_function('maniac')
        #
        #
        # # Tests the proper linking when Cache is used as a decorator
        # self.assertEqual(testable_function.cache.data[('maniac',)].previous_key, ('eels',))
        #
        # # Tests the stats() method when Cache is used as a decorator
        # maniac_stats = testable_function.cache.data[('maniac',)].stats()
        # self.assertEqual(maniac_stats['hits'], 0)
        # self.assertEqual(maniac_stats['expiry'], None)
        # testable_function('maniac')
        # maniac_stats = testable_function.cache.data[('maniac',)].stats()
        # self.assertEqual(maniac_stats['hits'], 1)
        # self.assertEqual(maniac_stats['expiry'], None)
        #
        # # Tests the get_cacheable_stats() method when Cache is used as a decorator
        # eels_stats = testable_function.cache.get_cacheable_stats(('eels',))
        # self.assertEqual(eels_stats, {'expiry': None, 'hits': 0})
        #
        # # Tests the wipe() method when Cache is used as a decorator
        # before_wipe_stats = testable_function.cache.stats()
        # testable_function.cache.wipe()
        # self.assertEqual(testable_function.cache.stats(), before_wipe_stats)
        # self.assertEqual(testable_function.cache.size, 0)
        #
        # # Tests the resize() method when Cache is used as a decorator
        # self.assertEqual(testable_function.cache.max_size, 2)
        # testable_function.cache.resize(15)
        # self.assertEqual(testable_function.cache.max_size, 15)


class TestCacheable(unittest.TestCase):

    def setUp(self) -> Any:
        self.target_time = datetime.datetime.now()
        self.untimed = new_cacheable('monkey')
        self.timed = new_cacheable('chimney', self.target_time)
        self.not_exists = NOTEXISTS

    def test_functionality(self):
        # Tests persistent cacheable
        cacheable_reply = self.untimed.get_value()
        self.assertEqual(cacheable_reply, 'monkey')
        cacheable_reply = self.untimed.stats()
        self.assertEqual(cacheable_reply, {"hits": 1, "expiry": None})

        # Tests expiring cacheable
        cacheable_reply = self.timed.get_value()
        self.assertEqual(cacheable_reply, 'chimney')
        cacheable_reply = self.timed.stats()
        self.assertEqual(cacheable_reply, {"hits": 1, "expiry": self.target_time})
        new_expiration = datetime.datetime.now()
        self.timed.set_expiration_to(new_expiration)
        self.assertEqual(self.timed.expiration, new_expiration)

        self.timed.update_expiration_by(datetime.timedelta(1))
        self.assertEqual(self.timed.expiration, new_expiration + datetime.timedelta(1))

        # Tests NOTEXISTS cacheable
        cacheable_reply = self.not_exists.get_value()
        assert (cacheable_reply, None)
