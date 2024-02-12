from django.db import models
#! extends current user with abstract user
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []