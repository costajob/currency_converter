from os import path
from urllib.parse import urlparse
from urllib.request import urlopen
from xml.etree import ElementTree


class Fetcher:
    """
    Synopsis
    ========
    Parse the specified XML source locally if present. If it is not,
    tries to fetch it remotely from the specified URL. 
    Returns a raw ElementTree object to be properly wrapped.

    Examples
    ========
    >>> fetcher = Fetcher('cconv/tests/stubs.xml')
    >>> fetcher().__class__
    <class 'xml.etree.ElementTree.ElementTree'>
    """

    XML = 'cconv/data/rates.xml'
    URL = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml'

    def __init__(self, doc=XML, url=URL):
        self.doc = path.abspath(doc)
        self.url = urlparse(url).geturl()

    def __call__(self):
        if not path.exists(self.doc):
            with urlopen(self.url) as remote, open(self.doc, 'wb') as local:
                local.write(remote.read())
        with open(self.doc) as doc:
            return ElementTree.parse(doc)


class Document:
    """
    Synopsis
    ========
    Receive an XML ElementTree object cntaining the exchange rates in EUR and
    returns a nested dict of useful data.
    Check 'cconv/data/rates.xml' for an example.

    Examples
    ========
    >>> tree = ElementTree.parse('cconv/tests/stubs.xml')
    >>> doc = Document(tree)
    >>> doc()
    {'2018-11-26': {'USD': '1.1363', 'ZAR': '15.7322'}, '2018-08-29': {'USD': '1.166', 'ZAR': '16.8176'}}
    """

    XMLNS = '{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}'
    NAME = 'Cube'

    def __init__(self, tree):
        self.tree = tree
        self.nodes = {}

    def __call__(self):
        if self.nodes:
            return self.nodes
        for node in self.tree.iter(f'{self.XMLNS}{self.NAME}'):
            if 'time' in node.attrib:
                time = node.get('time')
                self.nodes[time] = {}
            if self._is_rate(node.attrib):
                currency = node.get('currency')
                rate = node.get('rate')
                self.nodes[time][currency] = rate
        return self.nodes

    def _is_rate(self, node):
        return 'currency' in node and 'rate' in node
