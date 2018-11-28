import unittest
from xml.etree import ElementTree
from cconv import data


class TestData(unittest.TestCase):
    def test_fetcher_local(self):
        tree = data.Fetcher('cconv/tests/stubs.xml')()
        self.assertIsInstance(tree, ElementTree.ElementTree)

    def test_parser(self):
        tree = data.Fetcher('cconv/tests/stubs.xml')()
        parser = data.Parser(tree)
        nodes = parser()
        self.assertIn('2018-11-26', nodes)
        self.assertIn('2018-08-29', nodes)
        self.assertEqual(nodes['2018-11-26']['USD'], '1.1363')
        self.assertEqual(nodes['2018-08-29']['USD'], '1.166')
        self.assertEqual(nodes['2018-08-29']['ZAR'], '16.8176')
        self.assertEqual(len(parser()), 2)


if __name__ == '__main__':
    unittest.main()

