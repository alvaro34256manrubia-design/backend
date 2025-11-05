from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Productos



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Productos
from .forms import UploadProductos

@login_required(login_url="/users/login/")
def product_list_view(request):
    if request.method == 'POST':
        form = UploadProductos(request.POST)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.user = request.user
            new_product.save()
            return redirect('productos:lista')
    else:
        form = UploadProductos()
    
    products = Productos.objects.filter(user=request.user)[:20]
    return render(request, 'list_product.html', {
        'form': form,
        'productos': products
    })