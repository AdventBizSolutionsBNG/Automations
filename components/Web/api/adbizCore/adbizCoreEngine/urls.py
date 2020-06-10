from django.urls import path, include
from . import views

urlpatterns = [
    path('DataLake/', views.get_data_lake_storage_details, name="get_data_lake_storage_details"),
    # path('sync/<pe>/', views.sync_hub, name="sync_hub"),
    # path('<ce>/', views.get_ce_details, name="get_ce_details"),
    # path('<ce>/', views.add_site, name="add_site"),
    # path('<ce>/<customer_code>/', views.get_customer_details, name="get_customer_details"),
    # path('ce/<customer_code>/<site_id>', views.get_site_details, name="get_site_details"),
    # path('ce/<customer_code>/<site_id>/<env_id>/', views.get_env_details, name="get_env_details"),
    # path('ce/<customer_code>/<site_id>/<env_id>/<module_id>', views.get_module_details, name="get_module_details"),

]