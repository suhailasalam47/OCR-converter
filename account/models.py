from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, username, email, password=None):
        if not email:
            raise ValueError("User must have an email")

        if not username:
            raise ValueError("User must have a username") 

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            username = username,
        )    

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, first_name, username, email, password=None):
        user = self.create_user(
            email= self.normalize_email(email),
            first_name=first_name,
            username=username,
            password=password,
        )   
        user.is_admin = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_active = True
        user.save(using=self._db)
        return user   


class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name",]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

