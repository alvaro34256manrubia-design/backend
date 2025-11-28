from django.shortcuts import render, redirect, get_object_or_404
from .models import Game 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

@login_required
def games_list(request):
    # Obtener todas las salas activas y del usuario
    games = Game.objects.all().order_by('-id')
    
    if request.method == "POST":
        room_name = request.POST.get("room_name", "").strip()
        if room_name:
            if Game.objects.filter(room_name=room_name).exists():
                messages.error(request, "❌ Ya existe una sala con ese nombre. Por favor, elige otro.")
            else:
                game = Game.objects.create(room_name=room_name, owner=request.user)
                messages.success(request, f"✅ Sala '{room_name}' creada exitosamente!")
                return redirect('Games:game_detail', room_name=room_name)
        else:
            messages.error(request, "❌ Debes ingresar un nombre para la sala.")
    
    return render(request, 'games_list.html', {'games': games})

@login_required
def game_detail(request, room_name):
    game = get_object_or_404(Game, room_name=room_name)
    
    # Unirse al juego si hay espacio y no es el owner
    if game.player2 is None and request.user != game.owner:
        game.player2 = request.user
        game.save()
        messages.success(request, f"🎮 Te has unido a la sala como Jugador 2!")
    
    # Procesar movimiento
    if request.method == "POST" and not game.over:
        try:
            square = int(request.POST.get("square", -1))
            if 0 <= square <= 8:
                success = game.make_move(request.user, square)
                if success:
                    # Verificar si el juego terminó después del movimiento
                    if game.over:
                        if game.winner:
                            messages.success(request, f"🎉 ¡{game.winner} gana el juego!")
                        else:
                            messages.info(request, "🤝 ¡El juego terminó en empate!")
                    else:
                        messages.success(request, "✅ Movimiento realizado!")
                else:
                    messages.error(request, "❌ Movimiento inválido. No es tu turno o la casilla está ocupada.")
            else:
                messages.error(request, "❌ Movimiento inválido.")
        except (ValueError, TypeError):
            messages.error(request, "❌ Error en el movimiento.")
    
    # Preparar el tablero para el template
    board = list(game.board)
    
    return render(request, 'games_room.html', {
        'game': game, 
        'board': board,
        'user': request.user
    })

@login_required
def delete_game(request, room_name):
    game = get_object_or_404(Game, room_name=room_name)
    if request.user == game.owner:
        game_name = game.room_name
        game.delete()
        messages.success(request, f"🗑️ Sala '{game_name}' eliminada exitosamente!")
    else:
        messages.error(request, "❌ Solo el creador de la sala puede eliminarla.")
    return redirect('Games:games_list')