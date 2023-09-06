from django.shortcuts import render, redirect
from autenticacion import models as autenticacion
from django.contrib.auth.models import User
from . import models

def empresas(request):
    return render(request, "empresas.html")

def crearEmpresas(request):
    idUsuario = request.user.id
    empresa = models.Empresa.objects.filter(usuarioVinculado_id = idUsuario).exists()

    if empresa:
        return redirect(empresas)

    else:
        if request.method == 'POST':

            nit = request.POST['nit']
            nombreEmpresa = request.POST['nombreEmpresa']
            direccion = request.POST['direccion']
            correo = request.POST['correo']
            telefono = request.POST['telefono']

            idUsuarioAutenticado = autenticacion.Perfil.objects.filter(id = idUsuario).values_list('id', flat= True)
            
            registroEmpresa = models.Empresa.objects.create(nit = nit, nombreEmpresa = nombreEmpresa, direccion = direccion,
                                                            correo = correo, telefono = telefono, usuarioVinculado_id = idUsuarioAutenticado[0])
            registroEmpresa.save()
            return redirect(empresas)
        
        return render(request, "crearEmpresas.html")
