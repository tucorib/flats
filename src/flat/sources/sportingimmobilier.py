'''
Created on 31 aout 2018

@author: tuco
'''
from flat.configuration.sources import get_source_options
from flat.sources import RestSource


class SportingImmobilier(RestSource):

    def __init__(self, name):
        super(SportingImmobilier, self).__init__(name)

        self.surfaceMin = get_source_options(self.name).get_float('surface-min', None)
        self.locations = get_source_options(self.name).get('locations', None)

    def get_annonces(self):
        for _ in self.soup.find_all('div', attrs={'class': 'grid-lots-item'}):
            parseIt = True
            if self.surfaceMin:
                parseIt = parseIt and float(_.find('p', attrs={'class': 'lot-surface'}).find(text=True)) >= self.surfaceMin
            if self.locations:
                parseIt = parseIt and _.find('p', attrs={'class': 'lot-localisation'}).get_text() in self.locations
            if parseIt:
                yield (
                    _.element.get('id'),
                    '%s%s' % (self.domain, _.find('a').get('href'))
                )

    def has_next_page(self):
        return self.soup.find('div', attrs={"class": "post-next"}).find('a') is not None

    def go_to_next_page(self):
        self.url = self.soup.find('div', attrs={"class": "post-next"}).find('a').get('href')
