from django.shortcuts import render
from administracion.models import Proyecto
from autenticacion.models import User

def inventario(request):
    return render(request, "inventario.html")

def landingCoordinador(request):
    idUsuario = request.user.id
    idEmpresa = Proyecto.objects.filter(coordinadorVinculado_id = idUsuario).values_list('empresaVinculada_id', flat= True)
    proyectos = Proyecto.objects.filter(empresaVinculada_id = idEmpresa[0])
    return render(request, "landingCoordinador.html", {'proyectos':proyectos})

def opcionesCoordinador(request,proyectoId):
    return render(request, "opcionesCoordinador.html")

def crearInventario(request):
    return render(request, "crearInventario.html")
