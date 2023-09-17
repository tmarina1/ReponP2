from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from . import models
from administracion.views import crearEmpresas, landingAdmon
from inventario.views import landingCoordinador

'''
Este método tiene la función de mostrar la página principal de la página web.
'''
def inicio(request):
    logout(request)
    return render(request, 'autenticacion/inicio.html')

'''
Este método tiene como propósito mostrar la página de registro de usuarios administradores. 
En primer lugar, verifica que las contraseñas ingresadas coincidan. Si coinciden, procede a 
comprobar si el usuario ya ha sido registrado previamente. Si el usuario aún no ha sido registrado, 
se le permite crear una cuenta de usuario administrador. Sin embargo, si el usuario ya existe en el sistema, 
se impide la creación de un duplicado y no se permite el registro.
'''
def registro(request):
    logout(request)
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

'''
Este método facilita el inicio de sesión para los usuarios con roles de administrador y coordinador. 
Comienza por verificar si el usuario que intenta iniciar sesión existe en el sistema y si la información 
proporcionada coincide con la registrada previamente. Si los datos son correctos, el usuario es redirigido 
a su respectiva página principal, según su rol (administrador o coordinador). En caso de que los datos no 
coincidan o no exista el usuario, se muestra un mensaje de error que invita al usuario a intentarlo nuevamente.
'''
def inicioSesion(request):
    logout(request)
    if request.method == 'POST':
        usuario = request.POST['correo']
        clave = request.POST['clave']
        usuarioAut = authenticate(request, username=usuario, password=clave)
        
        if usuarioAut is not None:
            usuario = User.objects.get(email = usuario)
            perfil = models.Perfil.objects.get(id = usuario.id)
            cargo = perfil.cargo
            login(request, usuarioAut)
            if cargo:
                return redirect(crearEmpresas)
            else:
                return redirect(landingCoordinador)
        else:
            mensaje = "Información incorrecta. Inténtalo de nuevo."
            return render(request, 'autenticacion/inicioSesion.html', {'mensaje': mensaje})
    return render(request,'autenticacion/inicioSesion.html')

'''
Este método tiene como objetivo mostrar la página de recuperación de contraseña. En esta página, 
los usuarios pueden iniciar el proceso de restablecimiento de su contraseña en caso de haberla olvidado o perdido.
'''
def recuperarClave(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        mensaje = "Si el correo es valido, te enviaremos para recuperar contraseña, por favor revisa el correo spam"
        

    return render(request, 'autenticacion/recuperarClave.html',{'mensaje': mensaje})
