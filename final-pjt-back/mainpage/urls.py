from django.urls import path
from . import views

app_name = 'mainpage'

urlpatterns = [
    path('', views.mainpage, name='mainpage'),  # 메인 페이지 뷰
]
