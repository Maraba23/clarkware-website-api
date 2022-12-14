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
                        return redirect('dashboard')
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
def dashboard(request):
    max_profiles = Profile.objects.all().count()
    current_user = Profile.objects.get(user=request.user)
    subscribed_profiles = Subscription.objects.all().count()
    return render(request, 'dashboard.html', {'max_profiles': max_profiles, 'current_user': current_user, 'subscribed_profiles': subscribed_profiles})

@login_required(login_url='index')
def redeem_key(request):
    current_user = Profile.objects.get(user=request.user)
    return render(request, 'redeem_key.html', {'current_user': current_user})

@login_required(login_url='index')
def user_page(request):
    current_user = Profile.objects.get(user=request.user)
    return render(request, 'user_page.html', {'current_user': current_user})







#==================================================================================================#


@login_required(login_url='index')
def admin_page_keys(request):
    current_user = Profile.objects.get(user=request.user)
    if current_user.is_admin:
        return render(request, 'admin_page_keys.html', {'current_user': current_user})
    else:
        sweetify.error(request, 'You are not authorized to view this page', icon='error', button='OK', timer='3000')
        return redirect('dashboard')

@login_required(login_url='index')
def admin_page_users(request):
    current_user = Profile.objects.get(user=request.user)
    all_users = Profile.objects.all()
    if current_user.is_admin:
        return render(request, 'admin_page_users.html', {'current_user': current_user, 'all_users': all_users})
    else:
        sweetify.error(request, 'You are not authorized to view this page', icon='error', button='OK', timer='3000')
        return redirect('dashboard')

@login_required(login_url='index')
def admin_page_user_edit(request, pk):
    current_user = Profile.objects.get(user=request.user)
    if current_user.is_admin:
        user = Profile.objects.get(pk=pk)
        return render(request, 'admin_page_user_edit.html', {'current_user': current_user, 'user': user})
    else:
        sweetify.error(request, 'You are not authorized to view this page', icon='error', button='OK', timer='3000')
        return redirect('dashboard')

@login_required(login_url='index')
def admin_page_user_delete_sub(request, pk):
    current_user = Profile.objects.get(user=request.user)
    if current_user.is_admin:
        user = Profile.objects.get(pk=pk)
        return render(request, 'admin_page_user_delete.html', {'current_user': current_user, 'user': user})
    else:
        sweetify.error(request, 'You are not authorized to view this page', icon='error', button='OK', timer='3000')
        return redirect('dashboard')

@login_required(login_url='index')
def admin_page_user_delete(request, pk):
    current_user = Profile.objects.get(user=request.user)
    if current_user.is_admin:
        user = Profile.objects.get(pk=pk)
        user.delete()
        sweetify.success(request, 'User deleted', icon='success', button='OK', timer='3000')
        return redirect('admin_page_users')
    else:
        sweetify.error(request, 'You are not authorized to view this page', icon='error', button='OK', timer='3000')
        return redirect('dashboard')


#$=================================================================================================$#

@login_required(login_url='index')
def admin_page_status_and_uploads(request):
    current_user = Profile.objects.get(user=request.user)
    if current_user.is_admin:
        return render(request, 'admin_page_status_and_uploads.html', {'current_user': current_user})
    else:
        sweetify.error(request, 'You are not authorized to view this page', icon='error', button='OK', timer='3000')
        return redirect('dashboard')


#$=================================================================================================$#