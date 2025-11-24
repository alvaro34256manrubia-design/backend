from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Game(models.Model):
    room_name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_games')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player2_games', blank=True, null=True)
    board = models.CharField(max_length=9, default="-" * 9)
    active_player = models.IntegerField(default=1)
    winner = models.CharField(max_length=10, blank=True, null=True)
    current_player = models.IntegerField(default=1)
    over = models.BooleanField(default=False)
    
    def __str__(self):
        return self.room_name
    
    def make_move(self, user, position):
        if self.over or self.board[position] != "-": 
            return False
        if self.active_player == 1 and user == self.owner:
            token = 'X'
        elif self.active_player == 2 and user == self.player2:
            token = 'O'
        else:
            return False

        board_list = list(self.board)
        board_list[position] = token
        self.board = "".join(board_list)
        
        winner_token = self.check_winner()
        if winner_token:
            self.winner = self.owner.username if winner_token == 'X' else self.player2.username
            self.over = True
        elif "-" not in self.board:
            self.winner = "Empate"
            self.over = True
        else:
            self.active_player = 2 if self.active_player == 1 else 1
            
        self.save()
        return True
    
    def check_winner(self):
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # filas
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columnas
            [0, 4, 8], [2, 4, 6]              # diagonales
        ]
        b= self.board
        for line in wins:
            a, b1, c = line
            if b[a] != "-" and b[a] == b[b1] == b[c]:
                return b[a]
        return None
            
            