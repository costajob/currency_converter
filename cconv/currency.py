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

    Examples
    ========
    >>> rates = EurRates('2018-11-23', {'usd': '1.1363', 'ZAR': '15.7322'})
    >>> print(rates)
    EurRates('2018-11-23', {'USD': 1.1363, 'ZAR': 15.7322})
    """

    FORMAT = '%Y-%m-%d'

    def __init__(self, ref_date, nodes={}):
        self.ref_date = datetime.strptime(ref_date, self.FORMAT).date()
        self.nodes = self._normalize(nodes)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.ref_date}', {self.nodes})"

    def __getitem__(self, key):
        return self.nodes[key]

    def _normalize(self, nodes):
        return {str(k).upper(): float(v) for k, v in nodes.items()}
