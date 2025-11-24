import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import TicTacToeGame, GameMessage

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'game_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'chat_message':
            await self.handle_chat_message(data)
        elif message_type == 'game_move':
            await self.handle_game_move(data)

    async def handle_chat_message(self, data):
        message = await self.save_message(data['room_id'], data['user_id'], data['message'])
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': data['message'],
                'username': data['username'],
                'timestamp': message.timestamp.isoformat()
            }
        )

    async def handle_game_move(self, data):
        game_data = await self.process_game_move(
            data['room_id'], 
            data['square_index'], 
            data['user_id']
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_update',
                'game_data': game_data
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp']
        }))

    async def game_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game_update',
            'game_data': event['game_data']
        }))

    @database_sync_to_async
    def save_message(self, room_id, user_id, message):
        game = TicTacToeGame.objects.get(id=room_id)
        user = User.objects.get(id=user_id)
        return GameMessage.objects.create(
            game=game,
            user=user,
            message=message
        )

    @database_sync_to_async
    def process_game_move(self, room_id, square_index, user_id):
        game = TicTacToeGame.objects.get(id=room_id)
        user = User.objects.get(id=user_id)
        if (user == game.owner and game.active_player == 'X') or \
           (user == game.player2 and game.active_player == 'O'):
            
            if game.board[square_index] == '' and game.game_state == 'active':
                game.board[square_index] = game.active_player
                
                winner = game.check_winner()
                if winner:
                    game.game_state = 'won_p1' if winner == 'X' else 'won_p2'
                elif game.is_board_full():
                    game.game_state = 'tie'
                else:
                    game.active_player = 'O' if game.active_player == 'X' else 'X'
                
                game.save()

        return {
            'board': game.board,
            'active_player': game.active_player,
            'game_state': game.game_state,
            'room_name': game.room_name,
            'owner': game.owner.username,
            'player2': game.player2.username if game.player2 else None
        }