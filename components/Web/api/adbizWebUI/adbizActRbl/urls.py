from django.urls import path
from . import views
from django.views.generic.base import TemplateView


urlpatterns = [
    path(r'home/', TemplateView.as_view(template_name='actrbl_index.html'), name='home'),
    #path(r'sales_forecast/', views.get_actrbl_sales_forecast, name='sales_forecast'),
]