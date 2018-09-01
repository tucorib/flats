'''
Created on 31 aout 2018

@author: tuco
'''
from flat.sources import RestSource


class BonCoin(RestSource):

    def __init__(self, name):
        super(BonCoin, self).__init__(name)

    def get_annonces(self):
        for _ in self.soup.find_all('li', attrs={"itemtype": "http://schema.org/Offer"}):
            yield (
                _.find('a', attrs={"class": "clearfix trackable"}).get('href'),
                _.find('a', attrs={"class": "clearfix trackable"}).get('href')
            )

    def has_next_page(self):
        for _ in self.soup.find_all('a', attrs={"class": "_1f-eo"}):
            if _.find('span', attrs={'name': 'chevronRight'}):
                return True

    def go_to_next_page(self):
        for _ in self.soup.find_all('a', attrs={"class": "_1f-eo"}):
            if _.find('span', attrs={'name': 'chevronRight'}):
                self.url = '%s%s' % (self.domain, _.get('href'))
