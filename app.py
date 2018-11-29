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

    def __init__(self, env, res):
        self.env = env
        self.res = res
        self.body = self._body()
        self.headers = self._headers()

    def __iter__(self):
        if self._matches():
            self.res('200 OK', self.headers)
            yield self.body

    def _body(self):
        try:
            amt, src, dest, ref = self._params()
            ref = ref or self.DATES[0]
            rates = self.CACHE.fetch(ref, self._rates)
            money = currency.Money(src, amt)
            comp = converter.Computer(money, dest, rates)
            return dumps(comp()).encode()
        except (self.RefDateError, converter.Computer.CurrencyError) as e:
            logger.error(e)
            return str(e).encode()
    
    def _headers(self):
        return [('Content-type', 'text/json'), ('Content-Length', str(len(self.body)))]

    def _matches(self):
        return self.env['PATH_INFO'] == self.PATH

    def _params(self):
        params = parse_qs(self.env.get('QUERY_STRING')) or {}
        amt = params.get('amount', ['9.99'])[0]
        src = params.get('src_currency', ['EUR'])[0]
        dest = params.get('dest_currency', ['USD'])[0]
        ref = params.get('reference_date', [''])[0]
        return (escape(q) for q in (amt, src, dest, ref))

    def _rates(self, ref):
        try:
            return currency.EurRates(ref, self.NODES[ref])
        except KeyError as e:
            logger.error(e)
            raise self.RefDateError(f'invalid reference date, use one of these: {", ".join(self.DATES)}')
