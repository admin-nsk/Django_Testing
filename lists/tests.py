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
        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)

        other_list = List.objects.create()
        first_text_other_list = "First element 2 list"
        second_text_other_list = "Second element 2 list"
        Item.objects.create(text=first_text_other_list, list=other_list)
        Item.objects.create(text=second_text_other_list, list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, first_text_other_list)
        self.assertNotContains(response, second_text_other_list)

    def test_uses_list_template(self):
        '''тест: испльзует шаблон списка'''
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_passes_correct_list_to_template(self):
        '''тест: передается првильный шаблон списка'''
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)



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
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

class NewItemTest(TestCase):
    '''тест нового элемента списка'''

    def test_can_save_a_POST_an_exiting_list(self):
        '''тест: можно сохранить post-запрос в существующий списоок'''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item an exiting list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item an exiting list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirect_to_list_view(self):
        '''тест: переадресуется в представленние списка'''
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item an exiting list'}
        )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

