from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class SurveyResponse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.IntegerField()  # age 필드 추가
    asset_ratio = models.CharField(max_length=50)
    expected_return = models.CharField(max_length=50)
    financial_knowledge = models.CharField(max_length=50)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)


