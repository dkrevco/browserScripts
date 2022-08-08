import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import selenium.common.exceptions as selex
from selenium.webdriver.common.by import By
import datetime
import os
from selenium.webdriver.support.ui import Select
import random
import re



class Browser:

    def __init__(self):
        self.headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(f'user-agent={self.headers}')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.set_window_size(1920, 1080)

    def open_url(self, url: str = 'https://www.iport.ru/'):

        self.page = self.driver.get(url)
        time.sleep(random.randint(3, 6))



class BurgerChecker(Browser):

    def __init__(self):

        self.columns = ['href', 'HeadingCounter', 'Products on Page']
        self.pages_data = []

        super(BurgerChecker, self).__init__()


    def run(self):
        print('Start')
        self.open_url()
        self._get_links()
        self._filter_for_catalog()
        self._checker_pages()
        self._create_dataframe()
        self._save_to_file()

        # div.SubCategoryPanelstyles__SubCategoryPanel__LinkBlock-sc-5cku7y-2.keMytB > div > div > div > div > a

    def _get_links(self):

        self.links = self.driver.find_elements(By.TAG_NAME, 'a')
        self.links = [x.get_attribute('href') for x in self.links]
        self.links = list(filter(None, self.links))

        return self.links

    def _filter_for_catalog(self):

        self.catalog_pages = {x for x in self.links if x.find('/catalog') >= 0}

        return self.catalog_pages


    def _checker_pages(self):

        for link in self.catalog_pages:

            try:
                print(f'Opening {link}')
                self.open_url(link)
                self._find_header_counter()
                self._count_products()
                self.pages_data.append([link, self.counter, len(self.products)])
            except Exception as ex:
                print(ex)
                self.pages_data.append([link, str(ex), '-'])

    def _find_header_counter(self):

        self.counter = self.driver.find_element(By.CLASS_NAME, 'indexstyles__Catalog__ProductCount-sc-l92pc1-1.bqcbnp')
        self.counter = self.counter.text.split('- ')[1]

        return self.counter

    def _count_products(self):

        self.products = self.driver.find_elements(By.CLASS_NAME, 'CatalogGridstyles__CatalogGrid__Item-sc-bla7rq-2.hNLNBZ')

        return self.products

    def _create_dataframe(self):

        self.dataframe = pd.DataFrame(self.pages_data, columns=self.columns)

        return self.dataframe

    def _save_to_file(self):

        self.dataframe.to_csv(f'catalog_check.csv')



def main():

    bc = BurgerChecker()

    bc.run()


if __name__ == '__main__':

    main()