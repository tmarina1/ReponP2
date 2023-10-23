from django.shortcuts import render, redirect
from autenticacion.models import Perfil
from django.contrib.auth.models import User
from . import models
from inventario.models import Insumo
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage as mensajeEmail
from django.template.loader import render_to_string
from repon import settings as configuraciones
from django.db.models import Q
from datetime import datetime
import pandas as pd
from repon.settings import UBICACION
from django.db.models import Count,Avg,Sum,F, Value,  FloatField
from inventario.models import Insumo
from django.db.models.functions import Coalesce
from inventario.models import TransferenciaInsumo, Insumo
#------------------------------------------------------------------
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

'''
Este método permite mostrar la página principal de los usuarios administradores. Para acceder a esta página,
es necesario estar autenticado como administrador. El sistema obtiene el ID de usuario y verifica si aún no
se ha creado una empresa asociada a la cuenta. En caso de que no se haya creado una empresa, se redirige al
usuario a la página de creación de empresa. Si ya existe una empresa asociada, el usuario es redirigido directamente
a su página principal de administrador.
'''
@login_required
def landingAdmon(request):
    idUsuario = request.user.id
    empresa = models.Empresa.objects.filter(usuarioVinculado_id = idUsuario).exists()
    mensaje=''
    if not empresa:
        return redirect(crearEmpresas)
    estadoTransferencia = 0
    return render(request, "landingAdmon.html",{'estadoTransferencia':estadoTransferencia})


'''
Este método habilita a un usuario que ya ha iniciado sesión para acceder a la página de creación de proyectos.
Al crear un proyecto, el método verifica que no exista otro proyecto con el mismo nombre. Si no se encuentra
un proyecto con el mismo nombre, se permite la creación del proyecto de manera exitosa.
'''
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

    return render(request,'crearProyecto.html',{'ciudades':UBICACION[0], 'departamentos':UBICACION[1]})

'''
Este método tiene como objetivo mostrar la página de creación de coordinadores. En primer lugar,
verifica los proyectos existentes en la empresa para posteriormente vincular al coordinador con
uno de estos proyectos durante la creación. Además, se asegura de que el coordinador no haya sido
registrado previamente. Si el coordinador no se encuentra registrado previamente, procede a crearlo.
Posterior a eso envia al correo del coordinador las credenciales para que pueda ingresar a la plataforma.
'''
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
            perfil,creado = Perfil.objects.get_or_create(usuario=usuario)
            if creado:
                perfil.nombreCargo = "Coordinador"
                perfil.save()
            proyecto.coordinadorVinculado = perfil
            proyecto.save()
            mensajeExito = 'se ha creado correctamente el coordinador, por favor pidele que revise su correo, en la carpeta spam'

            plantilla = render_to_string('correoCoordinador.html',{
                'nombre':nombre,
                'correo':correo,    
                'clave':clave,
                'nombreProyecto':nombreProyecto
            })
            
            asunto = f"Credenciales de autenticacion para el uso de PAS para {nombre}"
            correoAEnviar = mensajeEmail(
                asunto,
                plantilla,
                configuraciones.EMAIL_HOST_USER,
                [correo]
            )

            correoAEnviar.fail_silently = False
            correoAEnviar.send()

            return render(request,'crearCoordinador.html',{"proyectos":proyectos,"mensajeExito":mensajeExito})

        except:
            mensajeError= 'Ya existe un coordinador registrado con este correo'
            return render(request,'crearCoordinador.html',{"proyectos":proyectos,"mensajeError":mensajeError})
        
    return render(request,'crearCoordinador.html',{"proyectos":proyectos})

'''
Este método tiene como finalidad mostrar la página de creación de empresas. Inicialmente,
verifica si el administrador registrado ya posee una empresa, en cuyo caso lo redirige a 
la página principal de administración. Si el administrador no tiene una empresa registrada,
se le permite crear una. Sin embargo, si la empresa ya existe, se impide la creación de una empresa
duplicada y se permite proceder únicamente si se trata de una empresa nueva."
'''
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
                mensaje = "Error al crear la empresa debido a que ya existe. Por favor verificar la información e intentarlo nuevamente."
            else:
                idUsuarioAutenticado = Perfil.objects.filter(id = idUsuario).values_list('id', flat= True)
                registroEmpresa = models.Empresa.objects.create(nit = nit, nombreEmpresa = nombreEmpresa, direccion = direccion,
                                                                departamento = departamento, ciudad = ciudad, usuarioVinculado_id = idUsuarioAutenticado[0])
                registroEmpresa.save()
                mensaje = 'Empresa creada satisfactoriamente.'
                return render(request, "landingAdmon.html",{'mensaje': mensaje})
        return render(request, "crearEmpresas.html",{'mensaje': mensaje, 'ciudades':UBICACION[0], 'departamentos':UBICACION[1]})

'''
Este método tiene como finalidad mostrar la información con la que se inscribió la empresa y la información básica de los proyectos
relacionados. Esto se logra realizando dos queries a la base de datos en donde se encuentra la empresa relacionada al usuario logueado
y los proyectos utilizando el id de esta misma empresa.
'''
@login_required
def verEmpresa(request):
    idUsuario = request.user.id
    empresa = models.Empresa.objects.get(usuarioVinculado = idUsuario)
    proyectos = models.Proyecto.objects.filter(empresaVinculada = empresa.id)
    return render(request, 'verEmpresa.html',{'empresa':empresa, 'proyectos':proyectos})

@login_required
def panelAdministrador(request):
    return render(request, 'panelAdministrador.html')

def comparacionProyectos(request):

    idUsuario = request.user.id
    empresa = models.Empresa.objects.get(usuarioVinculado_id = idUsuario)
    proyectosMiEmpresa = models.Proyecto.objects.filter(empresaVinculada_id = empresa.id)

    if request.method == 'POST':
        miProyecto = request.POST['miProyecto']
        otroProyecto = request.POST['otroProyecto']

        

        ## lado izq
        proyectoActual = models.Proyecto.objects.get(nombreProyecto = miProyecto)
        cantidadInsumos = Insumo.objects.filter(proyectoAsociado_id = proyectoActual.id).aggregate(cantidad=Sum('cantidad'))
        insumoMasDesaprovechado = Insumo.objects.filter(proyectoAsociado_id = proyectoActual.id).order_by('cantidad')[:3]
        costosInsumos = Insumo.objects.filter(proyectoAsociado_id = proyectoActual.id).aggregate(total = Sum(F('valorUnitario')*F('cantidad')))
        Aprobados = TransferenciaInsumo.objects.filter(proyectoDestino_id = proyectoActual.id,estado = "Aceptado").count()

        miActualProyecto = {'proyectoActual':proyectoActual,'cantidadInsumos':cantidadInsumos,'insumoMasDesaprovechado':insumoMasDesaprovechado,
                            'costosInsumos':costosInsumos,'Aprobados':Aprobados}
        ##lado der
        proyectoAComparar = models.Proyecto.objects.get(nombreProyecto = otroProyecto)
        cantidadInsumosOtro = Insumo.objects.filter(proyectoAsociado_id = proyectoAComparar.id).aggregate(cantidad=Sum('cantidad'))
        insumoMasDesaprovechadoOtro = Insumo.objects.filter(proyectoAsociado_id = proyectoAComparar.id).order_by('cantidad')[:3]
        costosInsumosOtro = Insumo.objects.filter(proyectoAsociado_id = proyectoAComparar.id).aggregate(total = Sum(F('valorUnitario')*F('cantidad')))
        AprobadosOtro = TransferenciaInsumo.objects.filter(proyectoDestino_id = proyectoAComparar.id,estado = "Aceptado").count()

        miOtroProyecto = {'proyectoAComparar':proyectoAComparar,'cantidadInsumosOtro':cantidadInsumosOtro,'insumoMasDesaprovechadoOtro':insumoMasDesaprovechadoOtro,
                            'costosInsumosOtro':costosInsumosOtro,'AprobadosOtro':AprobadosOtro}
        
        return render(request, 'comparacionProyectos.html',{'proyectosMiEmpresa':proyectosMiEmpresa,'miActualProyecto':miActualProyecto,'miOtroProyecto':miOtroProyecto})

        
    return render(request, 'comparacionProyectos.html',{'proyectosMiEmpresa':proyectosMiEmpresa})

'''
Metodo que lista las solicitudes de traspaso de insumos entre proyectos para el administrador de la empresa, y se verifica si
al aprobar una solicitud se verificara si la nueva cantidad del insumo está disponible con las otras solicitudes, sino se rechazará la
peticion automaticamente y se enviara un correo al coordinador con su respectiva respuesta
'''
@login_required
def verSolicitudesTraspaso(request, estadoTransferencia):
    idUsuario = request.user.id
    mensaje = ''
    solicitudes = TransferenciaInsumo.objects.filter(administrador_id = idUsuario)
    if estadoTransferencia == 1:
        mensaje = 'Lo sentimos, se ha rechazado por falta de insumos en el inventario'
    elif estadoTransferencia == 2:
        mensaje = 'Se ha aceptado exitosamente'
    elif estadoTransferencia == 3:
        mensaje = 'Se ha rechazado exitosamente'

    return render(request,'verSolicitudesTraspaso.html',{'solicitudes':solicitudes,'mensaje':mensaje})

'''
Metodo encargado de realizar el proceso de transferencia de insumos de un proyecto a otro cuando este es aceptado por el
administrador de la empresa. Enviando un correo al coordinador con su respectiva respuesta.
estadoTransferencia = 1: se ha rechazado por falta de insumos en el inventario
estadoTransferencia = 2: se ha aceptado por parte del administrador
'''
@login_required
def aceptarTraspaso(request, transferenciaId):
    if request.method == 'POST':
        solicitud = TransferenciaInsumo.objects.get(id = transferenciaId)
        insumo =  Insumo.objects.get(id = solicitud.insumo_id)
        coordinador = User.objects.get(id = solicitud.coordinadorSolicitante_id)
        proyecto = models.Proyecto.objects.get(coordinadorVinculado_id = solicitud.coordinadorSolicitante_id)
        

        if solicitud.cantidad > insumo.cantidad or solicitud.proyectoDestino_id == insumo.proyectoAsociado_id:
            plantilla = render_to_string('traspasos/correoFaltaInventario.html',{
            'nombre': coordinador.first_name,
            'insumo': insumo.referencia,
            'cantidad': solicitud.cantidad
            })
            asunto = f"Respuesta a la solicitud del insumo \"{insumo.referencia}\" para el proyecto \"{proyecto.nombreProyecto}\""
            correoAEnviar = mensajeEmail(
                asunto,
                plantilla,
                configuraciones.EMAIL_HOST_USER,
                [coordinador.email]
            )
            correoAEnviar.fail_silently = False
            correoAEnviar.send()
            estadoTransferencia = 1
            solicitud.estado = "Rechazado"
            solicitud.save() 

        elif solicitud.cantidad == insumo.cantidad:
            insumo.proyectoAsociado_id = solicitud.proyectoDestino_id
            insumo.save()
            plantilla = render_to_string('traspasos/correoAprobacion.html',{
            'nombre': coordinador.first_name,
            'insumo': insumo.referencia,
            'cantidad': solicitud.cantidad
            })
            asunto = f"Respuesta a la solicitud del insumo \"{insumo.referencia}\" para el proyecto \"{proyecto.nombreProyecto}\""
            correoAEnviar = mensajeEmail(
                asunto,
                plantilla,
                configuraciones.EMAIL_HOST_USER,
                [coordinador.email]
            )
            correoAEnviar.fail_silently = False
            correoAEnviar.send()
            estadoTransferencia = 2
            solicitud.estado = "Aceptado"
            solicitud.save() 
        elif solicitud.cantidad < insumo.cantidad:
            insumo.cantidad -= solicitud.cantidad
            insumo.save()
            comprobarExistencia = Insumo.objects.filter(codigo = insumo.codigo, proyectoAsociado_id = solicitud.proyectoDestino_id)
            if comprobarExistencia:
                comprobarExistencia[0].cantidad += solicitud.cantidad
                comprobarExistencia[0].save() 
            else:
                nuevoInsumo = Insumo.objects.create(codigo = insumo.codigo, referencia = insumo.referencia, unidad = insumo.unidad,
                                                    cantidad = solicitud.cantidad, valorUnitario = insumo.valorUnitario, impuesto = insumo.impuesto,
                                                    nombreMarca = insumo.nombreMarca,tipoInsumo = insumo.tipoInsumo,
                                                    ubicacion = insumo.ubicacion,fechaCaducidad = insumo.fechaCaducidad,
                                                    fechaCompra = insumo.fechaCompra, observaciones = insumo.observaciones, proyectoAsociado_id = solicitud.proyectoDestino_id)
                nuevoInsumo.save()
            plantilla = render_to_string('traspasos/correoAprobacion.html',{
            'nombre': coordinador.first_name,
            'insumo': insumo.referencia,
            'cantidad': solicitud.cantidad
            })
            asunto = f"Respuesta a la solicitud del insumo \"{insumo.referencia}\" para el proyecto \"{proyecto.nombreProyecto}\""
            correoAEnviar = mensajeEmail(
                asunto,
                plantilla,
                configuraciones.EMAIL_HOST_USER,
                [coordinador.email]
            )
            correoAEnviar.fail_silently = False
            correoAEnviar.send()
            estadoTransferencia = 2
            solicitud.estado = "Aceptado"
            solicitud.save() 
        return redirect(verSolicitudesTraspaso, estadoTransferencia)
    return render(request, 'traspasos/aceptado.html')

'''
Metodo encargado de estabelcer el estado rechazado en el proceso de transferencia de insumos de un proyecto a otro cuando este 
es denegado por el administrador de la empresa. Enviando un correo al coordinador con su respectiva respuesta.
estadoTransferencia = 3: se ha Rechazado por parte del administrador
'''
@login_required
def rechazarTraspaso(request, transferenciaId):
    if request.method == 'POST':
        solicitud = TransferenciaInsumo.objects.get(id = transferenciaId)
        solicitud.estado = "Rechazado"
        solicitud.save()
        insumo =  Insumo.objects.get(id = solicitud.insumo_id)
        coordinador = User.objects.get(id = solicitud.coordinadorSolicitante_id)
        proyecto = models.Proyecto.objects.get(coordinadorVinculado_id = solicitud.coordinadorSolicitante_id)

        plantilla = render_to_string('traspasos/correoRechazo.html',{
            'nombre': coordinador.first_name,
            'insumo': insumo.referencia,
            'cantidad': solicitud.cantidad
        })
        asunto = f"Respuesta a la solicitud del insumo \"{insumo.referencia}\" para el proyecto \"{proyecto.nombreProyecto}\""
        correoAEnviar = mensajeEmail(
            asunto,
            plantilla,
            configuraciones.EMAIL_HOST_USER,
            [coordinador.email]
        )
        correoAEnviar.fail_silently = False
        correoAEnviar.send()
        estadoTransferencia = 3
        return redirect(verSolicitudesTraspaso, estadoTransferencia)
    return render(request, 'traspasos/rechazado.html')


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def ingresoCategoria(request):
    idUsuario = request.user.id
    insumosExistentes = Insumo.objects.filter(proyectoAsociado__empresaVinculada__usuarioVinculado__id = idUsuario).order_by('referencia')

    paginacion = Paginator(insumosExistentes, 10)  # Muestra 10 insumos por página
    pagina = request.GET.get('pagina')

    if request.method == 'POST':
        filtros = {
            f'{llave}__icontains': valor
            for llave, valor in request.POST.items()
            if llave in ['referencia', 'categoria','proyectoAsociado__nombreProyecto']
            }
        insumosExistentes =  insumosExistentes.filter(**filtros)
        paginacion = Paginator(insumosExistentes, 10)

    try:
        insumos = paginacion.page(pagina)
    except PageNotAnInteger:
        # Si el parámetro de la página no es un número, muestra la primera página
        insumos = paginacion.page(1)
    except EmptyPage:
        # Si la página está fuera de rango, muestra la última página de resultados
        insumos = paginacion.page(paginacion.num_pages)
    return render(request, 'ingresoCategoria.html',{'insumos': insumos})

def verInventarioAdmin(request, insumoId):
    item = Insumo.objects.get(id=insumoId)
    valorSubTotal = item.cantidad*item.valorUnitario
    if item.impuesto == 'si':
        valorTotal = valorSubTotal+(valorSubTotal*0.19)
    else:
        valorTotal = valorSubTotal
    
    if request.method == 'POST':
        codigoInsumo = request.POST.get('codigo')
        unidadBase = request.POST.get('unidadBase')
        cantidad = request.POST.get('cantidad')
        marca = request.POST.get('marca')
        tipoInsumo = request.POST.get('tipoInsumo')
        lugarAlmacenado = request.POST.get('lugarAlmacenado')
        valorUnidad = request.POST.get('valorU')
        iva = request.POST.get('iva')
        fechaCaducidad = request.POST.get('fechaCaducidad')
        fechaCompra = request.POST.get('fechaCompra')
        categoria = request.POST.get('categoria')
        observaciones = request.POST.get('observaciones')

        insumoBuscado = Insumo.objects.get(id=insumoId)

        insumoBuscado.unidad = unidadBase
        insumoBuscado.cantidad = cantidad
        insumoBuscado.nombreMarca = marca
        insumoBuscado.tipoInsumo = tipoInsumo
        insumoBuscado.ubicacion = lugarAlmacenado
        insumoBuscado.valorUnitario = valorUnidad
        insumoBuscado.impuesto = iva
        if fechaCaducidad and fechaCaducidad != 'NA':
            fechaCaducidadParseada = datetime.strptime(fechaCaducidad, '%Y-%m-%dT%H:%M')
            insumoBuscado.fechaCaducidad = fechaCaducidadParseada
        if fechaCompra:
            fechaCompraParseada = datetime.strptime(fechaCompra, '%Y-%m-%dT%H:%M')
            insumoBuscado.fechaCompra = fechaCompraParseada
        insumoBuscado.categoria = categoria
        insumoBuscado.observaciones = observaciones

        insumoBuscado.save()
        return redirect(verInventarioAdmin, insumoId)


    return render(request, "verInventarioAdmin.html", {'item': item, 'valorTotal': valorTotal})

def subirArchivoEntreno(request):
    mensajes =''
    try:
        if request.method == 'POST' and request.FILES['archivo']:
            archivo = request.FILES['archivo']
            df = pd.read_excel(archivo)
            X = df['Referencia']
            y = df['categoria']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            vectorTFIDF = TfidfVectorizer()
            X_train_tfidf = vectorTFIDF.fit_transform(X_train)

            modelo_path = os.path.join('administracion', 'static', 'archivosModelo', 'modeloDeClasificacion.pkl')
            vectorizador_path = os.path.join('administracion', 'static', 'archivosModelo', 'vectorizadorTFIDF.pkl')

            clf = MultinomialNB()
            clf.fit(X_train_tfidf, y_train)

            joblib.dump(clf, modelo_path)
            joblib.dump(vectorTFIDF, vectorizador_path)
            return redirect(landingAdmon)
    except:
        mensajes = ['Error con el archivo subido, por favor verifica que el formato esté correctamente diligenciado']
    return render(request, 'subirArchivoEntreno.html', {'mensajes':mensajes})

@login_required
def comparacionMedio(request):
    idUsuario = request.user.id
    empresa = models.Empresa.objects.get(usuarioVinculado_id = idUsuario)


    proyectosMiEmpresa = models.Proyecto.objects.filter(empresaVinculada_id = empresa.id).count()
    cantidadInsumos = Insumo.objects.filter(proyectoAsociado__empresaVinculada__id=empresa.id).aggregate(cantidad=Sum('cantidad'))
    costosInsumos = Insumo.objects.filter(proyectoAsociado__empresaVinculada__id=empresa.id).aggregate(total = Sum(F('valorUnitario')*F('cantidad')))
    insumosMayorCantidad = Insumo.objects.filter(proyectoAsociado__empresaVinculada__id=empresa.id).order_by('-cantidad')[:3]


    miEmpresa = {'proyectosMiEmpresa':proyectosMiEmpresa,'cantidadInsumos':cantidadInsumos['cantidad'],
                 'costosInsumos':costosInsumos['total'],'Desperdiciados':insumosMayorCantidad}


    promedioProyectosRestantes = models.Proyecto.objects.values('empresaVinculada__id').annotate(
        cantidadProyectos=Count('id')
    ).exclude(empresaVinculada__id = empresa.id).aggregate(
        promedioProyectos=Avg('cantidadProyectos')
    )

    sumaCantidadInsumos = Insumo.objects.exclude(proyectoAsociado__empresaVinculada__id=empresa.id).aggregate(
        totalCantidad=Sum('cantidad'))['totalCantidad']
    empresasConInsumos = models.Empresa.objects.exclude(id=empresa.id).annotate(cantidadInsumos=Count('proyecto__insumo')).filter(
        cantidadInsumos__gt=0)
    cantidadEmpresas = empresasConInsumos.count()

    promedioInsumos = sumaCantidadInsumos / cantidadEmpresas

    costoTotalInsumos = Insumo.objects.exclude(proyectoAsociado__empresaVinculada__id=empresa.id).aggregate(
        costoTotal=Sum(F('valorUnitario')*F('cantidad')))['costoTotal']

    promedioPrecios = costoTotalInsumos  / cantidadEmpresas

    insumosMayorCantidad = Insumo.objects.exclude(proyectoAsociado__empresaVinculada__id=empresa.id).order_by('-cantidad')[:3]


    medio = {'promedioProyectosRestantes':promedioProyectosRestantes['promedioProyectos'],'promedioInsumos':promedioInsumos,
             'promedioPrecios':promedioPrecios,'insumosMayorCantidad':insumosMayorCantidad}

    print(promedioPrecios )
    return render(request, 'comparacionMedio.html',{'miEmpresa':miEmpresa,'empresa': empresa,'medio':medio})