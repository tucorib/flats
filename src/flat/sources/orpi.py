'''
Created on 31 aout 2018

@author: tuco
'''
from flat.configuration.sources import get_source_options
from flat.sources import JsRestSource, xpath_soup


class Orpi(JsRestSource):

    def __init__(self, name, *args, **kargs):
        super(Orpi, self).__init__(name, kargs['browser'])

        self.locations = get_source_options(self.name).get('locations', None)

    def get_annonces(self):
        for _ in self.soup.find('section', attrs={'class': 'resultLayout-estateList'}).find_all('li'):
            parseIt = True
            if self.locations:
                parseIt = parseIt and any(location in _.find('a').get('href') for location in self.locations)
            if parseIt:
                yield (
                    _.get('id'),
                    '%s%s' % (self.domain, _.find('a').get('href'))
                )

    def has_next_page(self):
        return self.soup.find('nav', attrs={"class": "paging"}).findChildren(recursive=False)[-1].name == 'a'

    def go_to_next_page(self):
        # Remove cookie bar
        self.browser.execute_script('if(document.getElementById("cookieconsent-banner")) document.getElementById("cookieconsent-banner").outerHTML = "";')

        xpath = xpath_soup(self.soup.find('nav', attrs={"class": "paging"}).findChildren(recursive=False)[-1])
        self.browser.find_element_by_xpath(xpath).click()
