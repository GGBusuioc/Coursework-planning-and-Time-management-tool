from django.urls import path, include
from . import views



app_name = 'sis'
urlpatterns = [
    # basic paths
    path('', views.index, name="index"),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),

    # basic redirect paths
    path('staff_redirect/', views.staff_redirect, name="staff_redirect"),
    path('student_redirect/', views.student_redirect, name="student_redirect"),
    path('professor_redirect/', views.professor_redirect, name="professor_redirect"),

    # student paths
    path('coursework_scheduler/', views.coursework_scheduler, name="coursework_scheduler"),
    path('coursework_details/<int:module_id>/<int:coursework_id>/', views.coursework_details, name='coursework_details'),

    # profesor paths
    path('create_coursework/', views.create_coursework, name="create_coursework"),
    path('taught_modules/', views.taught_modules, name="taught_modules"),

    # staff member paths
    path('enroll_module/', views.enroll_module, name="enroll_module"),
    path('assign_module/', views.assign_module, name="assign_module"),
    path('display_users/', views.display_users, name="display_users"),
    path('create_module/', views.create_module, name="create_module"),

]
