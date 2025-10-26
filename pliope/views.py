from django.shortcuts import render
from .models import Person

def pliopefun(request):
    return render(request, 'lista.html')

def person(request, slug):
    try:
        my_person = Person.objects.get(slug=slug)
    except Person.DoesNotExist:
         return render(request, 'error.html')    
    return render(request, 'person.html', {'person': my_person})
