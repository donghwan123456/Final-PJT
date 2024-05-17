from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    address = models.TextField(blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    assets = models.IntegerField(blank=True, null=True)
    Goal = models.IntegerField(blank=True, null=True)