from django.shortcuts import render 
from pliope.models import Person

def homepage(request):
    person_list = Person.objects.all()
    return render (request, 'home.html',  {'person_list': person_list} )


