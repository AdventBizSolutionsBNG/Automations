from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('getAllDashboards/', views.get_all_dashboards, name='get_all_dashboards'),
    # path('/pe/<pe_instance_id>/', views.get_pe_details, name="get_pe_details"),
    # path('/pe/<pe_instance_id>/<customer_id>/', views.get_customer_details, name="get_customer_details"),
    # path('/pe/<pe_instance_id>/<customer_id>/<site_id>', views.get_site_details, name="get_site_details"),
    # path('/pe/<pe_instance_id>/<customer_id>/<site_id>/<env_instance_id>/', views.get_env_details, name="get_env_details"),
    # path('/pe/<pe_instance_id>/<customer_id>/<site_id>/<env_instance_id>/<module_id>', views.get_module_details, name="get_module_details"),

]