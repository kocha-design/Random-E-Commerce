from django.urls import path
from . import views

urlpatterns = [
    # Public / Customer
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),

    # Seller dashboard
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('dashboard/new/', views.product_create, name='product_create'),
    path('dashboard/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('dashboard/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('dashboard/pending/', views.seller_pending, name='seller_pending'),
]