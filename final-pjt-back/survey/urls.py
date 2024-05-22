from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView

app_name ='survey'
urlpatterns = [
    path('', views.index, name='index'),
    # path('thank-you/', TemplateView.as_view(template_name="survey_thank_you.html"), name='thank_you'),
]

