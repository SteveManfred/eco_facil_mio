from django.db import models
from productos.models import Producto

class Proveedores(models.Model):  
    nombre = models.CharField(max_length=100)   
    direccion= models.CharField(max_length=15)
    @classmethod
    def total_proveedores(cls):
        return cls.objects.count()

class Compras(models.Model):
    proveedores = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    sub_total = models.FloatField(default=0) 
    descuento = models.FloatField(default=0) 
    total = models.FloatField(default=0) 

class Detalle_orden(models.Model):
    compra = models.ForeignKey(Compras, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio = models.FloatField(default=0)
    sub_total_detalle = models.FloatField(default=0)
    descuento_detalle = models.FloatField(default=0)
    total_detalle = models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.producto)
    
