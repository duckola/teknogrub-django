from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_payment_method, name='add_payment_method'),
    path('delete/<int:method_id>/', views.delete_payment_method, name='delete_payment_method'),
]