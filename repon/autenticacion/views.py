from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from . import models
from administracion.views import crearEmpresas

def registro(request):
    colorMensaje = True
    mensaje = ''
    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        clave = request.POST['clave']
        claveRepetida = request.POST['claveRepetida']
        nombreCargo = request.POST['nombreCargo']
        celular = request.POST['celular']
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
                    perfil.nombreCargo = nombreCargo
                    perfil.celular = celular
                    perfil.save()
                    usuarioAut = authenticate(request, username=usuario, password=clave)
                    if usuarioAut is not None:
                        login(request, usuarioAut)
                        return redirect(crearEmpresas)
            except:
               mensaje = 'Ya existe un usuario registrado con este correo'
               colorMensaje = False
        
    return render(request, 'autenticacion/registro.html', {'colorMensaje':colorMensaje,'mensaje':mensaje})

def inicioSesion(request):
    if request.method == 'POST':
        usuario = request.POST['correo']
        clave = request.POST['clave']
        usuarioAut = authenticate(request, username=usuario, password=clave)
        
        if usuarioAut is not None:
            login(request, usuarioAut)
            return redirect(inicioSesionCoordinador)  # Redirigir a la página principal después del inicio de sesión
        else:
            # Manejo de error en caso de credenciales incorrectas
            mensaje = "Información incorrecta. Inténtalo de nuevo."
            return render(request, 'autenticacion/inicioSesion.html', {'mensaje': mensaje})
    return render(request,'autenticacion/inicioSesion.html')

def recuperarClave(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        mensaje = "Si el correo es valido, te enviaremos para recuperar contraseña, por favor revisa el correo spam"
        

    return render(request, 'autenticacion/recuperarClave.html',{'mensaje': mensaje})
