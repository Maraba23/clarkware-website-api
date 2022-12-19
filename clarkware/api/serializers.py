from rest_framework import serializers
from django.contrib.auth.models import User
from usuarios.models import Profile, Product, SubscriptionKey, Subscription


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'