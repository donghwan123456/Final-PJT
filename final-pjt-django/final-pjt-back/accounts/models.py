from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    address = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    assets = models.IntegerField(blank=True, null=True)
    goal = models.IntegerField(blank=True, null=True)