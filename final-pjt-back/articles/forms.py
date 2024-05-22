from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'content',)
        labels = {
            'title': '제목',
            'content': '내용',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': '제목을 입력하세요',
                'required': True,
            }),
            'content': forms.Textarea(attrs={
                'placeholder': '내용을 입력하세요',
                'required': True,
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
