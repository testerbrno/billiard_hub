from django.db import models
from django.contrib.auth.models import AbstractUser

class Player(AbstractUser):
    email = models.EmailField(('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
