import unittest
from cconv import data


class TestData(unittest.TestCase):
    def test_document(self):
        tree = data.Fetcher('cconv/tests/stubs.xml')()
        doc = data.Document(tree)
        nodes = doc()
        self.assertIn('2018-11-26', nodes)
        self.assertIn('2018-08-29', nodes)
        self.assertEqual(nodes['2018-11-26']['USD'], '1.1363')
        self.assertEqual(nodes['2018-08-29']['USD'], '1.166')
        self.assertEqual(nodes['2018-08-29']['ZAR'], '16.8176')
        self.assertEqual(len(doc()), 2)


if __name__ == '__main__':
    unittest.main()

