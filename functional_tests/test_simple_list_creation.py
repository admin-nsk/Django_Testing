from unittest import skip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

from .base import FunctionalTest


class NewVistorTest(FunctionalTest):
    ''' Тест нового посетителя'''

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)

        # Саша видит, что заголовок и шапка страницы говорят о списках
        # неотложных дел
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ему сразу предлагается ввести элемент списка дел
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')

        # Он набирает в текстовом поле "Починить замок"
        inputbox.send_keys('Починить дверь')

        # Когда он нажимает Enter страница обновляется, и теперь страница
        # содержит "1: Почнить замок" в качестве элемента списка
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Починить дверь')

        # Текстовое поле по-прежнему приглашает его добавить еще один элемент
        # Он вводит "Написать тесты"
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')
        inputbox.send_keys('Написать тесты')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Починить дверь')
        self.wait_for_row_in_list_table('2: Написать тесты')

    def test_multiple_users_can_start_list_at_different_urls(self):
        '''тест: многочисленные пользователи могут начать списки по разным url'''
        # Саша начинает новый список
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Заказать пиццу')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Заказать пиццу')

        # Он замечает, что его список имеет новый URL
        sasha_list_url = self.browser.current_url
        self.assertRegex(sasha_list_url, '/lists/.+')

        # Теперь новый пользователь, Фрэнсис, приходит на сайт.
        ## Мы используем новый сеанс браузера, тем самым обеспечивая, чтобы никакая
        ## информация от Эдит не прошла через данные cookie и пр.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Фрэнсис посещает домашнюю страницу. Нет никаких признаков списка Эдит
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertNotIn('Сделать мушку', page_text)

        # Фрэнсис начинает новый список, вводя новый элемент. Он менее
        # интересен, чем список Эдит...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить молоко')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        # Фрэнсис получает уникальный URL-адрес
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, sasha_list_url)

        # Опять-таки, нет ни следа от списка Эдит
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Купить молоко', page_text)
        # Удовлетворенные, они оба ложатся спать


if __name__ == '__main__':
    unittest.main(warnings='ignore')
