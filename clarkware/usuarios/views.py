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
    lista_produtos = Product.objects.all()
    return render(request, 'dashboard.html', {'max_profiles': max_profiles, 'current_user': current_user, 'subscribed_profiles': subscribed_profiles, 'lista_produtos': lista_produtos})

@login_required(login_url='index')
def redeem_key(request):
    current_user = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        if 'redeem_key' in request.POST:
            if SubscriptionKey.objects.filter(key=request.POST['redeem_key'], product=Product.objects.get(name='lite')).exists():
                if Subscription.objects.filter(user=current_user, product=Product.objects.get(name='lite')).exists():
                    sweetify.error(request, 'You already have a Lite subscription', icon='error', button='OK', timer='3000')
                    return redirect('dashboard')
                today = datetime.date.today()
                key_time = SubscriptionKey.objects.get(key=request.POST['redeem_key'], product=Product.objects.get(name='lite')).time
                end_date = today + datetime.timedelta(days=int(key_time))
                Subscription.objects.create(
                    user=current_user,
                    product=Product.objects.get(name='lite'),
                    end_date=end_date,
                    end_date_loader=end_date.strftime("%Y-%m-%d"),
                )
                SubscriptionKey.objects.get(key=request.POST['redeem_key'], product=Product.objects.get(name='lite')).delete()
                sweetify.success(request, 'Key redeemed successfully', icon='success', button='OK', timer='3000')
                return redirect('dashboard')
            elif SubscriptionKey.objects.filter(key=request.POST['redeem_key'], product=Product.objects.get(name='semirage')).exists():
                if Subscription.objects.filter(user=current_user, product=Product.objects.get(name='semirage')).exists():
                    sweetify.error(request, 'You already have a Semirage subscription', icon='error', button='OK', timer='3000')
                    return redirect('dashboard')
                today = datetime.date.today()
                key_time = SubscriptionKey.objects.get(key=request.POST['redeem_key'], product=Product.objects.get(name='semirage')).time
                end_date = today + datetime.timedelta(days=int(key_time))
                Subscription.objects.create(
                    user=current_user,
                    product=Product.objects.get(name='semirage'),
                    end_date=end_date,
                    end_date_loader=end_date.strftime("%Y-%m-%d"),
                )
                SubscriptionKey.objects.filter(key=request.POST['redeem_key'], product=Product.objects.get(name='semirage')).delete()
                sweetify.success(request, 'Key redeemed successfully', icon='success', button='OK', timer='3000')
                return redirect('dashboard')
            elif SubscriptionKey.objects.filter(key=request.POST['redeem_key'], product=Product.objects.get(name='rage')).exists():
                if Subscription.objects.filter(user=current_user, product=Product.objects.get(name='rage')).exists():
                    sweetify.error(request, 'You already have a Rage subscription', icon='error', button='OK', timer='3000')
                    return redirect('dashboard')
                today = datetime.date.today()
                key_time = SubscriptionKey.objects.get(key=request.POST['redeem_key'], product=Product.objects.get(name='rage')).time
                end_date = today + datetime.timedelta(days=int(key_time))
                Subscription.objects.create(
                    user=current_user,
                    product=Product.objects.get(name='rage'),
                    end_date=end_date,
                    end_date_loader=end_date.strftime("%Y-%m-%d"),
                )
                SubscriptionKey.objects.get(key=request.POST['redeem_key'], product=Product.objects.get(name='rage')).delete()
                sweetify.success(request, 'Key redeemed successfully', icon='success', button='OK', timer='3000')
                return redirect('dashboard')
            else:
                sweetify.error(request, 'Invalid key', icon='error', button='OK', timer='3000')
                return redirect('dashboard')
    return render(request, 'redeem_key.html', {'current_user': current_user})

@login_required(login_url='index')
def user_page(request):
    current_user = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        if 'change_password' in request.POST:
            current_user.user.set_password(request.POST['change_password'])
            current_user.user.save()
            sweetify.success(request, 'Password changed successfully', icon='success', button='OK', timer='3000')
            return redirect('user_page')
        elif 'change_email' in request.POST:
            current_user.user.email = request.POST['change_email']
            current_user.user.save()
            sweetify.success(request, 'Email changed successfully', icon='success', button='OK', timer='3000')
            return redirect('user_page')
    
    # get the user's subscriptions
    user_subscriptions = Subscription.objects.filter(user=current_user)
    for subscription in user_subscriptions:
        if subscription.end_date.strftime("%Y-%m-%d") < datetime.date.today().strftime("%Y-%m-%d"):
            subscription.delete()
        else:
            days_left = subscription.end_date.date() - datetime.date.today()
            subscription.days_left = days_left.days
            subscription.save()

    return render(request, 'user_page.html', {'current_user': current_user, 'user_subscriptions': user_subscriptions})







#==================================================================================================#


@login_required(login_url='index')
def admin_page_keys(request):
    current_user = Profile.objects.get(user=request.user)
    if current_user.is_admin:
        if request.method == 'POST':
            if "gen_lite" in request.POST:
                if 'key_lite' in request.POST:
                    if 'lite_prefix' in request.POST:
                        if request.POST['lite_prefix'] != '':
                            key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))
                            key = key[:5] + '-' + key[5:10] + '-' + key[10:15] + '-' + key[15:20] + '-' + key[20:]
                            key = request.POST['lite_prefix'] + '-' + key
                            SubscriptionKey.objects.create(
                                product=Product.objects.get(name='lite'),
                                key=key,
                                time=request.POST['key_lite'],
                                user=current_user,
                            )
                            sweetify.success(request, 'Key created successfully', icon='success', button='OK', timer='3000')
                            return redirect('admin_page_keys')
                    key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))
                    key = key[:5] + '-' + key[5:10] + '-' + key[10:15] + '-' + key[15:20] + '-' + key[20:]
                    SubscriptionKey.objects.create(
                        product=Product.objects.get(name='lite'),
                        key=key,
                        time=request.POST['key_lite'],
                        user=current_user,
                    )
                    sweetify.success(request, 'Key created successfully', icon='success', button='OK', timer='3000')
                    return redirect('admin_page_keys')
            
            elif "gen_semirage" in request.POST:
                if 'key_semirage' in request.POST:
                    if 'semirage_prefix' in request.POST:
                        if request.POST['semirage_prefix'] != '':
                            key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))
                            key = key[:5] + '-' + key[5:10] + '-' + key[10:15] + '-' + key[15:20] + '-' + key[20:]
                            key = request.POST['semirage_prefix'] + '-' + key
                            SubscriptionKey.objects.create(
                                product=Product.objects.get(name='semirage'),
                                key=key,
                                time=request.POST['key_semirage'],
                                user=current_user,
                            )
                            sweetify.success(request, 'Key created successfully', icon='success', button='OK', timer='3000')
                            return redirect('admin_page_keys')
                    key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))
                    key = key[:5] + '-' + key[5:10] + '-' + key[10:15] + '-' + key[15:20] + '-' + key[20:]
                    SubscriptionKey.objects.create(
                        product=Product.objects.get(name='semirage'),
                        key=key,
                        time=request.POST['key_semirage'],
                        user=current_user,
                    )
                sweetify.success(request, 'Key created successfully', icon='success', button='OK', timer='3000')
                return redirect('admin_page_keys')

            elif "gen_rage" in request.POST:
                if 'key_rage' in request.POST:
                    if 'rage_prefix' in request.POST:
                        if request.POST['rage_prefix'] != '':
                            key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))
                            key = key[:5] + '-' + key[5:10] + '-' + key[10:15] + '-' + key[15:20] + '-' + key[20:]
                            key = request.POST['rage_prefix'] + '-' + key
                            SubscriptionKey.objects.create(
                                product=Product.objects.get(name='rage'),
                                key=key,
                                time=request.POST['key_rage'],
                                user=current_user,
                            )
                            sweetify.success(request, 'Key created successfully', icon='success', button='OK', timer='3000')
                            return redirect('admin_page_keys')
                    key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))
                    key = key[:5] + '-' + key[5:10] + '-' + key[10:15] + '-' + key[15:20] + '-' + key[20:]
                    SubscriptionKey.objects.create(
                        product=Product.objects.get(name='rage'),
                        key=key,
                        time=request.POST['key_rage'],
                        user=current_user,
                    )
                    sweetify.success(request, 'Key created successfully', icon='success', button='OK', timer='3000')
                    return redirect('admin_page_keys')

        lista_keys_lite = SubscriptionKey.objects.filter(product=Product.objects.get(name='lite'))
        lista_keys_semirage = SubscriptionKey.objects.filter(product=Product.objects.get(name='semirage'))
        lista_keys_rage = SubscriptionKey.objects.filter(product=Product.objects.get(name='rage'))

        return render(request, 'admin_page_keys.html', {'current_user': current_user, 'lista_keys_lite': lista_keys_lite, 'lista_keys_semirage': lista_keys_semirage, 'lista_keys_rage': lista_keys_rage})
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

        if request.method == 'POST':
            if 'delete_user' in request.POST:
                user.delete()
                sweetify.success(request, 'User deleted', icon='success', button='OK', timer='3000')
                return redirect('admin_page_users')
            elif 'delete_user_subscriptions' in request.POST:
                Subscription.objects.filter(user=user).delete()
                sweetify.success(request, 'User subscriptions deleted', icon='success', button='OK', timer='3000')
                return redirect('admin_page_users')
            elif 'reset_user_hwid' in request.POST:
                user.hwid = ''
                user.save()
                sweetify.success(request, 'User HWID reset', icon='success', button='OK', timer='3000')
                return redirect('admin_page_users')
            if 'update' in request.POST:
                if request.POST['password'] != '':
                    user.user.set_password(request.POST['password'])
                    user.user.save()
                    sweetify.success(request, 'User password changed', icon='success', button='OK', timer='3000')
                    return redirect('admin_page_users')
                elif request.POST['email'] != '':
                    user.user.email = request.POST['email']
                    user.user.save()
                    sweetify.success(request, 'User email changed', icon='success', button='OK', timer='3000')
                    return redirect('admin_page_users')
                elif request.POST['username'] != '':
                    user.user.username = request.POST['username']
                    user.user.save()
                    sweetify.success(request, 'User username changed', icon='success', button='OK', timer='3000')
                    return redirect('admin_page_users')

        return render(request, 'admin_page_user_edit.html', {'current_user': current_user, 'user': user})
    else:
        sweetify.error(request, 'You are not authorized to view this page', icon='error', button='OK', timer='3000')
        return redirect('dashboard')

@login_required(login_url='index')
def admin_delete_key(request, pk):
    current_user = Profile.objects.get(user=request.user)
    if current_user.is_admin:
        key = SubscriptionKey.objects.get(pk=pk)
        key.delete()
        sweetify.success(request, 'Key deleted', icon='success', button='OK', timer='3000')
        return redirect('admin_page_keys')
    else:
        sweetify.error(request, 'You are not authorized to view this page', icon='error', button='OK', timer='3000')
        return redirect('dashboard')

#$=================================================================================================$#

@login_required(login_url='index')
def admin_page_status_and_uploads(request):
    current_user = Profile.objects.get(user=request.user)
    if current_user.is_admin:
        if request.method == 'POST':
            if 'upload_lite_dll' in request.FILES:
                Product.objects.filter(name='lite').update(dll=request.FILES['upload_lite_dll'])
                sweetify.success(request, 'DLL uploaded', icon='success', button='OK', timer='3000')
                return redirect('admin_page_status_and_uploads')
            elif 'upload_lite_driver' in request.FILES:
                Product.objects.filter(name='lite').update(driver=request.FILES['upload_lite_driver'])
                sweetify.success(request, 'Driver uploaded', icon='success', button='OK', timer='3000')
                return redirect('admin_page_status_and_uploads')
            elif 'upload_semirage_dll' in request.FILES:
                Product.objects.filter(name='semirage').update(dll=request.FILES['upload_semirage_dll'])
                sweetify.success(request, 'DLL uploaded', icon='success', button='OK', timer='3000')
                return redirect('admin_page_status_and_uploads')
            elif 'upload_semirage_driver' in request.FILES:
                Product.objects.filter(name='semirage').update(driver=request.FILES['upload_semirage_driver'])
                sweetify.success(request, 'Driver uploaded', icon='success', button='OK', timer='3000')
                return redirect('admin_page_status_and_uploads')
            elif 'upload_rage_dll' in request.FILES:
                Product.objects.filter(name='rage').update(dll=request.FILES['upload_rage_dll'])
                sweetify.success(request, 'DLL uploaded', icon='success', button='OK', timer='3000')
                return redirect('admin_page_status_and_uploads')
            elif 'upload_rage_driver' in request.FILES:
                Product.objects.filter(name='rage').update(driver=request.FILES['upload_rage_driver'])
                sweetify.success(request, 'Driver uploaded', icon='success', button='OK', timer='3000')
                return redirect('admin_page_status_and_uploads')
            
            if 'update_status' in request.POST:
                if request.POST['lite_status'] == '0':
                    Product.objects.filter(name='lite').update(status='Undetected')
                elif request.POST['lite_status'] == '1':
                    Product.objects.filter(name='lite').update(status='Updating')
                elif request.POST['lite_status'] == '2':
                    Product.objects.filter(name='lite').update(status='Use at your own risk')
                elif request.POST['lite_status'] == '3':
                    Product.objects.filter(name='lite').update(status='Detected')
                if request.POST['semirage_status'] == '0':
                    Product.objects.filter(name='semirage').update(status='Undetected')
                elif request.POST['semirage_status'] == '1':
                    Product.objects.filter(name='semirage').update(status='Updating')
                elif request.POST['semirage_status'] == '2':
                    Product.objects.filter(name='semirage').update(status='Use at your own risk')
                elif request.POST['semirage_status'] == '3':
                    Product.objects.filter(name='semirage').update(status='Detected')
                if request.POST['rage_status'] == '0':
                    Product.objects.filter(name='rage').update(status='Undetected')
                elif request.POST['rage_status'] == '1':
                    Product.objects.filter(name='rage').update(status='Updating')
                elif request.POST['rage_status'] == '2':
                    Product.objects.filter(name='rage').update(status='Use at your own risk')
                elif request.POST['rage_status'] == '3':
                    Product.objects.filter(name='rage').update(status='Detected')
                sweetify.success(request, 'Status updated', icon='success', button='OK', timer='3000')
                return redirect('admin_page_status_and_uploads')    
        return render(request, 'admin_page_status_and_uploads.html', {'current_user': current_user})
    else:
        sweetify.error(request, 'You are not authorized to view this page', icon='error', button='OK', timer='3000')
        return redirect('dashboard')


#$=================================================================================================$#

########## DOWNLOADS ##########

def download_dll(request, apikey, user_id, user_token, product_id):
    if apikey == API_KEY:
        user = Profile.objects.get(pk=user_id)
        if user.user_token == user_token:
            if product_id == '1':
                product = Product.objects.get(name='lite')
            elif product_id == '2':
                product = Product.objects.get(name='semirage')
            elif product_id == '3':
                product = Product.objects.get(name='rage')
            else:
                return HttpResponse('Invalid product ID')
            if product.status == 'Undetected':
                if product.dll:
                    return FileResponse(product.dll)
                else:
                    return HttpResponse('DLL not found')
            elif product.status == 'Updating':
                return HttpResponse('DLL is updating')
            elif product.status == 'Use at your own risk':
                return FileResponse(product.dll)
            elif product.status == 'Detected':
                return HttpResponse('DLL is detected')
            else:
                return HttpResponse('Invalid product status')
        else:
            return HttpResponse('Invalid user token')
    else:
        return HttpResponse('Invalid API key')

#$=================================================================================================$#

def download_driver(request, apikey, user_id, user_token, product_id):
    if apikey == API_KEY:
        user = Profile.objects.get(pk=user_id)
        if user.user_token == user_token:
            if product_id == '1':
                product = Product.objects.get(name='lite')
            elif product_id == '2':
                product = Product.objects.get(name='semirage')
            elif product_id == '3':
                product = Product.objects.get(name='rage')
            else:
                return HttpResponse('Invalid product ID')
            if product.status == 'Undetected':
                if product.driver:
                    return FileResponse(product.driver)
                else:
                    return HttpResponse('Driver not found')
            elif product.status == 'Updating':
                return HttpResponse('Driver is updating')
            elif product.status == 'Use at your own risk':
                return FileResponse(product.driver)
            elif product.status == 'Detected':
                return HttpResponse('Driver is detected')
            else:
                return HttpResponse('Invalid product status')
        else:
            return HttpResponse('Invalid user token')
    else:
        return HttpResponse('Invalid API key')

#$=================================================================================================$#