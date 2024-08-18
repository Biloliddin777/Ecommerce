from django.contrib import admin
from django.urls import path

from ecommerce.views import views

urlpatterns = [
    path('project-management/', views.project_management, name='project_management'),
    path('customers/', views.customers, name='customers'),
    path('customer-details/<int:customer_id>/', views.customer_details, name='customer_details'),
    path('user/profile/', views.profile, name='profile'),
    path('settings/', views.profile_settings, name='profile_settings'),
    path('add-customer/', views.add_customer, name='add_customer'),
    path('edit-customer/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path('delete-customer/<int:customer_id>/', views.delete_customer, name='delete_customer'),
]
