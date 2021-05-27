from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname'] #will be required @createsuperuser command

    objects = UserManager()

    def __str__(self):
        return self.nickname
