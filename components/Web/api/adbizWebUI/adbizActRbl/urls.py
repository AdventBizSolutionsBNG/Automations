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
    path('actrbl_customer_collections/<dashboard_code>/', views.get_actrbl_customer_collections, name='actrbl_customer_collections'),
    path('actrbl_ageing_report/<dashboard_code>/', views.get_actrbl_ageing_report, name='actrbl_ageing_report'),
    path('actrbl_goods_invoiced_dispatch_comparision/<dashboard_code>/', views.get_actrbl_goods_invoiced_dispatch_comparision, name='actrbl_goods_invoices_dispatch_comparision'),
    path('actrbl_customer_sales_vs_collections/<dashboard_code>/', views.get_actrbl_customer_sales_vs_collections, name='actrbl_customer_sales_vs_collections'),
    path('actrbl_customer_planned_vs_actuals/<dashboard_code>/', views.get_actrbl_customer_planned_vs_actuals, name='actrbl_customer_planned_vs_actuals'),
    #
]

# TemplateView.as_view(template_name='actrbl_index.html')