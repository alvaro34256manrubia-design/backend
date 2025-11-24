from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db import models
from .models import TicTacToeGame, GameMessage
from .forms import CreateGameForm, JoinGameForm

@login_required
def games_list(request):
    active_games = TicTacToeGame.objects.filter(game_state='active')
    user_games = TicTacToeGame.objects.filter(
        models.Q(owner=request.user) | models.Q(player2=request.user)
    )
    
    if request.method == 'POST':
        form = CreateGameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.owner = request.user
            game.save()
            messages.success(request, f'Sala "{game.room_name}" creada exitosamente!')
            return redirect('games:game_room', room_id=game.id)
    else:
        form = CreateGameForm()
    
    return render(request, 'games_list.html', {
        'active_games': active_games,
        'user_games': user_games,
        'form': form
    })

@login_required
def game_room(request, room_id):
    game = get_object_or_404(TicTacToeGame, id=room_id)
    messages_list = game.messages.all()[:50]
    
    # Unirse al juego si hay espacio
    if game.player2 is None and request.user != game.owner:
        game.player2 = request.user
        game.save()
        messages.success(request, f'Te has unido a la sala "{game.room_name}"')
    
    return render(request, 'game_room.html', {
        'game': game,
        'messages_list': messages_list,
        'game_data': {
            'room_id': room_id,
            'room_name': game.room_name,
            'board': game.board,
            'active_player': game.active_player,
            'game_state': game.game_state,
            'owner': game.owner.username,
            'player2': game.player2.username if game.player2 else None,
            'current_user': request.user.username,
        }
    })

@login_required
def make_move(request, room_id):
    if request.method == 'POST':
        game = get_object_or_404(TicTacToeGame, id=room_id)
        square_index = int(request.POST.get('square'))
        
        # Verificar si el usuario puede jugar
        if (request.user == game.owner and game.active_player == 'X') or \
           (request.user == game.player2 and game.active_player == 'O'):
            
            # Verificar que la casilla esté vacía
            if game.board[square_index] == '':
                game.board[square_index] = game.active_player
                
                # Verificar ganador
                winner = game.check_winner()
                if winner:
                    game.game_state = 'won_p1' if winner == 'X' else 'won_p2'
                elif game.is_board_full():
                    game.game_state = 'tie'
                else:
                    # Cambiar turno
                    game.active_player = 'O' if game.active_player == 'X' else 'X'
                
                game.save()
                messages.success(request, 'Movimiento realizado!')
        
        return redirect('games:game_room', room_id=room_id)

@login_required
def delete_game(request, room_id):
    game = get_object_or_404(TicTacToeGame, id=room_id)
    if request.user == game.owner:
        game.delete()
        messages.success(request, 'Sala eliminada exitosamente!')
    return redirect('games:games_list')