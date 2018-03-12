from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

from django.http import HttpResponseRedirect

from sis.forms import UserForm
from django.template import RequestContext
from .models import Module

from django.views.decorators.csrf import csrf_exempt

from django.urls import reverse



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
                    return render(request, 'sis/student_home.html')
                    #return redirect('sis.views.index')
                elif user.is_professor:
                    return render(request, 'sis/professor_home.html')
                elif user.is_staff:
                    #return redirect('redirect_test', user=user)
                    return redirect(staff_redirect)
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



def staff_redirect(request):
    print("you here")
    print(request.session['user_id'])
    return HttpResponse("You have been redirected")
