from django.urls import path
from .views import *

urlpatterns = [
    path('see_if_user_exists/<str:apikey>/<str:username>/<str:password>', see_if_user_exists, name='see_if_user_exists'),
    path('get_profile_by_username/<str:apikey>/<str:username>', get_profile_by_username, name='get_profile_by_username'),

]