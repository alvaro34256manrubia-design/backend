from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product



@login_required(login_url="/users/login/")
def product_list__view(request):
    products = Product.objects.filter(user=request.user)
    return render(request, 'product_list.html', {'productos': 'home'})

