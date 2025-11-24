from django.db import models
from django.contrib.auth.models import User

class TicTacToeGame(models.Model):
    GAME_STATES = [
        ('active', 'Activo'),
        ('won_p1', 'Ganó Jugador 1'),
        ('won_p2', 'Ganó Jugador 2'),
        ('tie', 'Empate'),
    ]
    
    room_name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_games')
    player2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='joined_games')
    
    # Tablero: lista de 9 elementos (X, O, o vacío)
    board = models.JSONField(default=list)
    
    active_player = models.CharField(max_length=1, default='X')  # X o O
    game_state = models.CharField(max_length=10, choices=GAME_STATES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"TicTacToe - {self.room_name}"
    
    def save(self, *args, **kwargs):
        if not self.board:
            self.board = [''] * 9  # Tablero vacío de 3x3
        super().save(*args, **kwargs)
    
    def check_winner(self):
        # Combinaciones ganadoras
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
            [0, 4, 8], [2, 4, 6]              # Diagonales
        ]
        
        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ''):
                return self.board[combo[0]]
        return None
    
    def is_board_full(self):
        return '' not in self.board

class GameMessage(models.Model):
    game = models.ForeignKey(TicTacToeGame, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']