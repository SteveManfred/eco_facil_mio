from django.db import models
from categorias.models import Categorias


class Producto(models.Model):  
    nombre = models.CharField(max_length=100)  
    cantidad = models.CharField(max_length=3)  
    material= models.CharField(max_length=15)  
    categoria= models.ForeignKey(Categorias,on_delete=models.CASCADE)  
    @classmethod
    def total_productos(cls):
        return cls.objects.count()

