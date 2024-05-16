from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            'username',
            'password',
            'address',
            'birthday',
            'assets',
            'goal',
        )
        labels = {
            'username': '사용자명',
            'password': '비밀번호',
            'address': '주소',
            'birthday': '생년월일',
            'assets': '자산',
            'goal': '목표',
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'email',
        )

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'address',
            'birthday',
            'assets',
            'goal',
        )
        labels = {
            'username': '사용자명',
            'password': '비밀번호',
            'address': '주소',
            'birthday': '생년월일',
            'assets': '자산',
            'goal': '목표',
        }