from django import forms
from .models import TicTacToeGame

class CreateGameForm(forms.ModelForm):
    class Meta:
        model = TicTacToeGame
        fields = ['room_name']
        
    def clean_room_name(self):
        room_name = self.cleaned_data['room_name']
        if TicTacToeGame.objects.filter(room_name=room_name).exists():
            raise forms.ValidationError("Ya existe una sala con este nombre.")
        return room_name

class JoinGameForm(forms.Form):
    room_name = forms.CharField(max_length=100)