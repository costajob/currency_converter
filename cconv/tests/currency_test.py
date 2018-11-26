import datetime
import decimal
import unittest
from cconv import currency


class TestCurrency(unittest.TestCase):
    def test_money(self):
        money = currency.Money('usd', '9.99')
        self.assertIsInstance(money.amount, decimal.Decimal)
        self.assertEqual(repr(money), "Money('USD', 9.99)")

    def test_money_bad_amount(self):
        with self.assertRaises(decimal.InvalidOperation):
            currency.Money('usd', 'MMCCXXII')

    def test_eur_rate(self):
        rate = currency.EurRate('usd', '1.1352', '2018-11-23')
        self.assertIsInstance(rate.rate, float)
        self.assertIsInstance(rate.ref_date, datetime.date)
        self.assertEqual(repr(rate), "EurRate('USD', 1.1352, '2018-11-23')")

    def test_eur_rate_bad_date(self):
        with self.assertRaises(ValueError):
            currency.EurRate('usd', '1.1352', '2018-11-31')


if __name__ == '__main__':
    unittest.main()
