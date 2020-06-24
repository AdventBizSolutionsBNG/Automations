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
    path('actrbl/salesForecast/',views.get_actrbl_sales_forecast , name="actrbl_sales_forecast"),
]

#TemplateView.as_view(template_name='actrbl_sales_forecast.html')