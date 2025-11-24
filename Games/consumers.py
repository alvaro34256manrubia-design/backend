import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Game
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

@database_sync_to_async
def get_game_state(game):
    return {
        "board": game.board,
        "active_player": game.active_player,
        "player1": game.owner.username if game.owner else None,
        "player2": game.player2.username if game.player2 else None,
        "winner": game.winner,
        "over": game.over,
        
    }
        
@database_sync_to_async
def get_game(room_id):
    return Game.objects.get(room_name=room_id)

@database_sync_to_async
def get_user(user_id):
    return User.objects.get(id=user_id)

@database_sync_to_async
def make_move(game, user, position):
    return game.make_move(user, position)

@database_sync_to_async
def save_game(game):
    game.save()


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_id = f'game_{self.room_id}'
        
        await self.channel_layer.group_add(
            self.room_group_id,
            self.channel_name
        )
        
        await self.accept()
        game=await get_game(self.room_id)
        await self.send(text_data=json.dumps({
            "game_state": await get_game_state(game)
        }))
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_id,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        game = await get_game(self.room_id)
       
        if 'move' in data and 'user' in data: # comprobacion de usuario y movimiento
            user = await get_user(data['user'])
            success = await make_move(game, user, int(data['move']))
            if success:
                await save_game(game)
        game_state = await get_game_state(game)
        await self.channel_layer.group_send(
            self.room_group_id,
            {
                'type': 'game_message',
                'game_state': game_state
            }
        )
    
    async def game_message(self, event):
        await self.send(text_data=json.dumps({
            'game_state': event['game_state']
        }))
        
    async def send_game_state(self):
        game = Game.objects.get(room_name=self.room_id)
        await self.send(text_data=json.dumps({
            'game_state': await get_game_state(game)
        }))
        