from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model

# from django.forms import widgets


#from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import *

User = get_user_model()


class DateInput(forms.DateInput):
    input_type = 'date'


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['name', 'description']


class MyRadioSelect(forms.RadioSelect):
    template_name = 'sis/my_widgets/radio.html'

class CourseworkCompletedForm(forms.ModelForm):
    class Meta:
        model = UserCourseworkMembership
        fields = ['percentage']

        widgets = {
            'percentage': MyRadioSelect(),

        }





class CourseworkForm(forms.ModelForm):
    class Meta:
        model = Coursework
        fields = ['title', 'description', 'start', 'end', 'percentage', 'module']
        widgets = {
        'start' : DateInput(),
        'end' : DateInput(),
        }
    def __init__(self,  *args, user=None, **kwargs ):
        super(CourseworkForm, self).__init__(*args,**kwargs)

        if user:
            modules = UserModuleMembership.objects.filter(user=user)
            qr = Module.objects.none()

            for module in modules:
                print(module.module)
                qr =  qr | Module.objects.filter(name=module.module)
            self.fields['module'].queryset = qr


class UserModuleForm(forms.ModelForm):
    class Meta:
        model = UserModuleMembership
        fields = ['user','module']

    def __init__(self,  *args, **kwargs ):
        super(UserModuleForm, self).__init__(*args,**kwargs)
        self.fields['user'].queryset = User.objects.filter(student=True)

class AssignModuleForm(forms.ModelForm):
    class Meta:
        model = UserModuleMembership
        fields = ['user','module']

    def __init__(self,  *args, **kwargs ):
        super(AssignModuleForm, self).__init__(*args,**kwargs)
        self.fields['user'].queryset = User.objects.filter(professor=True)




class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email', 'password']



class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'student', 'professor', 'staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
