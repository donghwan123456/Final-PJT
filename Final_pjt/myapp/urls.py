# myapp/urls.py

from django.urls import path
from . import views

app_name ='myapp'
urlpatterns = [
    path('map/', views.map_view, name='map'),  # 빈 문자열로 설정하여 기본 경로로 매핑
]
