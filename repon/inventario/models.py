from django.db import models
from administracion.models import Proyecto
from django.contrib.auth.models import User

# Create your models here.

class Insumo(models.Model):
    codigo = models.CharField(max_length=15)
    referencia = models.CharField(max_length=150)
    unidad = models.CharField(max_length=100)
    cantidad = models.FloatField()
    valorUnitario = models.FloatField()
    impuesto = models.CharField(max_length=5, default='Si')
    nombreMarca = models.CharField(max_length=200)
    tipoInsumo = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200)
    fechaIngreso = models.DateTimeField(auto_now_add=True)
    fechaCaducidad = models.DateTimeField(null=True)
    fechaCompra = models.DateTimeField()
    observaciones = models.CharField(max_length=300, default='') 
    proyectoAsociado = models.ForeignKey(Proyecto, on_delete=models.CASCADE)