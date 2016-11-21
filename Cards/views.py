from django.shortcuts import render , render_to_response,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import *
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from .forms import *
from django.views.generic.edit import CreateView,DeleteView
import json
from Home.serializers import UsersinfoSerializers
from django.core.files.uploadedfile import TemporaryUploadedFile
from Home.models import *
import random
import string
# Create your views here.


def CardsProjects_All(request):

    if request.user.is_authenticated():
        current_user = Usersinfo.objects.get(no=request.user.pk)
        cards = current_user.cards.all().order_by('-card_date')[:2]

        if not cards:
            flag = 0
        else:
            flag = 1

        if request.method == "POST":
            title = request.POST.get('textbox')
            desc = request.POST.get('descp')
            datanew = Data()
            datanew.type = 0
            datanew.data = str(title)
            datanew.save()
            datanew1 = Data()
            datanew1.type = 6
            datanew1.data = str(desc)
            datanew1.save()
            cardnew1 = Cards()
            cardnew1.save()
            cardnew1.database.add(datanew)
            cardnew1.database.add(datanew1)
            cardnew1.card_date = datetime.now()
            cardnew1.key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
            cardnew1.change = 0
            cardnew1.save()
            ob = Card_id()
            ob.key = cardnew1.key
            ob.change = cardnew1.change
            ob.save()
            flag = 1
            card_title = Cards_title()
            card_title.c_key = ob
            card_title.name = str(title)
            card_title.save()
            current_user = Usersinfo.objects.get(no=request.user.pk)
            current_user.cards.add(cardnew1)
            current_user.save()
            cards = current_user.cards.all().order_by('-card_date')[:2]

        return render(request, 'Cards/HomePage.html' , {'cards' : cards, 'flag':flag})
    else:
        return redirect('Home:login')


def Show_cards(request):
    if request.user.is_authenticated():
        current_user = Usersinfo.objects.get(no=request.user.pk)
        cards = current_user.cards.all().order_by('-card_date')
        return render(request, 'Cards/show_cards.html', {'cards': cards})
    else:
        return redirect('Home:login')


def Add_Checklist(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            title = request.POST.get('titlebox')
            card_id = request.POST.get('card_id')
            checklist = Checklist()
            checklist.title = title
            checklist.list_date = datetime.now()
            checklist.save()
            items = ChecklistItems()
            items.Check_title = checklist
            items.save()
            datanew = Data()
            datanew.type = 3
            datanew.save()
            datanew.checklist.add(items)
            datanew.save()
            card = Cards.objects.get(pk=card_id)
            card.database.add(datanew)
            card.save()

            '''if 'save_list_item' in request.POST:
                out = 0
                which_list = request.POST.get('checkneed')
                item_name = request.POST.get('attr')
                data = Data.objects.all()
                checklist_main = Checklist.objects.get(title=which_list)
                for x in data:
                    for z in x.checklist.all():
                        if z.Check_title == checklist_main:
                            out = 1
                            break
                    if out == 1:
                        item_new = ChecklistItems()
                        item_new.item = item_name
                        item_new.Check_title = checklist_main
                        item_new.done = False
                        item_new.save()
                        x.checklist.add(item_new)
                        x.save()
                        break'''

            card = Cards.objects.get(pk=card_id)
            return render_to_response('Cards/checkbox_ajax.html', {'x': card})
        else:
            return redirect('Home:login')


def Add_Checklist_Item(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            out = 0
            which_list = request.POST.get('checkneed')
            item_name = request.POST.get('attrr')
            card_id = request.POST.get('card_id')
            data = Data.objects.all()
            checklist_main = Checklist.objects.get(title=which_list)
            for x in data:
                for z in x.checklist.all():
                    if z.Check_title == checklist_main:
                        out = 1
                        break
                if out == 1:
                    item_new = ChecklistItems()
                    item_new.item = item_name
                    item_new.Check_title = checklist_main
                    item_new.done = False
                    item_new.save()
                    x.checklist.add(item_new)
                    x.save()
                    break
            card = Cards.objects.get(pk=card_id)
            return render_to_response('Cards/checkbox_ajax.html', {'x': card})
        else:
            return redirect('Home:login')

def Store_post(request):
    if request.is_ajax():
        form = PostBoxForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            card_id = form.cleaned_data['card_id']
            if form.cleaned_data['com_text']:
                com = form.cleaned_data['com_text']
                datanew = Data()
                datanew.type = 1
                datanew.data = com
                datanew.save()
                card = Cards.objects.get(id=card_id)
                card.database.add(datanew)
                card.save()
            if request.FILES.get('upload_photo') is not None and request.FILES.get('upload_photo') is not "":
                card_attach = CardsAttach()
                card_attach.photo = request.FILES['upload_photo']
                card_attach.save()
                datanew = Data()
                datanew.type = 2
                datanew.data = str(card_attach.photo)
                datanew.save()
                card = Cards.objects.get(pk=card_id)
                card.database.add(datanew)
                card.save()
            if request.FILES.get('upload_attach') is not None and request.FILES.get('upload_attach') is not "":
                card_attach = CardsAttach()
                card_attach.photo = request.FILES['upload_attach']
                card_attach.save()
                datanew = Data()
                datanew.type = 5
                datanew.data = str(card_attach.photo)
                datanew.save()
                card = Cards.objects.get(pk=card_id)
                card.database.add(datanew)
                card.save()
            card = Cards.objects.get(id=card_id)
            return render_to_response('Cards/activity_ajax.html', {'x': card})



def Desc_post(request):
    if request.is_ajax():
        card_id = request.POST['cid']
        data_id = request.POST['did']
        about = request.POST['desc']
        datanew = Data.objects.get(pk=data_id)
        datanew.data = about
        datanew.save()
        card = Cards.objects.get(id=card_id)
        return render_to_response('Cards/desc_ajax.html', {'x': card})


@csrf_exempt
def add_item(request):
    if request.is_ajax():
        zkey = request.POST['zkeyval']
        fval = request.POST['val']
        x_key = request.POST['xkeyval']
        ob = ChecklistItems.objects.get(pk=zkey)
        if fval == "1":
            ob.done = 1
        else:
            ob.done = 0
        ob.save()
        card = Cards.objects.get(pk=x_key)
        return render_to_response('Cards/checkbox_ajax.html', {'x': card})


class DeleteCard(DeleteView):
    model = Cards
    success_url = reverse_lazy('cards:show_card')


'''JSON'''
class Cardlist(APIView):

    def get(self, request, key):
        u = User.objects.get(username=key)
        us = Usersinfo.objects.get(no=u.pk)
        cards = us.cards.all()
        serializer = CardsSerializers(cards, many=True)
        return Response(serializer.data)

    def post(self, request):
        x = json.dumps(request.data)
        data = json.loads(x)
        return HttpResponse(json.dumps(data))


class Statuslist(APIView):

    def get(self, request):
        status = Status.objects.all()
        serializer = StatusSerializers(status, many=True)
        return Response(serializer.data)

    def post(self):
        pass




