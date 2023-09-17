from django.shortcuts import render, redirect
from autenticacion import models as autenticacion
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.decorators import login_required

@login_required
def landingAdmon(request):
    idUsuario = request.user.id
    empresa = models.Empresa.objects.filter(usuarioVinculado_id = idUsuario).exists()
    mensaje=''
    if not empresa:
        return redirect(crearEmpresas)
    return render(request, "landingAdmon.html")

@login_required
def crearProyecto(request):
    if request.method == 'POST':
        nombreProyecto = request.POST['nombreProyecto']
        estadoProyecto = request.POST['estadoProyecto']
        direccion = request.POST['direccion']
        departamento = request.POST['departamento']
        ciudad = request.POST['ciudad']
        idUsuario = request.user.id
        idEmpresaAutenticada = models.Empresa.objects.filter(usuarioVinculado_id = idUsuario).values_list('id', flat= True)
        try:
            proyecto = models.Proyecto.objects.get(nombreProyecto = nombreProyecto, empresaVinculada_id = idEmpresaAutenticada[0])

            if proyecto:
                mensajeError = "Ya existe un proyecto con ese nombre"
                return render(request,'crearProyecto.html',{"mensajeError":mensajeError} )
            
        except:
            registroProyecto = models.Proyecto.objects.create(nombreProyecto = nombreProyecto, estadoProyecto = estadoProyecto, 
                                                                direccion = direccion, departamento = departamento, ciudad = ciudad, 
                                                                empresaVinculada_id = idEmpresaAutenticada[0])
            registroProyecto.save()
            mensajeExito = "Proyecto creado exitosamente."
            return render(request,'crearProyecto.html',{"mensajeExito":mensajeExito} )

    return render(request,'crearProyecto.html')

@login_required
def crearCoordinador(request):
    idUsuario = request.user.id
    idEmpresaAutenticada = models.Empresa.objects.filter(usuarioVinculado_id = idUsuario).values_list('id', flat= True)
    proyectos =  proyecto = models.Proyecto.objects.filter(empresaVinculada_id = idEmpresaAutenticada[0])

    if request.method == 'POST':
        
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        clave = request.POST['clave']
        nombreProyecto = request.POST['nombreProyecto']

        proyecto = models.Proyecto.objects.get(nombreProyecto = nombreProyecto, empresaVinculada_id = idEmpresaAutenticada[0])
        try:
            usuario = User.objects.create_user(first_name=nombre,username=correo, email=correo, password=clave)
            usuario.save()
            perfil,creado = autenticacion.Perfil.objects.get_or_create(usuario=usuario)
            if creado:
                perfil.nombreCargo = "Coordinador"
                perfil.save()
            proyecto.coordinadorVinculado = perfil
            proyecto.save()
            mensajeExito = 'se ha creado correctamente el coordinador'
            return render(request,'crearCoordinador.html',{"proyectos":proyectos,"mensajeExito":mensajeExito})
        
        except:
            mensajeError= 'Ya existe un coordinador registrado con este correo'
            return render(request,'crearCoordinador.html',{"proyectos":proyectos,"mensajeError":mensajeError})
        
    return render(request,'crearCoordinador.html',{"proyectos":proyectos})
        
@login_required
def crearEmpresas(request):
    idUsuario = request.user.id
    empresa = models.Empresa.objects.filter(usuarioVinculado_id = idUsuario).exists()
    mensaje=''
    if empresa:
        return redirect(landingAdmon)

    else:
        if request.method == 'POST':

            nit = request.POST['nit']
            nombreEmpresa = request.POST['nombre']
            direccion = request.POST['direccion']
            departamento = request.POST['departamento']
            ciudad = request.POST['ciudad']

            nitEmpresaExistente = models.Empresa.objects.filter(nit=nit).exists()
            nombreEmpresaExistente = models.Empresa.objects.filter(nombreEmpresa=nombreEmpresa).exists()

            if nitEmpresaExistente or nombreEmpresaExistente:
                mensaje = "Error al crear la empresa, debido a que ya existe. Por favor, verifica la información e inténtalo nuevamente."
            else:
                idUsuarioAutenticado = autenticacion.Perfil.objects.filter(id = idUsuario).values_list('id', flat= True)
                registroEmpresa = models.Empresa.objects.create(nit = nit, nombreEmpresa = nombreEmpresa, direccion = direccion,
                                                                departamento = departamento, ciudad = ciudad, usuarioVinculado_id = idUsuarioAutenticado[0])
                registroEmpresa.save()
                return redirect(landingAdmon)
        
        return render(request, "crearEmpresas.html",{'mensaje': mensaje})
