from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path
from usuarios.views import *
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    path('dashboard/', home, name='home'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
