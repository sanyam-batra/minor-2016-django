from django import forms
from .models import *

class CardsForm(forms.ModelForm):

    class Meta:
        model = CardsAttach
        fields = '__all__'


class PostBoxForm(forms.Form):
    card_id = forms.CharField()
    com_text = forms.CharField(required=False, widget=forms.Textarea)
    photo = forms.FileField(required=False)
    attach = forms.FileField(required=False)


