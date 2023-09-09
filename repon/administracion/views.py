from django.shortcuts import render, redirect
from autenticacion import models as autenticacion
from django.contrib.auth.models import User
from . import models

# Create your views here.
def landingAdmon(request):
    return render(request, "landingAdmon.html")

def crearProyecto(request):
    
    if request.method == 'POST':

        nombreProyecto = request.POST['nombreProyecto']
        estadoProyecto = request.POST['estadoProyecto']
        direccion = request.POST['direccion']
        departamento = request.POST['departamento']
        ciudad = request.POST['ciudad']

        idUsuario = request.user.id
        idEmpresaAutenticada = models.Empresa.objects.filter(usuarioVinculado_id = idUsuario).values_list('id', flat= True)
        registroProyecto = models.Proyecto.objects.create(nombreProyecto = nombreProyecto, estadoProyecto = estadoProyecto, 
                                                            direccion = direccion, departamento = departamento, ciudad = ciudad, 
                                                            empresaVinculada_id = idEmpresaAutenticada[0])
        registroProyecto.save()
        return redirect(landingAdmon)

    return render(request,'crearProyecto.html')

def crearCoordinador(request):
    return render(request,'crearCoordinador.html')

def crearEmpresas(request):
    idUsuario = request.user.id
    empresa = models.Empresa.objects.filter(usuarioVinculado_id = idUsuario).exists()
    
    if empresa:
        return redirect(landingAdmon)

    else:
        if request.method == 'POST':

            nit = request.POST['nit']
            nombreEmpresa = request.POST['nombre']
            direccion = request.POST['direccion']
            correo = request.POST['correo']
            telefono = request.POST['telefono']

            idUsuarioAutenticado = autenticacion.Perfil.objects.filter(id = idUsuario).values_list('id', flat= True)
            registroEmpresa = models.Empresa.objects.create(nit = nit, nombreEmpresa = nombreEmpresa, direccion = direccion,
                                                            correo = correo, telefono = telefono, usuarioVinculado_id = idUsuarioAutenticado[0])
            registroEmpresa.save()
            return redirect(landingAdmon)
        
        return render(request, "crearEmpresas.html")
