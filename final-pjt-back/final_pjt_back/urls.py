"""
URL configuration for final_pjt_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.views.generic import RedirectView
# from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('api/v1/', include('articles.urls')),
    path('accounts/', include('accounts.urls')),
    path('finlife/', include('finlife.urls')),
    path('articles/', include('articles.urls')),
    path('myapp/', include('myapp.urls')),
    path('survey/', include('survey.urls')),
    path('', RedirectView.as_view(url='/mainpage/', permanent=False)),  # 루트 URL 리디렉션
    path('mainpage/', include('mainpage.urls')),  # 메인 페이지를 제공하는 앱의 URL 설정을 포함
    # path('<int:user_pk>/password/', views.change_password, name='change_password')
]
