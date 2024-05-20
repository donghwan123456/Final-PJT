# myapp/urls.py

from django.urls import path
from .views import map_view

app_name ='myapp'
urlpatterns = [
    path('map/', map_view, name='myapp'),  # 빈 문자열로 설정하여 기본 경로로 매핑
]
