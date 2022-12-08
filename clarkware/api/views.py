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