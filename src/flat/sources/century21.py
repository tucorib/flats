'''
Created on 31 aout 2018

@author: tuco
'''
from flat.sources import RestSource


class Century21(RestSource):

    def __init__(self, name, *args, **kargs):
        super(Century21, self).__init__(name)

    def get_annonces(self):
        for _ in self.soup.find('ul', attrs={'class': 'annoncesListeBien'}).find_all('li', attrs={'class': 'annonce'}):
            yield (
                _.find('div', attrs={'class': 'contentAnnonce'}).get('data-uid'),
                '%s%s' % (self.domain, _.find('a').get('href'))
            )

    def has_next_page(self):
        return self.soup.find('li', attrs={"class": "btnSUIV_PREC suivant"}) is not None

    def get_next_url(self):
        return '%s%s' % (
            self.domain,
            self.soup.find('li', attrs={"class": "btnSUIV_PREC suivant"}).find('a').get('href')
        )
