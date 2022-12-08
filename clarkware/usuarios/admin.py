from django.contrib import admin
from .models import Profile, Product, SubscriptionKey, Subscription


admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(SubscriptionKey)
admin.site.register(Subscription)
