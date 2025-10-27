from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm



def users(request):
    return render(request, 'register.html')


def register_view(request):
    form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form })

