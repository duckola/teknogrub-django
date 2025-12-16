from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.settings_view, name='settings'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
]

