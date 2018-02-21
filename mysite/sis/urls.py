from django.urls import path, include
from . import views



app_name = 'sis'
urlpatterns = [
    path('home/', views.home),
    #path('register/', views.UserFormView.as_view(), name='register'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('index/', views.index, name="index")
]
