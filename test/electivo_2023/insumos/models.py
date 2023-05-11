from django.db import models



class Insumos(models.Model):  
    nombre = models.CharField(max_length=100) 
    cantidad = models.CharField(max_length=3) 
    material= models.CharField(max_length=15)  
    @classmethod
    def total_insumos(cls):
        return cls.objects.count()  
