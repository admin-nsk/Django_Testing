from django.shortcuts import render
from lists.models import Item


def home_page(request):
    '''Домашняя страница'''
    item = Item()
    item.text = request.POST.get('item_text', '')
    item.save()
    items = Item.objects.all()
    return render(request, 'home.html', {'tasks': items})