'''
Created on 31 aout 2018

@author: tuco
'''

from flat.configuration.sources import get_source_options
from flat.sources import RestSource


class Foncia(RestSource):

    def __init__(self, name):
        super(Foncia, self).__init__(name)

        self.locations = get_source_options(self.name).get('locations', None)

    def get_annonces(self):
        for _ in self.soup.find_all('article', attrs={'class': 'TeaserOffer'}):
            parseIt = True
            if self.locations:
                parseIt = parseIt and _.find('p', attrs={"class": "TeaserOffer-loc"}).get_text() in self.locations
            if parseIt:
                for span in _.find_all('span'):
                    if span.has_attr('data-reference'):
                        yield (
                            span.get('data-reference'),
                            '%s%s' % (
                                self.domain,
                                _.find('h3', attrs={"class": "TeaserOffer-title"}).find('a').get('href')
                            )
                        )
                    break

    def has_next_page(self):
        return self.soup.find('div', attrs={"class": "Pagination Pagination--more"}).find('a', text="Suivante >") is not None

    def get_next_url(self):
        return '%s%s' % (
            self.domain,
            self.soup.find('div', attrs={"class": "Pagination Pagination--more"}).find('a', text="Suivante >").get('href')
        )
