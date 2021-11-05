from django.core.exceptions import ValidationError
from django.utils.html import escape

from lists.models import Item, List
from django.test import TestCase


class HomePageTest(TestCase):
    """Тест домашней страницы"""

    def test_uses_home_page_template(self):
        """тест: используется домашний шаблон"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):
    """тест представления списка"""

    def test_displays_all_items(self):
        """тест отображает все элементы списка"""
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
        """тест: испльзует шаблон списка"""
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_passes_correct_list_to_template(self):
        """тест: передается првильный шаблон списка"""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def  test_cannot_save_empty_list_items(self):
        """тест: нельзя добавлять пустые элементы"""
        list_ = List.objects.create()
        item = Item(list=list_, text="")
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()


class NewListTest(TestCase):
    """тест нового списка"""

    def test_can_save_a_POST_request(self):
        """тест: можно сохранить post-запрос"""
        text = 'A new list item'
        self.client.post('/lists/new', data={'item_text': text})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, text)

    def test_redirects_after_POST(self):
        """перенаправление по запросу"""
        text = 'A new list item'
        response = self.client.post('/lists/new', data={'item_text': text})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_validation_error_are_sent_back_to_home_page_template(self):
        """тест: ошибки валидации отсылаются назад в шаблон
            домашней страницы"""
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        print(response.content.decode())
        self.assertContains(response, expected_error)

    def test_invalid_list_item_arent_saved(self):
        """тест: сохраняются недопустимые элементы списка"""
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


class NewItemTest(TestCase):
    """тест нового элемента списка"""

    def test_can_save_a_POST_an_exiting_list(self):
        """тест: можно сохранить post-запрос в существующий списоок"""
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
        """тест: переадресуется в представленние списка"""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item an exiting list'}
        )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

