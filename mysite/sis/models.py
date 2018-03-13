from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
    )

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_student=False, is_professor=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        user_obj = self.model(
            email = self.normalize_email(email),
        )

        user_obj.set_password(password) # change user password
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.professor = is_professor
        user_obj.student = is_student
        user_obj.save(using=self._db)
        return user_obj

    def create_studentuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_student=True,
            )
        return user

    def create_professoruser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_professor=True,
            )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
         )
        return user

class User(AbstractBaseUser):
    email     = models.EmailField(max_length=255, unique=True)
    # name      = models.CharField(max_length=255, blank=True, null=True)
    # surname   = models.CharField(max_length=255, blank=True, null=True)
    #timestamp = models.DateTimeField(auto_now_add=True)

    # able to login
    active    = models.BooleanField(default=True)
    # student
    student     = models.BooleanField(default=False)
    # professor user non superuser
    professor    = models.BooleanField(default=False)
    # superuser
    staff       = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELD = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        return ('%s %s') % (self.name, self.surname)

    @property
    def is_student(self):
        return self.student
    @property
    def is_professor(self):
        return self.professor
    @property
    def is_staff(self):
        return self.staff
    @property
    def is_active(self):
        return self.active


class Module(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Coursework(models.Model):
    title = models.CharField(max_length=255, unique=True)
    start = models.CharField(max_length=255, default="unspecified")
    end = models.CharField(max_length=255, default="unspecified")
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s"  % (self.module, self.title)

class UserModuleMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    def __str__(self):
        return ("%s %s" % (self.user, self.module))
