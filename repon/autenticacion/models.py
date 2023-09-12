from django.contrib.auth.models import User
from django.db import models

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cargo = models.BooleanField(default=False)
    nombreCargo = models.CharField(max_length=50)
    celular = models.CharField(max_length=50, null=True)
    
