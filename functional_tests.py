import os

from selenium import webdriver
import unittest

browser = webdriver.Firefox()

class NewVistorTest(unittest.TestCase):
    ''' Тест нового посетителя'''

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()
        self.browser.close()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        self.fail('Закончить тест!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
