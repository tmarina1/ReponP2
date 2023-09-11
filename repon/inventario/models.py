from django.db import models
from datetime import datetime
from administracion.models import Proyecto

# Create your models here.

class Insumo(models.Model):
    codigo = models.CharField(max_length=15)
    referencia = models.CharField(max_length=150)
    unidad = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=10, decimal_places=3)
    valorUnitario = models.DecimalField(max_digits=10, decimal_places=2)
    impuesto = models.DecimalField(max_digits=5, decimal_places=2,default='19')
    nombreMarca = models.CharField(max_length=200)
    tipoInsumo = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200)
    fechaIngreso = models.DateTimeField(auto_now_add=True)
    fechaCaducidad = models.DateTimeField(default='')
    fechaCompra = models.DateTimeField(default=datetime.now)
    observaciones = models.CharField(max_length=200, default='') 
    proyectoAsociado = models.ForeignKey(Proyecto, on_delete=models.CASCADE)