from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid


class UserManager(BaseUserManager):
    def create_user(self, username: str, first_name: str, last_name: str, email: str,
                    password: str = None, is_staff=False, is_superuser=False) -> "User":
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')

        user            = self.model(email=self.normalize_email(email))
        user.username   = username
        user.first_name = first_name
        user.last_name  = last_name
        user.set_password(password)
        user.is_active  = True
        user.is_staff   = is_staff
        user.is_superuser = is_superuser
        user.save()
        return user

    def create_superuser(self, username: str, first_name: str, last_name: str,
                         email: str, password: str) -> "User":
        user = self.create_user(username, first_name, last_name, email, password, is_staff=True,
                                is_superuser=True)
        return user


class User(AbstractUser):
    id         = models.CharField(default=str(uuid.uuid4()), max_length=255, unique=True,primary_key=True,  editable=False)
    username   = models.CharField(max_length=255, verbose_name='username', unique=True)
    first_name = models.CharField(max_length=255, verbose_name='first name')
    last_name  = models.CharField(max_length=255, verbose_name='last name')
    email      = models.EmailField(max_length=255, verbose_name='Email', unique=True)
    password   = models.CharField(max_length=255, verbose_name='password')

    objects = UserManager()

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        db_table     = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
