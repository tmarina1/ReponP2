from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from .  import models

def registro(request):
    
    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        clave = request.POST['clave']
        claveRepetida = request.POST['claveRepetida']
        administrador = 1
        if clave != claveRepetida:
            messages.warning(request, 'Las contraseñas no coinciden')
        else:
            usuario = User.objects.create_user(first_name=nombre,username=correo, email=correo, password=clave,is_superuser=administrador)
            usuario.save()
            messages.success(request, 'Usuario creado exitosamente')
        
    return render(request, 'autenticacion/registro.html')
