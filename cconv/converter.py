from decimal import Decimal

class Computer:
    """
    Synopsis
    ========
    Accepts a money-like object (a tuple of currency-amount), an ISO destination currency 
    and an EUR rates object (a dict) and computes the appropriate conversion.

    Examples
    ========
    >>> comp = Computer(('USD', 10.0), 'CHF')
    >>> comp({'USD': 1.1352, 'CHF': 1.1316})
    {'amount': 9.97, 'currency': 'CHF'}
    """

    def __init__(self, money, dest='EUR'):
        self.src, self.amount =  money
        self.dest = str(dest).upper()

    def __call__(self, rates):
        ratio = rates[self.dest] / rates[self.src]
        conversion = ratio * self.amount
        return {'amount': float(f'{conversion:.2f}'), 'currency': self.dest}
