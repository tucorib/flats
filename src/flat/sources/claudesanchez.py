# -*- coding: utf-8 -*
'''
Created on 31 aout 2018

@author: tuco
'''
import re

from flat.sources import RestSource

REFERENCE_REGEX = r'Ref : (.*)$'


class ClaudeSanchez(RestSource):

    def __init__(self, name):
        super(ClaudeSanchez, self).__init__(name)

    def get_annonces(self):
        for _ in self.soup.find_all('div', attrs={'class': 'annonce'}):
            reference_search = re.search(REFERENCE_REGEX, _.find('span', attrs={'class': 'reference'}).get_text(), re.IGNORECASE)

            if reference_search:
                yield (
                    reference_search.group(1),
                    _.find('div', attrs={'class': 'pied-annonce'}).find_all('a')[0].get('href')
                )

    def has_next_page(self):
        for _ in self.soup.find_all('a', attrs={"class": "num_page"}):
            if _.find('img', attrs={'alt': 'page suivante'}):
                return True

    def go_to_next_page(self):
        for _ in self.soup.find_all('a', attrs={"class": "num_page"}):
            if _.find('img', attrs={'alt': 'page suivante'}):
                self.url = '%s%s' % (self.domain, _.get('href'))
                break
