from django.urls import path
from . import views
from .models import Person

person_list = Person.objects.all()

app_name="people"

urlpatterns =[
    path('', views.pliopefun, name="lista"),
    path('<slug:slug>', views.person, name='person')
]
