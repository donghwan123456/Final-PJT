from django.urls import path
from . import views

app_name = "finlife"
urlpatterns = [
    path('', views.index, name="index"),
    path('products/', views.products, name="products"),
    path('save_deposit_products/', views.save_deposit_products, name="save_deposit_products"),
    path('deposit_products/', views.deposit_products, name="deposit_products"),
    path('deposit_product_options/<str:fin_prdt_cd>/', views.deposit_product_options, name="deposit_product_options"),
    path('deposit_products/top_rate/', views.top_rate, name="top_rate"),
]