from rest_framework import serializers
from .models import *


class UsersinfoSerializers(serializers.ModelSerializer):

    class Meta:
        model = Usersinfo
        fields = ['no', 'cards']
        depth = 2
