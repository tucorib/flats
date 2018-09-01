'''
Created on 31 aout 2018

@author: tuco
'''

import re

from flat.configuration.sources import get_source_options
from flat.sources import JsRestSource

REFERENCE_REGEX = r'container-bien-(.*)$'


class Citya(JsRestSource):

    def __init__(self, name):
        super(Citya, self).__init__(name)

        self.locations = get_source_options(self.name).get('locations', None)

    def get_annonces(self):
        for _ in self.soup.find('div', attrs={'id': 'listing-biens'}).find_all('div', attrs={'class': 'col-sm-6'}):
            parseIt = True
            if self.locations:
                parseIt = parseIt and _.find('p', attrs={'class': 'truncate'}).get_text() in self.locations
            if parseIt:
                reference_search = re.search(REFERENCE_REGEX, _.find('div', attrs={'class': 'container-aper'}).get('id'), re.IGNORECASE)

                if reference_search:
                    yield (
                        reference_search.group(1),
                        _.find('a').get('href')
                    )

    def has_next_page(self):
        return False
