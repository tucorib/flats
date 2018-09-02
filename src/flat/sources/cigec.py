# -*- coding: utf-8 -*
'''
Created on 31 aout 2018

@author: tuco
'''
from selenium.webdriver.support.select import Select

from flat.configuration.sources import get_source_options
from flat.sources import JsRestSource

REFERENCE_REGEX = r'Ref. : (.*)$'


class Cigec(JsRestSource):

    def __init__(self, name, *args, **kargs):
        super(Cigec, self).__init__(name, kargs['browser'])

        self.typeBien = get_source_options(self.name).get('type-bien', [])
        self.nbPieces = get_source_options(self.name).get('nb-pieces', [])
        self.budgetMax = get_source_options(self.name).get('budget-max', None)
        self.location = get_source_options(self.name).get('location', None)

    def init_page(self, url):
        super(Cigec, self).init_page(url)
        # Fill form
        form = self.browser.find_element_by_id("CPHContenu_ctl00_RepLignes_RepColonnes_0_Filtres_0_Panlocation_0")
        # Type bien
        if self.typeBien:
            if "Appartement" not in self.typeBien:
                form.find_elements_by_id('CPHContenu_ctl00_RepLignes_RepColonnes_0_Filtres_0_RepCategories_0_CheCategorie_0').click()
            if "Maison" not in self.typeBien:
                form.find_elements_by_id('CPHContenu_ctl00_RepLignes_RepColonnes_0_Filtres_0_RepCategories_0_CheCategorie_1').click()

        # Nb pieces
        if self.nbPieces:
            if u"1 pièce" not in self.typeBien:
                form.find_element_by_id('CPHContenu_ctl00_RepLignes_RepColonnes_0_Filtres_0_ChePiece1_0').click()
            if u"2 pièces" not in self.typeBien:
                form.find_element_by_id('CPHContenu_ctl00_RepLignes_RepColonnes_0_Filtres_0_ChePiece2_0').click()
            if u"3 pièces" not in self.typeBien:
                form.find_element_by_id('CPHContenu_ctl00_RepLignes_RepColonnes_0_Filtres_0_ChePiece3_0').click()
            if u"4 pièces" not in self.typeBien:
                form.find_element_by_id('CPHContenu_ctl00_RepLignes_RepColonnes_0_Filtres_0_ChePiece4_0').click()
            if u"5 pièces et +" not in self.typeBien:
                form.find_element_by_id('CPHContenu_ctl00_RepLignes_RepColonnes_0_Filtres_0_ChePiece5_0').click()
        # Budget max
        if self.budgetMax:
            a = self.browser.find_element_by_id("slider-range3").find_elements_by_tag_name('a')[1]
            self.browser.execute_script("arguments[0].style.left = '%s%%';" % self.budgetMax, a)
        # Location
        if self.location:
            select = Select(self.browser.find_element_by_id("CPHContenu_ctl00_RepLignes_RepColonnes_0_Filtres_0_LstSecteurs_0"))
            select.select_by_visible_text(self.location)

        # Launch search
        launch_btn = self.browser.find_element_by_id("CPHContenu_ctl00_RepLignes_RepColonnes_0_Filtres_0_BouRechercher_0")
        self.browser.execute_script("arguments[0].click();", launch_btn)

    def get_annonces(self):
        for _ in self.soup.find_all('div', attrs={'class': 'Article'}):
            article_url = '%s%s' % (
                self.domain,
                _.find_all('span', attrs={'class': 'Bouton'})[1].find('a').get('href')
            )
            yield (
                article_url,
                article_url
            )

    def has_next_page(self):
        return self.soup.find('a', attrs={'id': "CPHContenu_Catalogue_PagArticles_BouSuivant", 'class': 'Desactive'}) is None

    def go_to_next_page(self):
        self.browser.execute_script("arguments[0].click();", self.browser.find_element_by_id("CPHContenu_Catalogue_PagArticles_BouSuivant"))
