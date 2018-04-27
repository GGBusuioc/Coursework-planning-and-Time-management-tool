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

from django.contrib import messages


import datetime
from datetime import timedelta




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
    return render(request, 'sis/login.html')

def index(request):
    return render(request, 'sis/index.html')





def coursework_scheduler(request):

    if not request.user.is_student:
        return HttpResponseRedirect('/login_user/')

    now = datetime.datetime.now()

    # display notifications
    print("Display notifications")
    notification_objects = Notification.objects.filter(user__id = request.session['user_id'])
    for notification in notification_objects:
        print(notification.notification)

    modules = UserModuleMembership.objects.filter(user__id = request.session['user_id'])

    modules_list = []
    graphdata_list = []
    graphlabel_list = []
    last_data_list = []
    # big_coursework = False
    coursework_objects = []
    for module in modules:
        courseworks = Coursework.objects.filter(module__id = module.module_id)

        # if coursework is ongoing
        #all_courseworks =  Coursework.objects.filter(module__id = module.module_id)

        coursework_objects.append(courseworks)
        modules_list.append(str(module.module))
        # graphdata_list.append(module.credits)

    color_list = ['#f92672', '#a6e22e', '#66d9ef', '#fd971f', '#ae81ff', '#8d7b92', '#a07b7b', '#9290a6', '#9aaca0', '#b595ac']
    # color_list = ['#8E44AD', '#2E86C1', '#1E8449']

    ongoing_courseworks_labels = []
    ongoing_courseworks_data = []


    coursework_list = []
    for an_object in coursework_objects:

        for coursework in an_object:
            coursework_payload = {}
            coursework_payload['id'] = coursework.id
            coursework_payload['title'] = coursework.title
            coursework_payload['start'] = coursework.start
            coursework_payload['end'] = coursework.end
            coursework_payload['color'] = coursework.color
            coursework_payload['percentage'] = coursework.percentage
            module = Module.objects.get(name = coursework.module)
            coursework_payload['module_id'] = module.id
            coursework_payload['module_name'] = module.name
            coursework_payload['progress'] = 0


            coursework_list.append(coursework_payload)
            print("COURSEWORK")
            print(coursework.title)

            # if the coursework is not mark as completed
            objects = UserCourseworkMembership.objects.filter(user__id = request.session['user_id'], coursework = coursework.id)
            for object in objects:
                coursework_payload['progress'] =  object.percentage

                if coursework_payload['start'] <= now.date() and coursework_payload['end'] >= now.date() and coursework_payload['progress']!=100:
                    ongoing_courseworks_labels.append(coursework_payload['title'])

                    # if module.credits/(100/coursework.percentage)>=10:
                        # big_coursework = True

                    ongoing_courseworks_data.append(module.credits/(100/coursework.percentage))

                    nr_hours = (module.credits/(100/coursework.percentage) * 90) / 60

                    # if any coursework is big and above 10credits & there are more than 5 courseworks

                    # else use this formula
                    # nr_hours = (module.credits/(100/coursework.percentage) * 30) / 60

                    last_data_list.append(nr_hours)


                if object.percentage != 100 and coursework_payload['end'] >= now.date():

                    graphdata_list.append(module.credits/(100/coursework.percentage))
                    # print(module.credits/(100/coursework.percentage))


                    # if any coursework is big and above 10credits & there are more than 5 courseworks

                    graphlabel_list.append(coursework.title)


    radar_data =[]
    # for el in last_data_list:
    #     # print(int(round(el, 0)))
    #     radar_data.append(int(round(el, 0)))
    #
    # ongoing_colors =[]
    # colors_used = []
    # i = 0
    # for coursework in coursework_list:
    #     # if the cw deadline is in the past then keep its color
    #     for el in ongoing_courseworks_labels:
    #         print(coursework['title'])
    #         if(coursework['title']==el):
    #
    #             ongoing_colors.append(coursework['color'])
    #
    #
    #     if coursework['progress'] != 100 and coursework['end'] >= now.date():
    #         coursework['color'] = color_list[i]
    #
    #         colors_used.append(color_list[i])
    #         i = i + 1


# hereeee
    print("RADAR DATA")
    print(radar_data)
    ongoing_colors =[]
    colors_used = []
    i = 0
    for coursework in coursework_list:
        if coursework['progress'] != 100 and coursework['end'] > now.date():
            coursework['color'] = color_list[i]

            colors_used.append(color_list[i])
            i = i + 1


        for el in ongoing_courseworks_labels:
            if(coursework['title']==el):

                ongoing_colors.append(coursework['color'])

    for el in last_data_list:
        radar_data.append(int(round(el, 0)))


    # compute data for the last graph





    return render(request, 'sis/coursework_scheduler.html', {'radar_data':radar_data,'ongoing_colors':ongoing_colors,'ongoing_courseworks_labels':ongoing_courseworks_labels, 'ongoing_courseworks_data':ongoing_courseworks_data, 'colors_used': colors_used,'coursework_list' : coursework_list, 'modules_list' : modules_list , 'graphdata_list':graphdata_list, 'graphlabel_list':graphlabel_list}, )



def staff_redirect(request):
    return render(request, 'sis/staff_home.html')

def professor_redirect(request):
    return render(request, 'sis/professor_home.html')


def student_redirect(request):

    now = datetime.datetime.now()


    print("Student redirect notifications")
    notification_objects = Notification.objects.filter(user__id = request.session['user_id'])
    for notification in notification_objects:
        print(notification.notification)
        messages.info(request, notification.notification)
        print("Added message to messages")

    # check if any deadline is close

    # for all the courseworks that the student has
    user_coursework_objects = UserCourseworkMembership.objects.filter(user__id = request.session['user_id'])
    for user_coursework in user_coursework_objects:

        coursework = user_coursework.coursework
        coursework_object = Coursework.objects.get(id=coursework.id)


        if now.date()+datetime.timedelta(days=1) == coursework_object.end:
            # check if the coursework is marked as completed
            if user_coursework.percentage < 100:
                messages.warning(request, "Deadline for %s is %s. Your progress so far is: %d PERCENT" % (coursework_object ,coursework_object.end, user_coursework.percentage))

        if coursework_object.end-datetime.timedelta(days=1) < now.date() and user_coursework.percentage != 100:
            messages.error(request, "Deadline for %s has passed. Your progress so far is: %d PERCENT" % (coursework_object , user_coursework.percentage))

            # add notification

        # for each coursework check if the deadline is near


    # empty the notifications
    print("Display notifications after deletion")
    for notification in notification_objects:
        notification.delete()

    print(notification_objects)


    return render(request, 'sis/student_home.html')


def coursework_details(request, module_id, coursework_id):
    # get current user
    coursework = Coursework.objects.get(id=coursework_id)
    user_cousework_object = UserCourseworkMembership.objects.get(user=request.session['user_id'],coursework=coursework)
    print(user_cousework_object.percentage)

    form = CourseworkCompletedForm(request.POST or None, initial={'percentage': user_cousework_object.percentage})



    messages.info(request, "You have marked %s as being %d percent complete. " % (coursework.title, user_cousework_object.percentage))


    if form.is_valid():

        print(form.cleaned_data.get('percentage'))
        object = UserCourseworkMembership.objects.get(user=request.session['user_id'],coursework=coursework_id)


        object.percentage = form.cleaned_data.get('percentage')

        object.save()



    # search for the coursework
    coursework = Coursework.objects.get(id=coursework_id)
    user_cousework_object = UserCourseworkMembership.objects.get(user=request.session['user_id'],coursework=coursework)
    # get its specifications


    # get the number of credits for the project
    module_object = Module.objects.get(id=module_id)

    return render(request, 'sis/coursework_details.html', {'form':form, 'module_id' : module_id, 'coursework_id' : coursework_id, 'coursework_percentage':coursework.percentage, 'module_title':module_object.name,'module_credits':module_object.credits, 'coursework_details': coursework.description, 'coursework_title':coursework.title})



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

    print(form.is_valid())

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
            if UserModuleMembership.objects.filter(user=student, module=module):
                # let the student know that a new coursework has been created
                Notification.objects.create(user=student, notification="New coursework created. %s - %s. " % (new_coursework.title, module))
                print("Notifications created")
                UserCourseworkMembership.objects.create(user=student, coursework=new_coursework)


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
        Notification.objects.create(user=user, notification="You have been enrolled to a new module. Welcome to %s. " % (module))
        print("Module notification created")
        UserModuleMembership.objects.create(user=user, module=module)

        # for all the coruseworks create a relationship
        courseworks = Coursework.objects.filter(module=module)
        print(courseworks)
        for coursework in courseworks:
            print("What you are looking at")
            print(coursework)
            UserCourseworkMembership.objects.create(user=user, coursework=coursework)


    return render(request,'sis/enroll_module.html', {'form':form })



def assign_module(request):
    if not request.user.is_staff:
        return HttpResponseRedirect('/login_user/')


    students = User.objects.filter(student=True)

    form = AssignModuleForm(request.POST or None)
    if form.is_valid():
        user = User.objects.get(id=request.POST['user'])
        module = Module.objects.get(id=request.POST['module'])

        UserModuleMembership.objects.create(user=user, module=module)


    return render(request,'sis/enroll_module.html', {'form':form, 'students':students})
