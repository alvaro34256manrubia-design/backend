from django import forms
from . import models
class UploadProduct(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['name','price','description','category']