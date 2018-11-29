import unittest
from cconv import converter


class TestConverter(unittest.TestCase):
    def test_computer(self):
        comp = converter.Computer(('USD', 10.0), 'DKK', {'USD': 1.1352, 'DKK': 7.4618})
        res = comp()
        self.assertEqual(res['currency'], 'DKK')
        self.assertEqual(res['amount'], 65.73)

    def test_computer_error(self):
        comp = converter.Computer(('USD', 10.0), 'CHF', {'USD': 1.1352, 'DKK': 7.4618})
        with self.assertRaises(converter.Computer.CurrencyError):
            comp()

    def test_computer_same(self):
        comp = converter.Computer(('USD', 10.0), 'USD', {})
        res = comp()
        self.assertEqual(res['currency'], 'USD')
        self.assertEqual(res['amount'], 10.0)

    def test_computer_eur_src(self):
        comp = converter.Computer(('EUR', 10.0), 'USD', {'USD': 1.1352})
        res = comp()
        self.assertEqual(res['currency'], 'USD')
        self.assertEqual(res['amount'], 11.35)

    def test_computer_eur_dest(self):
        comp = converter.Computer(('USD', 10.0), 'EUR', {'USD': 1.1352})
        res = comp()
        self.assertEqual(res['currency'], 'EUR')
        self.assertEqual(res['amount'], 8.81)


if __name__ == '__main__':
    unittest.main()
