from html import escape
from json import dumps
from urllib.parse import parse_qs
from cconv import data, currency, converter
from cconv.logger import BASE as logger


# Declare CPU/RAM intensive objects at start
CACHE = data.Cache()
TREE = data.Fetcher()()
NODES = data.Parser(TREE)()
DATES = list(NODES.keys())


def convert(environ, start_response):
    if environ['PATH_INFO'] != '/convert':
        start_response('404 Not Found', [])
        return []
    amt, src, dest, ref = _query(environ)
    try:
        rates = CACHE.fetch(ref, _rates)
        money = currency.Money(src, amt)
        comp = converter.Computer(money, dest, rates)
        res = dumps(comp()).encode()
    except KeyError as e:
        logger.error(e)
        res = str(e).encode()
    response_headers = [('Content-type', 'text/json'), ('Content-Length', str(len(res)))]
    start_response('200 OK', response_headers)
    return [res]


def _query(environ):
    query = parse_qs(environ.get('QUERY_STRING')) or {}
    amt = query.get('amount', ['9.99'])[0]
    src = query.get('src_currency', ['EUR'])[0]
    dest = query.get('dest_currency', ['USD'])[0]
    ref = query.get('reference_date', [''])[0]
    return [escape(q) for q in (amt, src, dest, ref)]


def _rates(ref):
    try:
        ref = ref or DATES[0]
        return currency.EurRates(ref, NODES[ref])
    except KeyError as e:
        logger.error(e)
        raise KeyError(f'unavailable reference date, use one of these: {", ".join(DATES)}')
