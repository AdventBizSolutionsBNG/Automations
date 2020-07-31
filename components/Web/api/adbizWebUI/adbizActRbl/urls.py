from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path(r'home/<dashboard_code>/', views.get_actrbl_home , name='actrbl_index'),
    path('actrbl_sales_summary/<dashboard_code>/', views.get_actrbl_sales_summary, name='actrbl_sales_summary'),
    path('actrbl_sales_forecast/<dashboard_code>/', views.get_actrbl_sales_forecasts, name='actrbl_sales_forecasts'),
    path('actrbl_discounted_invoices/<dashboard_code>/', views.get_actrbl_discounted_invoices, name='actrbl_discounted_invoices'),
    path('actrbl_sales_exceptions/<dashboard_code>/', views.get_actrbl_sales_exceptions, name='actrbl_sales_exceptions'),
    path('actrbl_sales_trends/<dashboard_code>/', views.get_actrbl_sales_trends, name='actrbl_sales_trends'),
]

# TemplateView.as_view(template_name='actrbl_index.html')