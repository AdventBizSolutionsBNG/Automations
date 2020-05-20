from django.urls import path, include
from .models import ContactUs
from . import views


urlpatterns = [

    #path('ContactUs/', views.contact_us, name="contact_us"),
    #path('\viewProductEngine\<int:productId>, views.index, name='index'),
    path("activate/", views.activate, name="activate"),
    # path("sync/", views.sync_details, name="sync_details"),
    # path("customer/add/<pe>/", views.add_customer, name="add_customer"),
]