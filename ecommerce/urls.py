from django.contrib import admin
from django.urls import path

from ecommerce.views import views

urlpatterns = [
    path('project-management/', views.project_management, name='project_management'),
    path('customers/', views.CustomerModelFormView.as_view(), name='customers'),
    path('customer-details/<int:customer_id>/', views.CustomerDetailsView.as_view(), name='customer_details'),
    path('user/profile/', views.profile, name='profile'),
    path('settings/', views.profile_settings, name='profile_settings'),
    path('add-customer/', views.CustomerCreateView.as_view(), name='add_customer'),
    path('edit-customer/<int:customer_id>/', views.CustomerUpdateView.as_view(), name='edit_customer'),
    path('delete-customer/<int:customer_id>/', views.CustomerDeleteView.as_view(), name='delete_customer'),
]
