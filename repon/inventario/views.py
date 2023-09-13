from django.shortcuts import render, redirect
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
    return render(request, "opcionesCoordinador.html", {'proyecto':proyectoId})

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
        print(f'request: {request.POST}')
        proyectoAsociado = Proyecto.objects.get(id = proyectoId)

        crearInsumo = Insumo.objects.create(codigo = codigo, referencia = ref, unidad = unidadBase, cantidad = cantidad,
                                            valorUnitario = valorU, impuesto = iva, nombreMarca = marca,
                                            tipoInsumo = tipoInsumo, ubicacion = lugarAlmacenado,
                                            observaciones = observaciones, proyectoAsociado = proyectoAsociado )
        crearInsumo.save()
        return redirect(opcionesCoordinador, proyectoId)

    return render(request, "crearInventario.html", {'proyecto':proyectoId})
