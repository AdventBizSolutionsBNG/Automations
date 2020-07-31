from django.urls import path
from . import views
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('home/', views.load_home_page, name='home'),
    path(r'', views.CustomLogin.as_view(), name='login'),
    path('login/', views.CustomLogin.as_view(), name='login'),
    path('logout/', views.custom_Logout, name='logout'),
    path('activate/', views.activation, name="activation"),
    #path('actrbl/salesForecast/',views.get_actrbl_sales_forecast , name="actrbl_sales_forecast"),
    #path('actrbl/salesSummary/',views.get_actrbl_sales_summary , name="actrbl_sales_summary"),
    #path('actrbl/salesException/',views.get_actrbl_sales_exception , name="actrbl_sales_exception"),
    # path('getComponentData/', views.get_component_data, name="get_component_data"),
    # path('getChartData/', views.get_chart_data, name="get_chart_data"),
    # path('getTableData/', views.get_table_data, name="get_table_data")
]

#TemplateView.as_view(template_name='actrbl_sales_forecast.html')