import unittest
from xml.etree import ElementTree
from cconv import data


class TestData(unittest.TestCase):
    def test_fetcher_local(self):
        tree = data.Fetcher('cconv/tests/stubs.xml')()
        self.assertIsInstance(tree, ElementTree.ElementTree)

    def test_parser(self):
        tree = ElementTree.parse('cconv/tests/stubs.xml')
        parser = data.Parser(tree)
        nodes = parser()
        self.assertIn('2018-11-26', nodes)
        self.assertIn('2018-08-29', nodes)
        self.assertEqual(nodes['2018-11-26']['USD'], '1.1363')
        self.assertEqual(nodes['2018-08-29']['USD'], '1.166')
        self.assertEqual(nodes['2018-08-29']['ZAR'], '16.8176')
        self.assertEqual(len(parser()), 2)

    def test_cache(self):
        col = []
        callback_1 = lambda key: {key: {'USD': '1.1363', 'ZAR': '15.7322'}}
        callback_2 = lambda key: col.append(key)
        cache = data.Cache()
        cache.fetch('2018-10-29', callback_1)
        cache.fetch('2018-10-29', callback_2)
        self.assertEqual(cache['2018-10-29'], {'2018-10-29': {'USD': '1.1363', 'ZAR': '15.7322'}})
        self.assertEqual(len(cache), 1)
        self.assertFalse(col)

    def test_cache_overflow(self):
        callback = lambda key: {key: {'USD': '1.1363', 'ZAR': '15.7322'}}
        cache = data.Cache(1)
        cache.fetch('key_1', callback)
        cache.fetch('key_2', callback)
        self.assertNotIn('key_1', cache)
        self.assertIn('key_2', cache)
        self.assertEqual(len(cache), 1)


if __name__ == '__main__':
    unittest.main()
