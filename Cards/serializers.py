from rest_framework import serializers
from .models import *


class CardsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Cards
        fields = ['id', 'key', 'database']
        depth = 2


class StatusSerializers(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ['username', 'card_id']
        depth = 2