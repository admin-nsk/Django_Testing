import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import unittest
import time

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    '''Функциональный тест'''

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        testing_server = os.environ.get('TESTING_SERVER')
        if testing_server:
            self.live_server_url = 'http://' + testing_server

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        '''ожидать строку в таблице списка'''
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id("id_list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as ex:
                if time.time() - start_time > MAX_WAIT:
                    raise ex
                time.sleep(1)

    def wait_for(self, fn):
        '''ожидать'''
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as ex:
                if time.time() - start_time > MAX_WAIT:
                    raise ex
                time.sleep(0.5)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
