from django.db import models
from django.db.models import CASCADE
from django.urls import reverse


class List(models.Model):
    '''Список'''

    def get_absolute_url(self):
        '''получить абсолютный url'''
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    '''элемент списка'''
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=CASCADE)
