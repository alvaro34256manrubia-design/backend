from django.contrib import admin
from .models import TicTacToeGame, GameMessage

@admin.register(TicTacToeGame)
class TicTacToeGameAdmin(admin.ModelAdmin):
    list_display = ['room_name', 'owner', 'player2', 'game_state', 'active_player', 'created_at']
    list_filter = ['game_state', 'created_at']
    search_fields = ['room_name', 'owner__username']

@admin.register(GameMessage)
class GameMessageAdmin(admin.ModelAdmin):
    list_display = ['game', 'user', 'message', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['user__username', 'message']