'''
Created on 31 aout 2018

@author: tuco
'''

from flat.sources import RestSource


class Adl(RestSource):

    def __init__(self, name, *args, **kargs):
        super(Adl, self).__init__(name)

    def get_annonces(self):
        for _ in self.soup.find_all('div', attrs={'class': 'item'}):
            yield (
                _.get('data-id'),
                _.find('a').get('href')
            )

    def has_next_page(self):
        return self.soup.find('a', attrs={"data-page": self.page + 1}) is not None

    def get_next_url(self):
        return self.soup.find('a', attrs={"data-page": self.page + 1}).get('href')
