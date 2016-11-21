from django.contrib.auth.models import User
from django.shortcuts import render,  redirect
from django.views.generic import View
from .forms import UserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, StreamingHttpResponse
from .models import *
from rest_framework.views import APIView
import json
from Home.serializers import UsersinfoSerializers
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
# Create your views here.
'''
json loads -> returns an object from a string representing a json object.
json dumps -> returns a string representing a json object from an object.
'''

class LoginFormView(View):
    form_class = LoginForm
    template_name = 'Home/index.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('cards:CardsProjects_All')
        form = self.form_class(None)
        return render(request, self.template_name,{})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:
                login(request, user)
                return redirect('cards:CardsProjects_All')
        return HttpResponse('<p>bhag</p>')


class UserFormView(View):
    form_class = UserForm
    template_name = 'Home/registrationform.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            u = Usersinfo()
            us = User.objects.get(pk=user.pk)
            u.no = us
            u.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('cards:CardsProjects_All')
        return render(request, self.template_name, {'form': form})

def logout_view(request):
    logout(request)
    return redirect('Home:welcome')


def board(request):
    return render(request, 'Home/base.html', {})


'''JSON'''
class Usersinfolist(APIView):

    def get(self, request):
        users = Usersinfo.objects.all()
        serializer = UsersinfoSerializers(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        received_data = json.dumps(request.data)
        json_data = json.loads(received_data)
        return HttpResponse(json.dumps(json_data['no']['email']))

