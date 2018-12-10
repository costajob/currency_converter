from html import escape
from json import dumps
from urllib.parse import parse_qs
from cconv import data, currency, converter
from cconv.logger import BASE as logger


class Converter:
    """
    Synopsis
    ========
    A plain WSGI compliant HTTP server aimed to be wrapped by Meinheld and executed
    via Gunicorn.
    """

    class RefDateError(KeyError):
        """
        This error is raised for invalid reference date.
        """

    PATH = '/convert'
    CACHE = data.Cache()
    TREE = data.Fetcher()()
    NODES = data.Parser(TREE)()
    DATES = list(NODES.keys())
    DEFAULTS = (['9.99'], ['EUR'], ['USD'], [''])

    def __init__(self, env, res):
        self.env = env
        self.res = res
        self.status = '200 OK' 
        self.body = self._body()
        self.headers = self._headers()

    def __iter__(self):
        if self._matches():
            self.res(self.status, self.headers)
            yield self.body

    def _body(self):
        try:
            amt, src, dest, ref = self._params()
            ref = ref or self.DATES[0]
            rates = self.CACHE.get(ref, self._rates)
            money = currency.Money(src, amt)
            comp = converter.Computer(money, dest, rates)
            return dumps(comp()).encode()
        except (self.RefDateError, converter.Computer.CurrencyError) as e:
            self.status = '422 Unprocessable Entity'
            logger.error(e)
            return dumps(self._error(e)).encode()
    
    def _headers(self):
        return [('Content-type', 'text/json'), ('Content-Length', str(len(self.body)))]

    def _matches(self):
        return self.env['PATH_INFO'] == self.PATH

    def _params(self):
        params = parse_qs(self.env.get('QUERY_STRING')) or {}
        amt = params.get('amount', self.DEFAULTS[0])[0]
        src = params.get('src_currency', self.DEFAULTS[1])[0]
        dest = params.get('dest_currency', self.DEFAULTS[2])[0]
        ref = params.get('reference_date', self.DEFAULTS[3])[0]
        return (escape(q) for q in (amt, src, dest, ref))

    def _rates(self, ref):
        try:
            return currency.EurRates(ref, self.NODES[ref])
        except KeyError as e:
            logger.error(e)
            raise self.RefDateError(f'invalid reference date, use one of these: {", ".join(self.DATES)}')

    def _error(self, e):
        msg, data = str(e).split(': ')
        return {msg[1:]: data[:-1]}
