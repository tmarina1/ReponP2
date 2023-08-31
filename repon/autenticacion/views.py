from django.shortcuts import render
from django.contrib import messages
from .  import models

def registro(request):
    
    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        clave = request.POST['clave']
        clave_repeat = request.POST['clave_repeat']
        cargo = ""
        empresa = ""

        if clave != clave_repeat:
            messages.info(request, 'Las contraseñas no coinciden')
        else:
            agregar = models.Usuario(nombre = nombre, correo = correo, cargo = cargo, empresa = empresa ,clave = clave)
            agregar.save()
            return render(request, 'autenticacion/registro.html')
        
    return render(request, 'autenticacion/registro.html')
