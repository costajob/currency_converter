from datetime import datetime
from decimal import Decimal


class Money:
    """
    Synopsis
    ========
    Represents the money value object, with currency and current amount expressed
    as a decimal class to support precise float arithmetics.

    Examples
    ========
    >>> money = Money('USD', 9.99)
    >>> print(money)
    Money('USD', 9.99)
    """

    def __init__(self, currency, amount=0):
        self.currency = str(currency).upper()
        self.amount = Decimal(amount)

    def __repr__(self):
        return f"Money('{self.currency}', {float(self.amount)})"


class EurRate:
    """
    Synopsis
    ========
    Represents the exchange rate value object related to the EUR currency.

    Examples
    ========
    >>> rate = EurRate('USD', 1.1352, '2018-11-23')
    >>> print(rate)
    EurRate('USD', 1.1352, '2018-11-23')
    """

    FORMAT = '%Y-%m-%d'

    def __init__(self, currency, rate, ref_date):
        self.currency = str(currency).upper()
        self.rate = float(rate)
        self.ref_date = datetime.strptime(ref_date, self.FORMAT).date()

    def __repr__(self):
        return f"EurRate('{self.currency}', {self.rate}, '{self.ref_date}')"
