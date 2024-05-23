from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView

app_name ='survey'
urlpatterns = [
    path('', views.index, name='index'),
    path('recommendations/', views.recommend_products, name='recommendations'),
]

