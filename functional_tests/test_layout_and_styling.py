from selenium.webdriver.common.keys import Keys
import unittest

from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):
    '''тест макета и стилевого оформления'''

    def test_layout_and_styling(self):
        '''тест макета и стилевого оформления'''
        # Саша открывает домашнюю страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1023, 768)

        # Он замечает, что поле ввода аккуратно центиовано
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # Она начинает новый список и видит, что поле ввода там тоже
        # аккуратно центировано
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )



if __name__ == '__main__':
    unittest.main(warnings='ignore')
