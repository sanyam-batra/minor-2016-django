import random
import string
from django.shortcuts import render,redirect,HttpResponse
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import *
from Home.models import *
from Cards.models import *


def boards_add(request):
    if request.user.is_authenticated():
            u = Usersinfo.objects.get(no=request.user.pk)
            boards = u.boards.all()
            if not boards:
                flag = 0
            else:
                flag = 1
            if request.method == "POST":
                title = request.POST.get('titlebox')
                boards_ob = Boards()
                boards_ob.save()
                boards_ob.uuid = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
                boards_ob.title = title
                boards_ob.save()
                u = Usersinfo.objects.get(no=request.user.pk)
                u.save()
                u.boards.add(boards_ob)
                u.save()
                boards = u.boards.all()
            return render(request, 'Boards/addboards.html', {'boards': boards, 'flag': flag})
    else:
        redirect('Home:login')


def list_add(request, idd):
    if request.user.is_authenticated():
        if 'sub_list' in request.POST:
            board_id = request.POST.get('board-id')
            title = request.POST.get('listbox')
            list_card = ListofCards()
            list_card.save()
            list_card.key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
            list_card.title = title
            list_card.save()
            boards = Boards.objects.get(uuid=board_id)
            boards.save()
            boards.listInsideProjects.add(list_card)
            boards.save()
        if 'add_mem' in request.POST:
            flag = 0
            mem_name = request.POST.get('member_box')
            us = User.objects.all()
            for x in us:
                if x.username == mem_name:
                    ob = Usersinfo.objects.get(no=x.pk)
                    b = Boards.objects.get(uuid=idd)
                    ob.boards.add(b)
                    ob.save()
                    flag = 1
                    break
            if flag == 0:
                return HttpResponse('User not found')
        if 'add_card' in request.POST:
            list_id = request.POST.get('list_id')
            title = request.POST.get('card_name')
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
            card_title = Cards_title()
            card_title.c_key = ob
            card_title.name = str(title)
            card_title.save()
            listt = ListofCards.objects.get(key=list_id)
            listt.listofcards.add(ob)
            listt.save()
        b = Boards.objects.get(uuid=idd)
        ll = b.listInsideProjects.all()
        names = Cards_title.objects.all()
        cards = Cards.objects.all()
        return render(request, 'Boards/addlist.html', {'obj': ll,  'board_id': idd, 'names':names, 'cards':cards ,'board': b })
    else:
        redirect('Home:login')


class DeleteBoard(DeleteView):
    model = Boards
    success_url = reverse_lazy('boards:boards_add')


class DeleteList(DeleteView):
    model = ListofCards
    success_url = reverse_lazy('boards:boards_add')
