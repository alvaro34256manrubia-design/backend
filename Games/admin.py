from django.contrib import admin
from .models import Game
# Register your models here.

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'owner', 'active_player', 'winner', 'over')
    list_filter = ('over',)
    search_fields = ('room_name', 'owner_username')