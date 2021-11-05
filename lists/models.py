from django.db import models
from django.db.models import CASCADE


class List(models.Model):
    '''Список'''
    pass


class Item(models.Model):
    '''элемент списка'''
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=CASCADE)
