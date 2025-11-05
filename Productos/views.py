from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Productos



@login_required(login_url="/users/login/")
def product_list_view(request):
    products = Productos.objects.filter(user=request.user)
    return render(request, 'product_list.html', {'productos': 'products'})

