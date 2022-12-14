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
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/redeem_key/', redeem_key, name='redeem_key'),
    path('dashboard/user_page/', user_page, name='user_page'),
    path('admin-page/users/', admin_page_users, name='admin_page_users'),
    path('admin-page/keys/', admin_page_keys, name='admin_page_keys'),
    path('admin-page/user/edit/<int:pk>/', admin_page_user_edit, name='admin_page_user_edit'),
    path('admin-page/user/delete/<int:pk>/', admin_page_user_delete, name='admin_page_user_delete'),
    path('admin-page/status_and_uploads/', admin_page_status_and_uploads, name='admin_page_status_and_uploads'),
    path('admin-page/user/delete/<int:pk>/', admin_page_user_delete, name='admin_page_user_delete'),
    path('admin-page/user/delete/sub/<int:pk>/', admin_page_user_delete_sub, name='admin_page_user_delete_sub'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
