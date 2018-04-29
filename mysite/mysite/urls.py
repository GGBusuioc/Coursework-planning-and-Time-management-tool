from django.urls import path, include, re_path
from django.contrib import admin
from sis import views


urlpatterns = [
    path('', include('sis.urls')),
    path('admin/', admin.site.urls),
]
