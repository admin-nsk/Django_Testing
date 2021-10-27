from django.shortcuts import render, redirect
from lists.models import Item


def home_page(request):
    '''Домашняя страница'''
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        return redirect('/lists/alone-list-in-the-world/')

    return render(request, 'home.html')


def view_list(request):
    '''представление списка'''

    items = Item.objects.all()
    return render(request, 'list.html', {'tasks': items})
