from django.urls import path
from . import views

app_name = 'exchange_app'
urlpatterns = [
    path('', views.home, name='home'),
    path('calculator/', views.calculator, name='calculator'),
]
