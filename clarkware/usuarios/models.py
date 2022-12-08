from email import message
from email.mime import image
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from sqlalchemy import null
import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    hwid = models.CharField(max_length=100, null=True)
    is_banned = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username

    
class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    version = models.CharField(max_length=100, null=True)
    dll = models.FileField(upload_to='dlls/', null=True)
    exe = models.FileField(upload_to='exes/', null=True)

    def __str__(self):
        return self.name


class SubscriptionKey(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    key = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    time = models.IntegerField(default=0)

    def __str__(self):
        return self.key + ' - time: ' + self.time + ' days'

class Subscription(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    end_date = models.DateTimeField()
    end_date_loader = models.CharField(max_length=100, null=True)
    days_left = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name + ' - ' + self.user.username

