from django import forms
from . import models


class UploadProductos(forms.ModelForm):
    class Meta:
        model = models.Productos
        fields = ['name','price','description','category']