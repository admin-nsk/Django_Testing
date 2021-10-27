from lists.models import Item, List
from django.test import TestCase


class HomePageTest(TestCase):
    '''Тест домашней страницы'''

    def test_uses_home_page_template(self):
        '''тест: используется домашний шаблон'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListAndItemModelTest(TestCase):
    '''Тест модели элемента списка'''

    def test_saving_and_retrieving_items(self):
        '''тест сохранения и получения элемента списка'''
        list_ = List()
        list_.save()

        first_text = 'The first (ever) list item'
        second_text = 'Item the second'
        first_item = Item()
        first_item.text = first_text
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = second_text
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, first_text)
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, second_text)
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):
    '''тест представления списка'''

    def test_displays_all_items(self):
        '''тест отображает все элементы списка'''
        list_ = List.objects.create()
        Item.objects.create(text="itemey 1", list=list_)
        Item.objects.create(text="itemey 2", list=list_)

        response = self.client.get('/lists/alone-list-in-the-world/')
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

    def test_uses_list_template(self):
        '''тест: испльзует шаблон списка'''
        response = self.client.get("/lists/alone-list-in-the-world/")
        self.assertTemplateUsed(response, "list.html")


class NewListTest(TestCase):
    '''тест нового списка'''

    def test_can_save_a_POST_request(self):
        '''тест: можно сохранить post-запрос'''
        text = 'A new list item'
        self.client.post('/lists/new', data={'item_text': text})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, text)

    def test_redirects_after_POST(self):
        '''перенаправление по запросу'''
        text = 'A new list item'
        response = self.client.post('/lists/new', data={'item_text': text})
        self.assertRedirects(response, '/lists/alone-list-in-the-world/')

