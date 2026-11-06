from django.urls import path
from . import views

urlpatterns = [
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/seller/', views.register_seller, name='register_seller'),
     path('profile/', views.profile_redirect, name='profile')
]