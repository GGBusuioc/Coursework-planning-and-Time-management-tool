from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

from django.http import HttpResponseRedirect

from sis.forms import UserForm
from django.template import RequestContext

from django.views.generic import View

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_student:
                    return render(request, 'sis/student_home.html')
                elif user.is_professor:
                    return render(request, 'sis/professor_home.html')
                elif user.is_staff:
                    return render(request, 'sis/staff_home.html')
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

# class UserFormView(View):
#     form_class = UserForm
#     template_name = 'sis/registration_form.html'
#     #display blank form
#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form':form})
#
#     # process form data
#     @csrf_protect
#     def post(self, request):
#         form = self.form_class(request.POST)
#
#         if form.is_valid():
#             # create an object from the form
#             # without saving it to the database
#             user = form.save(commit=False)
#             # cleaned (normalized) data
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#
#             user.set_password(password)
#             # save to the database
#             user.save()
#
#             user = authenticate(email=email, password=password)
#             if user is not None:
#                 if user.is_active:
#                     # now logged in
#                     login(request, user)
#                     # request.user.
#                     return redirect('sis:index')
#         return render(request, self.template_name, {'form':form})
