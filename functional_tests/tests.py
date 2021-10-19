from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVistorTest(LiveServerTestCase):
    ''' Тест нового посетителя'''

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        '''подтверждение строки в таблице списка'''
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)

        #Саша видит, что заголовок и шапка страницы говорят о списках
        #неотложных дел
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #Ему сразу предлагается ввести элемент списка дел
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')

        #Он набирает в текстовом поле "Починить замок"
        inputbox.send_keys('Починить дверь')

        #Когда он нажимает Enter страница обновляется, и теперь страница
        #содержит "1: Почнить замок" в качестве элемента списка
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table('1: Починить дверь')

        #Текстовое поле по-прежнему приглашает его добавить еще один элемент
        #Он вводит "Написать тесты"
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')
        inputbox.send_keys('Написать тесты')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table('1: Починить дверь')
        self.check_for_row_in_list_table('2: Написать тесты')


        self.fail('Закончить тест')


if __name__ == '__main__':
    unittest.main(warnings='ignore')