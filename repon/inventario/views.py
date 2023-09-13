from django.shortcuts import render, redirect
from datetime import datetime
from .models import Proyecto, Insumo
from django.db.models import Sum


def inventario(request, proyectoId):
    inventarioInsumos = Insumo.objects.filter(proyectoAsociado = proyectoId)
    #inventarioInsumos = Insumo.objects.filter(proyectoAsociado = proyectoId).values('codigo','referencia','nombreMarca').annotate(totalCantidad=Sum('cantidad')).order_by('codigo')
    return render(request, "inventario.html",{'proyecto':proyectoId,'inventario':inventarioInsumos})

def landingCoordinador(request):
    idUsuario = request.user.id
    idEmpresa = Proyecto.objects.filter(coordinadorVinculado_id = idUsuario).values_list('empresaVinculada_id', flat= True)
    proyectos = Proyecto.objects.filter(empresaVinculada_id = idEmpresa[0])
    return render(request, "landingCoordinador.html", {'proyectos':proyectos})

def opcionesCoordinador(request,proyectoId):
    proyecto = Proyecto.objects.get(id=proyectoId)
    idCoordinador = proyecto.coordinadorVinculado.id
    nombreProyecto = proyecto.nombreProyecto
    idUsuario = request.user.id
    return render(request, "opcionesCoordinador.html", {'proyecto':proyectoId, 'usuarioSesion':idUsuario, 'usuarioCoordinador':idCoordinador, 'nombre':nombreProyecto})

def crearInventario(request, proyectoId):
    if request.method == 'POST':
        codigo = request.POST['codigo']
        ref = request.POST['ref']
        unidadBase = request.POST['unidadBase']
        cantidad = request.POST['cantidad']
        valorU = request.POST['valorU']
        iva = request.POST['iva']
        marca = request.POST['marca']
        tipoInsumo = request.POST['tipoInsumo']
        lugarAlmacenado = request.POST['lugarAlmacenado']
        fechaCaducidad = request.POST['fechaCaducidad']
        fechaCompra = request.POST['fechaCompra']
        observaciones = request.POST['observaciones']

        if fechaCaducidad == '':
            fechaCaducidad = None
        if fechaCompra == '':
            fechaCompra = datetime.now()

        proyectoAsociado = Proyecto.objects.get(id = proyectoId)

        crearInsumo = Insumo.objects.create(codigo = codigo, referencia = ref, unidad = unidadBase, cantidad = cantidad,
                                            valorUnitario = valorU, impuesto = iva, nombreMarca = marca,
                                            tipoInsumo = tipoInsumo, ubicacion = lugarAlmacenado, fechaCaducidad = fechaCaducidad,
                                            fechaCompra = fechaCompra, observaciones = observaciones, proyectoAsociado = proyectoAsociado)
        crearInsumo.save()
        return redirect(opcionesCoordinador, proyectoId)

    return render(request, "crearInventario.html", {'proyecto':proyectoId})
