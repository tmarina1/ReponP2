from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect
from . import models

def registro(request):
    colorMensaje = True
    mensaje = ''
    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        clave = request.POST['clave']
        claveRepetida = request.POST['claveRepetida']
        administrador = True
        if clave != claveRepetida:
            mensaje = 'Las contraseñas no coinciden'
        else:
            try:
                usuario = User.objects.create_user(first_name=nombre,username=correo, email=correo, password=clave)
                usuario.save()
                perfil,creado = models.Perfil.objects.get_or_create(usuario=usuario)
                if creado:
                    perfil.cargo = administrador
                    perfil.save()
                return redirect(inicioSesion)
            except:
               mensaje = 'Ya existe un usuario registrado con este correo'
               colorMensaje = False
        
    return render(request, 'autenticacion/registro.html', {'colorMensaje':colorMensaje,'mensaje':mensaje})

def inicioSesion(request):
    return render(request,'autenticacion/inicioSesion.html')

def inicioSesionCoordinador(request):
    return render(request,'autenticacion/inicioSesionCoordinador.html')
