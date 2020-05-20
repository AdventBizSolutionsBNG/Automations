from django.urls import path

from . import views

urlpatterns = [
    path('', views.product_engine_index, name='product_engine_index'),
    #path('\viewProductEngine\<int:productId>, views.index, name='index'),
]