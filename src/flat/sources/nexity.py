'''
Created on 31 aout 2018

@author: tuco
'''
from flat.sources import JsRestSource, xpath_soup


class Nexity(JsRestSource):

    def __init__(self, name, *args, **kargs):
        super(Nexity, self).__init__(name, kargs['browser'])

    def get_annonces(self):
        for _ in self.soup.find_all('div', attrs={'class': 'item'}):
            yield (
                _.get('data-id'),
                '%s%s' % (self.domain, _.find('a', attrs={'class', 'offer-link'}).get('href'))
            )

    def has_next_page(self):
        return self.soup.find(
            'section',
            attrs={'id': 'pagination'}
        ).find(
            'a',
            attrs={"class": "pager-arrow", "data-page": self.page + 1}
        ) is not None

    def go_to_next_page(self):
        a = self.soup.find(
            'section',
            attrs={'id': 'pagination'}
        ).find(
            'a',
            attrs={"class": "pager-arrow", "data-page": self.page + 1}
        )
        xpath = xpath_soup(a)
        self.browser.find_element_by_xpath(xpath).click()
