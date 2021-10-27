from django.shortcuts import render, redirect
from lists.models import Item


def home_page(request):
    '''Домашняя страница'''
    return render(request, 'home.html')


def view_list(request):
    '''представление списка'''

    items = Item.objects.all()
    return render(request, 'list.html', {'tasks': items})


def new_list(request):
    '''создание нового списка'''
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/alone-list-in-the-world/')