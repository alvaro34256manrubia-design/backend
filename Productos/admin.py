from django.contrib import admin
from . import models

@admin.register(models.Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    search_fields = ('name', 'category')
    list_filter = ('category', 'date_published')
    


