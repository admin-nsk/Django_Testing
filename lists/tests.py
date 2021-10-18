from lists.models import Item
from django.test import TestCase


class HomePageTest(TestCase):
    '''Тест домашней страницы'''

    def test_uses_home_page_template(self):
        '''тест: используется домашний шаблон'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        '''тест: можно сохранить post-запрос'''
        text = 'A new list item'
        response = self.client.post('/', data={'item_text': text})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.object.first()
        self.assertEqual(new_item.text(), text)
        self.assertIn(text, response.content.decode())
        self.assertTemplateUsed(response, 'home.html')


class ItemModelTest(TestCase):
    '''Тест модели элемента списка'''

    def test_saving_and_retrieving_items(self):
        '''тест сохранения и получения элемента списка'''
        first_text = 'The first (ever) list item'
        second_text = 'Item the second'
        first_item = Item()
        first_item.text = first_text
        first_item.save()

        second_item = Item()
        second_item.text = second_text
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[0]
        self.assertEqual(first_saved_item.text(), first_text)
        self.assertEqual(second_saved_item.text(), second_text)


