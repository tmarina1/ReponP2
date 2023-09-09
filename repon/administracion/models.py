from django.db import models
from autenticacion import models as usuarios
from . import models as administracion

class Empresa(models.Model):
    nit = models.CharField(max_length=50)
    nombreEmpresa = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50)
    usuarioVinculado = models.ForeignKey(usuarios.Perfil, on_delete=models.CASCADE, null=True)

class Proyecto(models.Model):
    nombreProyecto = models.CharField(max_length=50)
    estadoProyecto = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100, default='NA')
    departamento = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    empresaVinculada = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)

