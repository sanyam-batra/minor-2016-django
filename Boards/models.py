from django.db import models
from Cards.models import *
# Create your models here.


class ListofCards(models.Model):
    title = models.CharField(max_length=100)
    key = models.CharField(max_length=100)
    listofcards = models.ManyToManyField(Card_id, related_name='listcards')

    def __str__(self):
        return (self.title)


class Boards(models.Model):
    uuid = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    listInsideProjects = models.ManyToManyField(ListofCards, related_name='listinside')

    def __str__(self):
        return (self.title)

