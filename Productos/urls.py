from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [ 
    path('', views.product_list_view, name='lista'),
]