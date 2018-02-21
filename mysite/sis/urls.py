from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.home),
    path('register/', views.UserFormView.as_view(), name='register'),
]
