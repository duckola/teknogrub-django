from django.urls import path
from . import views

urlpatterns = [
    # This is the line Django was looking for: name='checkout'
    path('checkout/', views.checkout_view, name='checkout'),

    path('cart/', views.cart_view, name='cart'),
    path('', views.order_history_view, name='order-history'),
    path('kitchen/', views.kitchen_dashboard_view, name='kitchen_dashboard'),
]