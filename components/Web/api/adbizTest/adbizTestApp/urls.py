from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import CountryListView, PersonListView
from . import views

urlpatterns = [
    path('country/<cc>/', views.get_country),
    path('country/', views.country_index),
    path('state/<cc>/<sc>/', views.get_state),
    path('country/ops/upload/', csrf_exempt(views.upload_country)),
    path('country/ops/add/', csrf_exempt(views.add_country)),
    path('countryTable/', views.get_country_table ),
    path('countryLV/', CountryListView.as_view() ),
    path('persons/', PersonListView.as_view() )
]
