from django.shortcuts import render, redirect
from autenticacion import models as autenticacion
from django.contrib.auth.models import User
from . import models

# Create your views here.
def landingAdmon(request):
    return render(request, "landingAdmon.html")

def crearProyecto(request):
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
            departamento = request.POST['departamento']
            ciudad = request.POST['ciudad']

            idUsuarioAutenticado = autenticacion.Perfil.objects.filter(id = idUsuario).values_list('id', flat= True)
            
            registroEmpresa = models.Empresa.objects.create(nit = nit, nombreEmpresa = nombreEmpresa, direccion = direccion,
                                                            departamento = departamento, ciudad = ciudad, usuarioVinculado_id = idUsuarioAutenticado[0])
            registroEmpresa.save()
            return redirect(landingAdmon)
        
        return render(request, "crearEmpresas.html")
