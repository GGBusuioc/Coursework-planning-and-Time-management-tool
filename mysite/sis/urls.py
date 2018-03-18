from django.urls import path, include
from . import views



app_name = 'sis'
urlpatterns = [
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('', views.index, name="index"),
    path('staff_redirect/', views.staff_redirect, name="staff_redirect"),
    path('student_redirect/', views.student_redirect, name="student_redirect"),
    path('professor_redirect/', views.professor_redirect, name="professor_redirect"),

    path('coursework_scheduler/', views.coursework_scheduler, name="coursework_scheduler"),
    path('taught_modules/', views.taught_modules, name="taught_modules"),
    path('create_coursework/', views.create_coursework, name="create_coursework"),
    path('display_users/', views.display_users, name="display_users"),
    path('create_module/', views.create_module, name="create_module"),
    path('coursework_details/<int:module_id>/<int:coursework_id>/', views.coursework_details, name='coursework_details'),

    path('enroll_module/', views.enroll_module, name="enroll_module"),



]
