from django.urls import path, include, re_path
from django.contrib import admin
from sis import views


urlpatterns = [
    path('', include('sis.urls')),
    path('admin/', admin.site.urls),
    #path('sis/', include('django.contrib.auth.urls')),
    #path('staff_redirect/', views.staff_redirect, name="staff_redirect")

]
