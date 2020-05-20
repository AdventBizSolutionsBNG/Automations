from django.urls import path, include
from . import views
from .views import login

urlpatterns = [
    path('registration/', views.login, name="registration"),
]