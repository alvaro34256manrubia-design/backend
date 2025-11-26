from django.urls import path
from . import views

app_name= 'Games'

urlpatterns = [
    path('', views.games_list, name='games_list'),
    path('<str:room_name>/', views.game_detail, name='game_detail'),
    path('<str:room_name>/room/', views.game_detail, name='games_room'),
    
]