from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.games_list, name='games_list'),
    path('room/<int:room_id>/', views.game_room, name='game_room'),
    path('room/<int:room_id>/move/', views.make_move, name='make_move'),
    path('room/<int:room_id>/delete/', views.delete_game, name='delete_game'),
]