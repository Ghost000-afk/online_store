from django.urls import path
from . import views


urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('categories/<int:category_id>/products/', views.product_list, name='product_list'),
    path('products/<int:pk>', views.product_detail, name='product_detail'),
    path('search/', views.search_products, name='search_products')
]