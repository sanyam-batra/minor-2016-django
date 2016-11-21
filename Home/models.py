from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from Cards.models import *
from Boards.models import *

# sanyam1996---superuser password
# sanyam-----superuser username


class Usersinfo(models.Model):
    no = models.ForeignKey(User, on_delete=models.CASCADE)
    pic = models.FileField()
    cards = models.ManyToManyField(Cards, related_name='cards')
    boards = models.ManyToManyField(Boards, related_name='boards')

    def __str__(self):
        return str(self.no)


