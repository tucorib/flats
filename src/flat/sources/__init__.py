from pydoc import locate
import itertools
import urllib2

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from flat.configuration.sources import get_source_class, get_source_options


class Source(object):

    def __init__(self, name):
        self.name = name

    def open(self):
        pass

    def parse(self):
        pass

    def close(self):
        pass


def build_source(source):
    return locate(get_source_class(source))(source)


def xpath_soup(element):
    """
    Generate xpath of soup element
    :param element: bs4 text or node
    :return: xpath as string
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        """
        @type parent: bs4.element.Tag
        """
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


class RestSource(Source):

    def __init__(self, name):
        super(RestSource, self).__init__(name)
        self.domain = get_source_options(self.name).get('domain', None)
        self.urls = [
            "%s%s" % (
                self.domain,
                _)
            for _ in get_source_options(self.name).get('urls', [])
        ]

    def get_annonces(self):
        pass

    def parse(self):
        for url in self.urls:
            self.page = 1
            for _ in self.parse_url(url):
                yield _

    def parse_url(self, url):
        self.load(url)
        for _ in self.get_annonces():
            yield _

        # Next page
        if self.has_next_page():
            next_url = self.get_next_url()
            self.page += 1
            for _ in self.parse_url(next_url):
                yield _

    def load(self, url):
        req = urllib2.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'fr-FR,fr;q=0.8',
            'Connection': 'keep-alive'
        })
        self.soup = BeautifulSoup(urllib2.urlopen(req).read(), 'html.parser')

    def has_next_page(self):
        pass

    def get_next_url(self):
        pass


class JsRestSource(RestSource):

    def __init__(self, name):
        super(JsRestSource, self).__init__(name)

    def open(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        self.browser = webdriver.Firefox(firefox_options=firefox_options)

    def load(self, url):
        self.browser.get(url)
        self.soup = BeautifulSoup(self.browser.page_source, 'html.parser')

    def close(self):
        self.browser.close()
