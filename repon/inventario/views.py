from django.shortcuts import render, redirect
from datetime import datetime
from .models import Proyecto, Insumo, TransferenciaInsumo, CostosProyecto
import pandas as pd
import difflib
from django.contrib.auth.decorators import login_required
from decimal import Decimal
import joblib
import os

'''
Este método tiene la función de listar los insumos en el inventario de un proyecto previamente seleccionado.
Además, permite realizar búsquedas y listar insumos que coincidan con los criterios especificados. Si se 
encuentra un insumo que es similar o se asemeja a uno existente, se facilita su visualización. Sin embargo, 
si no se encuentran insumos que coincidan o sean similares a lo buscado, se muestra un mensaje de error para 
informar al usuario que no se han encontrado resultados.
'''
@login_required
def inventario(request, proyectoId):
    inventarioInsumos = Insumo.objects.filter(proyectoAsociado = proyectoId, paraVender = False)
    mensajes = ''
    terminoBusqueda = request.GET.get('busqueda')
    if terminoBusqueda:
        if Insumo.objects.filter(proyectoAsociado = proyectoId, codigo__icontains = terminoBusqueda).exists():
            inventarioInsumos = Insumo.objects.filter(proyectoAsociado = proyectoId, codigo__icontains = terminoBusqueda)
        elif Insumo.objects.filter(proyectoAsociado = proyectoId, nombreMarca__icontains = terminoBusqueda).exists():
            inventarioInsumos = Insumo.objects.filter(proyectoAsociado = proyectoId, nombreMarca__icontains = terminoBusqueda)
        elif Insumo.objects.filter(proyectoAsociado = proyectoId, referencia__icontains = terminoBusqueda).exists():
            inventarioInsumos = Insumo.objects.filter(proyectoAsociado = proyectoId, referencia__icontains = terminoBusqueda)    
        else:
            insumos = Insumo.objects.filter(proyectoAsociado=proyectoId)
            nombres = [insumo.referencia for insumo in insumos]
            correccionReferencias = difflib.get_close_matches(terminoBusqueda, nombres, n=1, cutoff=0.6)
            if correccionReferencias:
                if Insumo.objects.filter(proyectoAsociado = proyectoId, codigo__icontains = correccionReferencias[0]).exists():
                    inventarioInsumos = Insumo.objects.filter(proyectoAsociado = proyectoId, codigo__icontains = correccionReferencias[0])
                if Insumo.objects.filter(proyectoAsociado = proyectoId, nombreMarca__icontains = correccionReferencias[0]).exists():
                    inventarioInsumos = Insumo.objects.filter(proyectoAsociado = proyectoId, nombreMarca__icontains =correccionReferencias[0])
                if Insumo.objects.filter(proyectoAsociado = proyectoId, referencia__icontains = correccionReferencias[0]).exists():
                    inventarioInsumos = Insumo.objects.filter(proyectoAsociado = proyectoId, referencia__icontains =  correccionReferencias[0])
            else:
                mensajes =['Error, lo que buscaste no existe o está mal escrito, intente nuevamente.']
            
    print (mensajes)
    return render(request, "inventario.html",{'proyecto':proyectoId,'inventario':inventarioInsumos,'terminoBusqueda':terminoBusqueda, 'mensajes':mensajes})
'''
Metodo que se encarga de listar los isumos del inventario
'''
@login_required
def verItemInventario(request, insumoId):
    mensaje = ''
    item = Insumo.objects.get(id=insumoId)
    valorSubTotal = item.cantidad*item.valorUnitario

    coordinadorSolicitante = request.user.id
    coordinadorDueño = item.proyectoAsociado_id
    
    coordinadorInsumo = Proyecto.objects.get(id = coordinadorDueño)


    if item.impuesto == 'si':
        valorTotal = valorSubTotal+(valorSubTotal*0.19)
    else:
        valorTotal = valorSubTotal
    

    if request.method == 'POST':
        cantidad = request.POST['cantidadTraspaso']
        
        administrador = item.proyectoAsociado.empresaVinculada.usuarioVinculado.id
        proyectoOrigen = item.proyectoAsociado.id    
        destino = Proyecto.objects.get(coordinadorVinculado_id = coordinadorSolicitante)
        proyectoDestino = destino.id
        insumo = item.id
        peticion = TransferenciaInsumo.objects.create(coordinadorSolicitante_id = coordinadorSolicitante, administrador_id = administrador,
                                                      proyectoOrigen_id = proyectoOrigen, proyectoDestino_id = proyectoDestino, insumo_id=insumo,
                                                      cantidad = cantidad)
        
        peticion.save()
        mensaje = 'se ha enviado la solicitud correctamente'

    return render(request, "verInventario.html", {'item': item, 'valorTotal': valorTotal, 'mensaje':mensaje,'coordinadorInsumo':coordinadorInsumo,'coordinadorSolicitante':coordinadorSolicitante})

'''
Este método tiene como propósito mostrar la página principal destinada al usuario con el rol de coordinador. 
La página principal para el coordinador proporciona acceso a las funciones relacionadas con la gestión de proyectos 
asociadas con su rol.
'''
@login_required
def landingCoordinador(request):
    idUsuario = request.user.id
    idEmpresa = Proyecto.objects.filter(coordinadorVinculado_id = idUsuario).values_list('empresaVinculada_id', flat= True)
    proyectos = Proyecto.objects.filter(empresaVinculada_id = idEmpresa[0])
    proyectosConCoordinador = []
    for proyecto in proyectos:
        if proyecto.coordinadorVinculado:
            proyectosConCoordinador.append(proyecto)
    return render(request, "landingCoordinador.html", {'proyectos':proyectosConCoordinador})

'''
Este método tiene como objetivo mostrar la página de opciones del coordinador. En esta página, 
el coordinador tiene la capacidad de realizar varias acciones, incluyendo la posibilidad de guardar 
uno o varios insumos y listar el inventario.
'''
@login_required
def opcionesCoordinador(request,proyectoId):
    proyecto = Proyecto.objects.get(id=proyectoId)
    idCoordinador = proyecto.coordinadorVinculado.id
    nombreProyecto = proyecto.nombreProyecto
    idUsuario = request.user.id
    return render(request, "opcionesCoordinador.html", {'proyecto':proyectoId, 'usuarioSesion':idUsuario, 'usuarioCoordinador':idCoordinador, 'nombre':nombreProyecto})

#----------------------------------------------------------------------

'''
Este método tiene la función de predecir la categoría de un insumo.
'''

def predecirCategoria(referencia):
    rutaModelo = os.path.join('administracion', 'static', 'archivosModelo', 'modeloDeClasificacion.pkl')
    rutaVectorizador = os.path.join('administracion', 'static', 'archivosModelo', 'vectorizadorTFIDF.pkl')

    clf = joblib.load(rutaModelo)
    vectorTFIDF = joblib.load(rutaVectorizador)

    descripcion_tfidf = vectorTFIDF.transform([referencia])
    categoria = clf.predict(descripcion_tfidf)
    return categoria[0]
#----------------------------------------------------------------------

'''
Este método tiene la función de mostrar la página destinada a ingresar un nuevo insumo al inventario de sobrantes existente y por defecto asignarle una categoría a dicho insumo.
'''
@login_required
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
                                            fechaCompra = fechaCompra, observaciones = observaciones, categoria = predecirCategoria(ref) , proyectoAsociado = proyectoAsociado)
    
        crearInsumo.save()
        return redirect(opcionesCoordinador, proyectoId)

    return render(request, "crearInventario.html", {'proyecto':proyectoId})

'''
Este método tiene como finalidad presentar la página destinada a la incorporación de múltiples 
insumos al inventario de sobrantes preexistente. Facilita este proceso mediante la carga de un archivo 
de Excel proporcionado al usuario como plantilla. Posteriormente, verifica que el archivo haya sido completado 
de manera adecuada antes de almacenar los insumos en el inventario.
'''
@login_required
def subirArchivo(request, proyectoId):
    mensajes =''
    try:
        if request.method == 'POST' and request.FILES['archivo']:
            archivo = request.FILES['archivo']
            proyectoAsociado = Proyecto.objects.get(id = proyectoId)
            df = pd.read_excel(archivo)
            for index, row in df.iterrows():
                Insumo.objects.create(codigo = row['Codigo_insumo'], referencia = row['Referencia'], unidad = row['Unidad_base'],
                                        cantidad = row['Cantidad'], valorUnitario = row['Valor_unitario'], impuesto = row['Iva'],
                                        nombreMarca = row['Marca'], tipoInsumo = row['Tipo_insumo'], ubicacion = row['Lugar_Almacenamiento'],
                                        fechaCaducidad = row['Fecha_caducidad'], fechaCompra = row['Fecha_compra'], 
                                        observaciones = row['Observaciones'], categoria = predecirCategoria(row['Referencia']) , proyectoAsociado = proyectoAsociado
                )
            return redirect(opcionesCoordinador, proyectoId)
    except:
        mensajes = ['Error con el archivo subido, por favor verifica que el formato esté correctamente diligenciado']
    return render(request, 'subirArchivo.html', {'proyecto':proyectoId, 'mensajes':mensajes})

@login_required
def ingresarCostos(request, proyectoId):
    if request.method == 'POST':
        valor = request.POST['valor']
        tipo = request.POST['tipo']
        observaciones = request.POST['observaciones']   

        proyectoAsociado = Proyecto.objects.get(id = proyectoId)

        costoNuevo = CostosProyecto.objects.create(valor=valor,tipo=tipo,observaciones=observaciones,
                                                   proyectoAsociado=proyectoAsociado) 
        costoNuevo.save()
    return render(request, 'ingresarCostos.html', {'proyecto':proyectoId})

    

    
