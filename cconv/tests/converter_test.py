import unittest
from cconv import converter


class TestConverter(unittest.TestCase):
    def test_computer(self):
        comp = converter.Computer(('USD', 10.0), 'DKK')
        res = comp({'USD': 1.1352, 'DKK': 7.4618})
        self.assertEqual(res['currency'], 'DKK')
        self.assertEqual(res['amount'], 65.73)


if __name__ == '__main__':
    unittest.main()
