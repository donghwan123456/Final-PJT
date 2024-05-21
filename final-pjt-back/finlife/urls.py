from django.urls import path
from . import views

app_name = "finlife"
urlpatterns = [
    path('', views.index, name="index"),
    path('deposit_products/', views.deposit_products, name="deposit_products"),
    path('deposit_product_options/<str:fin_prdt_cd>/', views.deposit_product_options, name="deposit_product_options"),
    path('top_rate/', views.top_rate, name="top_rate"),
    path('sort_rate/', views.sort_rate, name="sort_rate"),
    path('filter/', views.filter, name="filter"),
    # path('deposit_products/sort_rate/', views.sort_rate, name="sort_rate"),
]