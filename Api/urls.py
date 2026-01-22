from django.urls import path
from . import views

app_name = 'Api'

urlpatterns = [
    path('', views.get_server_status, name='get_server_status'),
    path('Api/ErrorSerializer/', views.get_errors),
    path('Api/ErrorSerializer/<int:code>/', views.get_error_from_code),
]