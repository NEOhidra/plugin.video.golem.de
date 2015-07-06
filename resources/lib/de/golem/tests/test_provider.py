import datetime

__author__ = 'bromix'

import unittest

from resources.lib.org.bromix import nightcrawler
from resources.lib.de import golem


class TestProvider(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # clear the cache
        # nightcrawler.Context().get_function_cache().clear()
        pass

    def test_on_root(self):
        context = nightcrawler.Context(path='/')
        result = golem.Provider().navigate(context)
        self.assertGreaterEqual(len(result), 7)
        pass

    def test_on_browse_newest(self):
        context = nightcrawler.Context(path='/browse/newest/')
        result = golem.Provider().navigate(context)
        self.assertEquals(len(result), 50)
        pass

    def test_on_week_in_review(self):
        # test years
        context = nightcrawler.Context(path='/browse/by-query/', params={'q': 'wochenrueckblick'})
        result = golem.Provider().navigate(context)
        self.assertGreaterEqual(len(result), 1)

        # test month
        now = datetime.datetime.now()-datetime.timedelta(30)
        context = nightcrawler.Context(path='/browse/by-query/%d/' % now.year, params={'q': 'wochenrueckblick'})
        result = golem.Provider().navigate(context)
        self.assertGreaterEqual(len(result), 1)

        # test end result
        context = nightcrawler.Context(path='/browse/by-query/%d/%d/' % (now.year, now.month),
                                       params={'q': 'wochenrueckblick'})
        result = golem.Provider().navigate(context)
        self.assertGreaterEqual(len(result), 1)
        pass

    def test_on_manufacturer_videos(self):
        now = datetime.datetime.now()-datetime.timedelta(30)
        context = nightcrawler.Context(path='/browse/by-query/%d/%d/' % (now.year, now.month),
                                       params={'q': 'herstellervideo'})
        result = golem.Provider().navigate(context)
        self.assertGreaterEqual(len(result), 1)
        pass

    def test_on_trailer(self):
        now = datetime.datetime.now()-datetime.timedelta(30)
        context = nightcrawler.Context(path='/browse/by-query/%d/%d/' % (now.year, now.month),
                                       params={'q': 'trailer'})
        result = golem.Provider().navigate(context)
        self.assertGreaterEqual(len(result), 1)
        pass

    def test_on_year(self):
        now = datetime.datetime.now()
        context = nightcrawler.Context(path='/browse/date/%d/' % now.year)
        result = golem.Provider().navigate(context)
        self.assertEquals(len(result), now.month)
        pass

    def test_on_year_and_month(self):
        now = datetime.datetime.now()
        context = nightcrawler.Context(path='/browse/date/%d/%d/' % (now.year, now.month))
        result = golem.Provider().navigate(context)
        self.assertEquals(len(result), 1)
        pass

    def test_on_browse_all(self):
        context = nightcrawler.Context(path='/browse/all/')
        result = golem.Provider().navigate(context)
        self.assertGreaterEqual(len(result), 100)
        pass

    def test_on_play(self):
        context = nightcrawler.Context(path='/browse/newest/')
        result = golem.Provider().navigate(context)
        video = result[0]

        path, params = nightcrawler.utils.path.from_uri(video['uri'])
        context = nightcrawler.Context(path, params)
        result = golem.Provider().navigate(context)
        self.assertEquals(result['type'], 'uri')
        self.assertIsNotNone(result.get('uri', None))
        pass

    # ===================

    def test_on_year2(self):
        now = datetime.datetime.now()
        context = nightcrawler.Context(path='/browse/year/%d/' % now.year)
        result = golem.Provider().navigate(context)
        self.assertEquals(len(result), now.month)
        pass

    def test_on_search_list(self):
        provider = golem.Provider()

        context = nightcrawler.Context(path='/search/list/')
        result = provider.navigate(context)
        items = result[0]
        pass

    def test_on_search_query(self):
        provider = golem.Provider()

        context = nightcrawler.Context(path='/search/query/', params={'q': 'Lenovo'})
        result = provider.navigate(context)
        items = result[0]
        pass

    pass
