from django.urls import path

from . import views


urlpatterns =[
    path('register/', views.register_company, name='register_company'),
    path('dashboard/', views.company_dashboard, name='company_dashboard'),
    path('add_product', views.add_product, name='add_product'),
    path('product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
]