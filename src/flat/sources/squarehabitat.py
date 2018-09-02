'''
Created on 31 aout 2018

@author: tuco
'''
import re
import urllib2

from bs4 import BeautifulSoup

from flat.configuration.sources import get_source_options
from flat.sources import JsRestSource

REFERENCE_REGEX = r'Ref. : (.*)$'


class SquareHabitat(JsRestSource):

    def __init__(self, name, *args, **kargs):
        super(SquareHabitat, self).__init__(name, kargs['browser'])

        self.typeAnnonce = get_source_options(self.name).get('type-annonce', None)
        self.typeBien = get_source_options(self.name).get('type-bien', None)
        self.location = get_source_options(self.name).get('location', None)
        self.budgetMax = get_source_options(self.name).get_float('budget-max', None)
        self.surfaceMin = get_source_options(self.name).get_float('surface-min', None)

    def init_page(self, url):
        super(SquareHabitat, self).init_page(url)
        # Fill form

        # Type annonce
        if self.typeAnnonce:
            self.browser.find_element_by_id("cphTop_lstTypeAnnonce-mask").click()
            for a in self.browser.find_element_by_id("cphTop_lstTypeAnnonce-mask").find_elements_by_tag_name('a'):
                if a.text == self.typeAnnonce:
                    self.browser.execute_script("arguments[0].click();", a)
                    break
        # Type bien
        if self.typeBien:
            self.browser.find_element_by_id("cphTop_lstTypeBien-mask").click()
            for a in self.browser.find_element_by_id("cphTop_lstTypeBien-mask").find_elements_by_tag_name('a'):
                if a.text == self.typeBien:
                    self.browser.execute_script("arguments[0].click();", a)
                    break
        # Location
        if self.location:
            self.browser.execute_script("document.getElementById('search_id').value='%s';" % self.location)
        # Budget
        if self.budgetMax:
            self.browser.find_element_by_name("ctl00$cphTop$txtBudgetMax").send_keys(str(self.budgetMax))
        # Surface
        if self.surfaceMin:
            self.browser.find_element_by_name("ctl00$cphTop$txtSurfaceMin").send_keys(str(self.surfaceMin))

        # Launch search
        launch_btn = self.browser.find_element_by_id("cphTop_lnkDemarrer")
        launch_btn.click()

    def get_annonces(self):
        for _ in self.soup.find('div', attrs={'class': 'row blocs-biens'}).find_all('a', attrs={'class': 'lien-bien'}):
            article_url = '%s%s' % (
                self.domain,
                _.get('href')
            )
            # Load article to find reference
            article_soup = BeautifulSoup(urllib2.urlopen(article_url).read(), 'html.parser')
            article_description = article_soup.find('div', attrs={"class": "description-bien"}).find_all('div')[0].find('p').get_text()
            reference_search = re.search(REFERENCE_REGEX, article_description, re.IGNORECASE)

            if reference_search:
                article_reference = reference_search.group(1)

                yield (
                    article_reference,
                    article_url
                )

    def has_next_page(self):
        return len(self.browser.find_element_by_class_name("pagination").find_elements_by_tag_name('li')[self.page + 1].find_elements_by_tag_name('span')) == 0

    def go_to_next_page(self):
        # Remove cookie bar
        self.browser.execute_script('$("#cookie-bar").remove()')
        self.browser.find_element_by_class_name("pagination").find_elements_by_tag_name('li')[self.page + 1].find_elements_by_tag_name('a')[0].click()
