from django.shortcuts import render, redirect
from autenticacion import models as autenticacion
from . import models

def empresas(request):
    return render(request, "empresas.html")

def crearEmpresas(request):
    if request.method == 'POST':

        nit = request.POST['nit']
        nombreEmpresa = request.POST['nombreEmpresa']
        direccion = request.POST['direccion']
        correo = request.POST['correo']
        telefono = request.POST['telefono']        

        registroEmpresa = models.Empresa.objects.create(nit = nit, nombreEmpresa = nombreEmpresa, direccion = direccion,
                                                        correo = correo, telefono = telefono)
        registroEmpresa.save()
        
        asignacionEmpresa = autenticacion.Perfil.objects.get()

        return redirect(empresas)
    
    return render(request, "crearEmpresas.html")
