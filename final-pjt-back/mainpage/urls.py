from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage, name='mainpage'),  # 메인 페이지 뷰
]