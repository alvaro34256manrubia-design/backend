from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_external_data, name='external_data'),
    path('posts/', views.get_multiple_posts, name='multiple_posts'),
]