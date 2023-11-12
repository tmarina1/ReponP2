from django.db import models
from administracion.models import Proyecto
from django.contrib.auth.models import User
from autenticacion.models import Perfil
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
    categoria = models.CharField(max_length=300, default='') 
    proyectoAsociado = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

class TransferenciaInsumo(models.Model):
    coordinadorSolicitante = models.ForeignKey(Perfil, related_name='coordinadorSolicitante', on_delete=models.CASCADE)
    administrador = models.ForeignKey(Perfil, related_name='administrador', on_delete=models.CASCADE)
    proyectoOrigen = models.ForeignKey(Proyecto, related_name='proyectoOrigen', on_delete=models.CASCADE)
    proyectoDestino = models.ForeignKey(Proyecto, related_name='proyectoDestino', on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cantidad = models.FloatField()
    estado = models.CharField(default='Pendiente', max_length=15)
    costoTransferencia = models.FloatField(default=0, max_length=15)

class CostosProyecto(models.Model):
    valor = models.FloatField()
    tipo = models.CharField(max_length=15)
    observaciones = models.CharField(max_length=300, default='')
    proyectoAsociado = models.ForeignKey(Proyecto, on_delete=models.CASCADE)