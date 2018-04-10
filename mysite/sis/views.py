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
import json

from django.contrib import messages


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:

                login(request, user)
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email
                request.session['username'] = user.email.split('@')[0]
                print("this is the username")
                print(request.session['username'])
                if user.is_student:
                    request.session['permission'] = 'student'
                    request.session['logged_in'] = 'logged_in'
                    return HttpResponseRedirect('/student_redirect/')

                elif user.is_professor:
                    request.session['permission'] = 'professor'
                    request.session['logged_in'] = 'logged_in'

                    return HttpResponseRedirect('/professor_redirect/')
                elif user.is_staff:

                    request.session['permission'] = 'staff'
                    request.session['logged_in'] = 'logged_in'
                    return HttpResponseRedirect('/staff_redirect/')
            else:
                return render(request, {'error_message':'Invalid login'})
        else:
            # if there is no user with that Email
            user_object = User.objects.filter(email=email)
            if user_object:
                messages.error(request, 'Wrong password input!')

            else:
                messages.error(request, 'Wrong email input!')





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





def coursework_scheduler(request):
    modules = UserModuleMembership.objects.filter(user__id = request.session['user_id'])

    modules_list = []
    graphdata_list = []
    graphlabel_list = []

    coursework_objects = []
    for module in modules:
        courseworks = Coursework.objects.filter(module__id = module.module_id )
        coursework_objects.append(courseworks)
        modules_list.append(str(module.module))
        # graphdata_list.append(module.credits)


    coursework_list = []
    for an_object in coursework_objects:
        for coursework in an_object:
            coursework_payload = {}
            coursework_payload['id'] = coursework.id
            coursework_payload['title'] = coursework.title
            coursework_payload['start'] = coursework.start
            coursework_payload['end'] = coursework.end
            coursework_payload['percentage'] = coursework.percentage
            module = Module.objects.get(name = coursework.module)
            coursework_payload['module_id'] = module.id
            coursework_payload['module_name'] = module.name

            # if the coursework is not mark as completed
            objects = UserCourseworkMembership.objects.filter(user__id = request.session['user_id'], coursework = coursework.id)
            for object in objects:
                if object.percentage != 100:
                    graphdata_list.append(module.credits/(100/coursework.percentage))
                    graphlabel_list.append(coursework.title)

            coursework_list.append(coursework_payload)


    print(graphlabel_list)


    return render(request, 'sis/coursework_scheduler.html', {'coursework_list' : coursework_list, 'modules_list' : modules_list , 'graphdata_list':graphdata_list, 'graphlabel_list':graphlabel_list}, )



def staff_redirect(request):
    return render(request, 'sis/staff_home.html')

def professor_redirect(request):
    return render(request, 'sis/professor_home.html')


def student_redirect(request):
    return render(request, 'sis/student_home.html')


def coursework_details(request, module_id, coursework_id):
    # get current user
    coursework = Coursework.objects.get(id=coursework_id)
    user_cousework_object = UserCourseworkMembership.objects.get(user=request.session['user_id'],coursework=coursework)
    print(user_cousework_object.percentage)

    form = CourseworkCompletedForm(request.POST or None, initial={'percentage': user_cousework_object.percentage})
    print(form.is_valid())

    print(form)
    if form.is_valid():
        print(form.cleaned_data.get('percentage'))
        object = UserCourseworkMembership.objects.get(user=request.session['user_id'],coursework=coursework_id)


        object.percentage = form.cleaned_data.get('percentage')

        object.save()



    # search for the coursework
    coursework = Coursework.objects.get(id=coursework_id)
    print(request.session['user_id'])
    user_cousework_object = UserCourseworkMembership.objects.get(user=request.session['user_id'],coursework=coursework)
    # get its specifications
    print("here should be the coursework specifications")

    return render(request, 'sis/coursework_details.html', {'form':form, 'module_id' : module_id, 'coursework_id' : coursework_id, 'coursework_details': coursework.description, 'coursework_title':coursework.title})



def taught_modules(request):
    if not request.user.is_professor:
        return HttpResponseRedirect('/login_user/')

    modules = UserModuleMembership.objects.filter(user__id=request.session['user_id'])
    modules_list = []
    for module in modules:
        modules_list.append(str(module.module))
    print(modules_list)
    return render(request, 'sis/taught_modules.html', {'modules_list': modules_list})


def create_module(request):

    if not request.user.is_staff:
        return HttpResponseRedirect('/login_user/')

    form = ModuleForm(request.POST or None)
    print(form.is_valid())

    if form.is_valid():
        name = request.POST['name']
        description = request.POST['description']

        Module.objects.create(name=name, description=description)
    return render(request,'sis/create_module.html', {'form':form})



def create_coursework(request):

    if not request.user.is_professor:
        return HttpResponseRedirect('/login_user/')
    print("request user before form")

    form = CourseworkForm(request.POST, user=request.user)
    print("AAAA")

    print(form.is_valid())
    # print(form.errors.as_data())
    # print(form.is_valid())
    if form.is_valid():
        module = Module.objects.get(id=request.POST['module'])
        title = request.POST['title']
        description = request.POST['description']
        start = request.POST['start']
        end = request.POST['end']
        percentage = request.POST['percentage']

        new_coursework = Coursework.objects.create(title=title, description=description, start=start, end=end, module=module, percentage=percentage)

        # for each student enrolled in that module
        students = User.objects.filter(student=True)
        for student in students:
            print(student)
            if UserModuleMembership.objects.get(user=student, module=module):
                print("You need to do some stuff for %s" % (student))
                UserCourseworkMembership.objects.create(user=student, coursework=new_coursework)


        # create entry in UserCourseworkMembership

    return render(request,'sis/create_coursework.html', {'form':form})


def display_users(request):
    if not request.user.is_staff:
        return HttpResponseRedirect('/login_user/')
    users = User.objects.all()

    user_list = []
    for user in users:
        user_dict = {}
        user_dict['id'] = user.id
        user_dict['email'] = user.email
        user_dict['is_student'] = user.is_student
        user_dict['is_professor'] = user.is_professor
        user_dict['is_staff'] = user.is_staff
        user_list.append(user_dict)

    return render(request,'sis/display_users.html', {'user_list':user_list})

def enroll_module(request):
    if not request.user.is_staff:
        return HttpResponseRedirect('/login_user/')


    form = UserModuleForm(request.POST or None)
    print(form.is_valid())
    if form.is_valid():
        user = User.objects.get(id=request.POST['user'])
        module = Module.objects.get(id=request.POST['module'])

        UserModuleMembership.objects.create(user=user, module=module)

    return render(request,'sis/enroll_module.html', {'form':form })

def assign_module(request):
    if not request.user.is_staff:
        return HttpResponseRedirect('/login_user/')

    form = AssignModuleForm(request.POST or None)
    if form.is_valid():
        user = User.objects.get(id=request.POST['user'])
        module = Module.objects.get(id=request.POST['module'])

        UserModuleMembership.objects.create(user=user, module=module)


    return render(request,'sis/assign_module.html', {'form':form })
