from django.db import models

class Empresa(models.Model):
    nit = models.CharField(max_length=50)
    nombreEmpresa = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50)

