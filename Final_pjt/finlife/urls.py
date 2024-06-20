from django.urls import path
from . import views

app_name = "finlife"
urlpatterns = [
    path('', views.index, name="index"),
    path('filter/', views.filter, name="filter"),
    path('compare/', views.compare_products, name='compare'),
    path('<str:product_type>/<int:product_id>/', views.product_detail, name='product_detail'),
    path('enroll/<str:product_type>/<int:product_id>/', views.enroll_product, name='enroll_product'),
]