from django.urls import path, include
from . import views



app_name = 'sis'
urlpatterns = [
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('', views.index, name="index"),
    path('staff_redirect/', views.staff_redirect, name="staff_redirect"),
    path('create_module/', views.create_module, name="create_module"),


]
