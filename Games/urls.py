from django.urls import path
from . import views

app_name = 'Games'

urlpatterns = [
    path('', views.games_list, name='games_list'),
    path('<str:room_name>/', views.game_detail, name='game_detail'),
    path('<str:room_name>/delete/', views.delete_game, name='delete_game'),
]