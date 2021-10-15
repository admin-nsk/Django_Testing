import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

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

        #Саша видит, что заголовок и шапка страницы говорят о списках
        #неотложных дел
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #Ему сразу предлагается ввести элемент списка дел
        inputbox = self.browser.find_element_by_id('id_new_time')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')

        #Он набирает в текстовом поле "Починить замок"
        inputbox.send_keys('Починить замок')

        #Когда он нажимает Enter страница обновляется, и теперь страница
        #содержит "1: Почнить замок" в качестве элемента списка
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_element_by_tag_name('tr')
        self.assertTrue(any(rows.text == '1: Починить дверь' for row in rows))

        #Текстовое поле по-прежнему приглашает его добавить еще один элемент
        #Он вводит "Написать тесты"
        self.fail('Закончить тест')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
