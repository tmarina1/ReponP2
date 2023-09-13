from django.db import models
from datetime import datetime
from administracion.models import Proyecto
from django.contrib.auth.models import User

# Create your models here.

class Insumo(models.Model):
    fechaActual = datetime.now()
    codigo = models.CharField(max_length=15)
    referencia = models.CharField(max_length=150)
    unidad = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=10, decimal_places=3)
    valorUnitario = models.DecimalField(max_digits=10, decimal_places=2)
    impuesto = models.CharField(max_length=5, default='Si')
    nombreMarca = models.CharField(max_length=200)
    tipoInsumo = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200)
    fechaIngreso = models.DateTimeField(default=fechaActual)
    fechaCaducidad = models.DateTimeField(null=True)
    fechaCompra = models.DateTimeField(default=fechaActual)
    observaciones = models.CharField(max_length=300, default='') 
    proyectoAsociado = models.ForeignKey(Proyecto, on_delete=models.CASCADE)