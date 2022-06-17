from os import name
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser, User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.apps import apps

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def _create_user(self, phone, email,  password, username,  **extra_fields):
        if not phone:
            raise ValueError('Пожалуйста, введите номер')
        email = self.normalize_email(email)
        user = self.model(phone=phone, email=email, **extra_fields)
        user.password = make_password(password)
        user.username = username
        user.save(using=self._db)
        return user

    def create_user(self, phone, username, email=None, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', False)
        # extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, email, password, username, **extra_fields)

    def create_superuser(self, phone=None, email=None, password=None, username=None, **extra_fields):
        user = self.create_user(phone, email, username, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def update_user(self, *args, **kwargs):
        return 'ok'

class CustomUser(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(unique=True,max_length=500)
    objects = CustomUserManager()
    USERNAME_FIELD = 'phone'

class Contact(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    email = models.EmailField()
    web = models.CharField(max_length=500)


class UserAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=500)
    country = models.CharField(max_length=500)
