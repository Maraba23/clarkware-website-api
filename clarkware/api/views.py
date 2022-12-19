import profile
from sys import api_version
import unicodedata
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken

from usuarios.models import *
from .serializers import *
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from rest_framework.decorators import api_view
from usuarios.models import Profile, Product, SubscriptionKey, Subscription
from django.shortcuts import render, redirect
import sweetify
import datetime

API_KEY = 'api_clark-Lp9JRC46wLoVjvrjWRjfbsYZ4Yrr45I4sLOq1pvhG9f3JBshqo'

@api_view(['GET'])
def see_if_user_exists(request, apikey, username, password):
    if apikey == API_KEY:
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return Response({'exists': True})
            else:
                return Response({'exists': False})
        except:
            return Response({'exists': False})
    else:
        return Response({'exists': False})


@api_view(['GET'])
def get_profile_by_username(request, apikey, username):
    if apikey == API_KEY:
        try:
            profile = Profile.objects.get(username=username)
            serializer = ProfileSerializer(profile, many=False)
            return Response(serializer.data)
        except:
            return Response({'exists': False})
    else:
        return Response({'exists': False})

@api_view(['GET', 'PUT'])
def check_hwid(request, apikey, username, hwid):
    if apikey == API_KEY:
        try:
            profile = Profile.objects.get(username=username)
            if profile.hwid == hwid:
                return Response('True')
            elif profile.hwid == '':
                profile.hwid = hwid
                profile.save()
                return Response('Profile updated')
            else:
                return Response('False')
        except:
            return Response('False')
    else:
        return Response({'exists': False})
