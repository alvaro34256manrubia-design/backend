from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm



def users(request):
    return render(request, 'users.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("users:home")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form })

