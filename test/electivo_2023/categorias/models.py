from django.db import models

class Categorias(models.Model):  
    nombre = models.CharField(max_length=100)  
    def __str__(self):
        return self.nombre
    @classmethod
    def total_categorias(cls):
        return cls.objects.count()  
