import ast
import code
from imp import reload
from itertools import product
import json
from numbers import Real
import profile
import random
from socket import SHUT_WR
import string
import subprocess
import re
from tokenize import Token
from unicodedata import name
from urllib import response
from xml.dom import UserDataHandler
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from .models import *
from django.contrib.auth import login
from .forms import *
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import sweetify
import requests
from rest_framework.response import Response
from knox.models import AuthToken
import json
import datetime
from django.contrib.auth.hashers import make_password
from django.http import FileResponse, HttpResponse, HttpResponseNotFound, JsonResponse
import stripe
from django.conf import settings
from django.views import View

API_KEY = 'api_clark-Lp9JRC46wLoVjvrjWRjfbsYZ4Yrr45I4sLOq1pvhG9f3JBshqo'

def index(request):
    if request.method == 'POST':
        if 'register' in request.POST:
            form1 = RegisterForm(request.POST)
            if form1.is_valid():
                user = form1.save()
                try:
                    Profile.objects.create(
                        user=user,
                        username=user.username,
                        email=user.email,
                        auth_token=''.join(random.choices(string.ascii_uppercase + string.digits, k=50)),
                    )
                except:
                    sweetify.error(request, 'There was an error creating your profile', icon='error', button='OK', timer='3000')
                    return redirect('index')

            else:
                sweetify.error(request, 'There was an error creating your account (#Error2)', icon='error', button='OK', timer='3000')
                return redirect('index')
        elif 'login' in request.POST:
            form2 = LoginForm(request.POST)
            if form2.is_valid():
                if User.objects.filter(username=request.POST['username']).exists():
                    user = User.objects.get(username=request.POST['username'])
                    if user.check_password(request.POST['password']):
                        auth_login(request, user)
                        return redirect('home')
                    else:
                        sweetify.error(request, 'Incorrect password', icon='error', button='OK', timer='3000')
                        return redirect('index')
                else:
                    sweetify.error(request, 'User not found', icon='error', button='OK', timer='3000')
                    return redirect('index')
            else:
                sweetify.error(request, 'There was an error logging in (#Error3)', icon='error', button='OK', timer='3000')
                return redirect('index')
        else:
            sweetify.error(request, 'There was an error (#Error1)', icon='error', button='OK', timer='3000')
            return redirect('index')


    return render(request, 'index.html')

@login_required(login_url='index')
def home(request):
    return render(request, 'dashboard.html')