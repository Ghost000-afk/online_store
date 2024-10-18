from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('list/', views.order_list, name='order_list'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('payment/error/', views.payment_error, name='payment_error'),
    path('payment/<int:order_id>/', views.process_payment, name='process_payment'),
    path('cash_on_delivery/<int:order_id>/', views.cash_on_delivery, name='cash_on_delivery'),
    path('payment/error/', views.payment_error, name='payment_error'),
]