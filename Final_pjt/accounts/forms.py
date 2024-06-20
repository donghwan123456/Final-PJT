from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms

# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = get_user_model()
        
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2', 'address', 'birthday', 'assets', 'Goal')
        labels = {
            'username': '닉네임',
            'password1': '비밀번호',
            'password2': '비밀번호 확인',
            'address': '주소',
            'birthday': '생년월일',
            'assets': '자산',
            'Goal': '목표'
        }
        help_texts = {
            'username': '',
            'password1': '',
            'password2': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['birthday'].widget = forms.DateInput(attrs={'type': 'date'})


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = (
            'username', 
            'address',
            'birthday',
            'assets',
            'Goal',
        )
        labels = {
            'username': '닉네임',
        }
        help_texts = {
            'username': '',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birthday'].widget = forms.DateInput(attrs={'type': 'date'})
        # 비밀번호 필드 제거
        if 'password' in self.fields:
            del self.fields['password']