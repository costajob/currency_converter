import datetime
import unittest
from cconv import currency


class TestCurrency(unittest.TestCase):
    def test_money(self):
        money = currency.Money('usd', '9.99')
        curr, amt = money
        self.assertEqual(curr, 'USD')
        self.assertEqual(amt, 9.99)
        self.assertEqual(repr(money), "Money('USD', 9.99)")

    def test_money_bad_amount(self):
        with self.assertRaises(ValueError):
            currency.Money('usd', 'MMCCXXII')

    def test_eur_rates(self):
        rates = currency.EurRates('2018-11-23', {'usd': '1.1352', 'CHF': '1.1316'})
        self.assertIsInstance(rates.ref_date, datetime.date)
        self.assertEqual(repr(rates), "EurRates('2018-11-23', {'USD': 1.1352, 'CHF': 1.1316})")
        self.assertEqual(rates['USD'], 1.1352)

    def test_eur_rate_bad_date(self):
        with self.assertRaises(ValueError):
            currency.EurRates('2018-11-31')


if __name__ == '__main__':
    unittest.main()
