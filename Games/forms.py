from django import forms
from .models import Game

class CreateGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['room_name']
        widgets = {
            'room_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Ingresa el nombre de la sala'
            })
        }
        
    def clean_room_name(self):
        room_name = self.cleaned_data['room_name']
        if Game.objects.filter(room_name=room_name).exists():
            raise forms.ValidationError("Ya existe una sala con este nombre.")
        return room_name

class JoinGameForm(forms.Form):
    room_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500',
            'placeholder': 'Ingresa el nombre de la sala a unirte'
        })
    )