from datetime import datetime


class Money:
    """
    Synopsis
    ========
    Represents the money value object, with currency and current amount expressed
    as a float object (assuming loss of precision is acceptable in favor of speed).

    Examples
    ========
    >>> money = Money('USD', 9.99)
    >>> print(money)
    Money('USD', 9.99)
    """

    def __init__(self, currency, amount=0):
        self.currency = str(currency).upper()
        self.amount = float(amount)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.currency}', {self.amount})"

    def __iter__(self):
        return (attr for attr in (self.currency, self.amount))


class EurRates:
    """
    Synopsis
    ========
    Represents the exchange rates of various currencies as EUR one by the specified
    reference date.
    The data is represented as a dict object with currency ISO as the key and a the
    exchange rate float as a value.

    Examples
    ========
    >>> rates = EurRates('2018-11-23')
    >>> print(rates)
    EurRates('2018-11-23', {})
    """

    FORMAT = '%Y-%m-%d'

    @classmethod
    def bulk(cls, data):
        """
        Creates a list of EurRates objects by a nested dict structure:
        """

    def __init__(self, ref_date, data={}):
        self.ref_date = datetime.strptime(ref_date, self.FORMAT).date()
        self.data = self._normalize(data)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.ref_date}', {self.data})"

    def __getitem__(self, key):
        return self.data[key]

    def _normalize(self, data):
        return {str(k).upper(): float(v) for k, v in data.items()}
