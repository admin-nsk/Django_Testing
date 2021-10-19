from django.shortcuts import render, redirect
from lists.models import Item


def home_page(request):
    '''Домашняя страница'''
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'home.html', {'tasks': items})