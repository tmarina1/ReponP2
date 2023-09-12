from django.shortcuts import render
from .models import Insumo, Proyecto

def inventario(request):
    return render(request, "inventario.html")

def landingCoordinador(request):
    return render(request, "landingCoordinador.html")

def opcionesCoordinador(request):
    return render(request, "opcionesCoordinador.html")

def crearInventario(request):
    if request.method == 'post':
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

        proyectoId = 1
        crearInsumo = Insumo.objects.create(codigo = codigo, referencia = ref, unidad = unidadBase, cantidad = cantidad,
                                            valorUnitario = valorU, impuesto = iva, nombreMarca = marca,
                                            tipoInsumo = tipoInsumo, ubicacion = lugarAlmacenado, fechaCaducidad = fechaCaducidad,
                                            fechaCompra = fechaCompra, observaciones = observaciones, proyectoAsociado = proyectoId )

    return render(request, "crearInventario.html")
