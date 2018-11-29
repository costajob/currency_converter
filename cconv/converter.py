from cconv.logger import BASE as logger

class Computer:
    """
    Synopsis
    ========
    Accepts a money-like object (a tuple of currency-amount), an ISO destination currency 
    and an EUR rates object (a dict) and computes the appropriate conversion.

    Examples
    ========
    >>> comp = Computer(('USD', 10.0), 'CHF', {'USD': 1.1352, 'CHF': 1.1316})
    >>> comp()
    {'amount': 9.97, 'currency': 'CHF'}
    """

    class CurrencyError(KeyError):
        """
        This error is raised for invalid currency ISO code.
        """

    DEFAULT = 'EUR'

    def __init__(self, money, dest, rates):
        self.src, self.amount =  money
        self.dest = str(dest).upper()
        self.rates = rates

    @property
    def ratio(self):
        try:
            if self.src == self.dest:
                return 1
            elif self.src == self.DEFAULT:
                return 1 / self.rates[self.dest]
            elif self.dest == self.DEFAULT:
                return self.rates[self.src]
            else:
                return self.rates[self.src] / self.rates[self.dest]
        except KeyError as e:
            logger.error(e)
            raise self.CurrencyError(f'invalid currency, use one of these: {self.DEFAULT}, {", ".join(self.rates.keys())}')

    def __call__(self):
        conversion = self.amount / self.ratio
        return {'amount': float(f'{conversion:.2f}'), 'currency': self.dest}
