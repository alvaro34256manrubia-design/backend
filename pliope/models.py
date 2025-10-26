from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=50)
    birth = models.DateField()
    slug = models.SlugField(unique=True, null=False, blank=False)
    propic = models.ImageField (upload_to='Media/', default="Media/default.png", null=True, blank=True)
    
    def __str__(self):
        return self.name
 
class Profesion(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=False, blank=False )
    


