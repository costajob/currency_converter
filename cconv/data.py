from os import path
from urllib.parse import urlparse
from urllib.request import urlopen
from xml.etree import ElementTree
from cconv.logger import BASE as logger


class Fetcher:
    """
    Synopsis
    ========
    Parse the specified XML source locally if present. If it does not exist or 
    if the 'fresh' flag is True, tries to fetch it remotely from the 
    specified URL. 
    Returns a raw ElementTree object for further parsing.

    Examples
    ========
    >>> fetcher = Fetcher('cconv/tests/stubs.xml')
    >>> fetcher().__class__
    <class 'xml.etree.ElementTree.ElementTree'>
    """

    XML = 'cconv/data/rates.xml'
    URL = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml'

    def __init__(self, doc=XML, url=URL, fresh=False):
        self.doc = path.abspath(doc)
        self.url = urlparse(url).geturl()
        self.fresh = fresh

    def __call__(self):
        if not path.exists(self.doc) or self.fresh:
            logger.info('fetching data remotely by %s', self.url)
            with urlopen(self.url) as remote, open(self.doc, 'wb') as local:
                local.write(remote.read())
        with open(self.doc) as doc:
            return ElementTree.parse(doc)


class Parser:
    """
    Synopsis
    ========
    Receive an XML ElementTree object cntaining the exchange rates in EUR and
    returns a nested dict of useful data.
    Check 'cconv/data/rates.xml' for an example.

    Examples
    ========
    >>> tree = ElementTree.parse('cconv/tests/stubs.xml')
    >>> doc = Parser(tree)
    >>> doc()
    {'2018-11-26': {'USD': '1.1363', 'ZAR': '15.7322'}, '2018-08-29': {'USD': '1.166', 'ZAR': '16.8176'}}
    """

    XMLNS = '{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}'
    ROOT = 'Cube'
    TIME = 'time'
    CURRENCY = 'currency'
    RATE = 'rate'

    def __init__(self, tree):
        self.tree = tree
        self.nodes = {}

    def __call__(self):
        if self.nodes:
            return self.nodes
        for node in self.tree.iter(f'{self.XMLNS}{self.ROOT}'):
            if self.TIME in node.attrib:
                time = node.get(self.TIME)
                self.nodes[time] = {}
            if self._is_rate(node.attrib):
                currency = node.get(self.CURRENCY)
                rate = node.get(self.RATE)
                self.nodes[time][currency] = rate
        return self.nodes

    def _is_rate(self, node):
        return self.CURRENCY in node and self.RATE in node
