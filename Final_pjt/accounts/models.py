from django.db import models
from django.contrib.auth.models import AbstractUser
from finlife.models import DepositProducts, SavingProducts

# Create your models here.

class User(AbstractUser):
    address = models.TextField(blank=True, null=True, verbose_name="주소")
    birthday = models.DateTimeField(blank=True, null=True, verbose_name="생년월일")
    assets = models.IntegerField(blank=True, null=True, verbose_name="자산")
    Goal = models.IntegerField(blank=True, null=True, verbose_name="목표")
    enrolled_deposit_products = models.ManyToManyField(DepositProducts, blank=True, related_name='enrolled_users')
    enrolled_saving_products = models.ManyToManyField(SavingProducts, blank=True, related_name='enrolled_users')