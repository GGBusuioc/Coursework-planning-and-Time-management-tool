from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

from django.http import HttpResponseRedirect

from sis.forms import UserForm
from django.template import RequestContext
from .models import *

from django.views.decorators.csrf import csrf_exempt

from django.urls import reverse
from django.template import loader
from django.template.response import TemplateResponse
from .forms import *


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)


        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['user_id'] = user.id
                if user.is_student:
                    return render(request, 'sis/student_home.html', {'var': 'var'})
                elif user.is_professor:
                    return render(request, 'sis/professor_home.html')
                elif user.is_staff:
                    request.session['permission'] = 'staff'
                    request.session['logged_in'] = 'logged_in'
                    # print(request.session['permission'])
                    return HttpResponseRedirect('/staff_redirect/')
            else:
                return render(request, {'error_message':'Invalid login'})
    return render(request, 'sis/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'sis/login.html', context)

def index(request):
    return render(request, 'sis/index.html')


#@login_required
def create_module(request):
    print(request.user)
    if not request.user.is_staff:
        return HttpResponseRedirect('/login_user/')



    form = ModuleForm(request.POST or None)
    if form.is_valid():
        name = request.POST['name']
        description = request.POST['description']

        Module.objects.create(name=name, description=description)


    return render(request,'sis/create_module.html')

def staff_redirect(request):
    return render(request, 'sis/staff_home.html')


def professor_redirect(request):
    return HttpResponse("You have been redirected to professor view")


def student_redirect(request):
    return HttpResponse("You have been redirected to student view")
