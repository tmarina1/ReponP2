from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.landingAdmon, name='landingAdmon'),
    path('crearEmpresa/', views.crearEmpresas, name='crearEmpresas'),
    path('verEmpresa/', views.verEmpresa, name='verEmpresa'),
    path('crearProyecto/', views.crearProyecto, name='crearProyecto'),
    path('crearCoordinador/', views.crearCoordinador, name='crearCoordinador'),
    path('panelAdministrador/', views.panelAdministrador, name='panelAdministrador'),
    path('comparacionProyectos/', views.comparacionProyectos, name='comparacionProyectos'),
    path('verSolicitudesTraspaso/<int:estadoTransferencia>', views.verSolicitudesTraspaso, name='verSolicitudesTraspaso'),
    path('aceptarTraspaso/<int:transferenciaId>', views.aceptarTraspaso, name='aceptarTraspaso'),
    path('rechazarTraspaso/<int:transferenciaId>', views.rechazarTraspaso, name='rechazarTraspaso'),
    path('listaInsumosAdmin/', views.listaInsumosAdmin, name='listaInsumosAdmin'),
    path('verInventarioAdmin/<int:insumoId>', views.verInventarioAdmin, name='verInventarioAdmin'),
    path('subirArchivoEntreno/', views.subirArchivoEntreno, name='subirArchivoEntreno'),
    path('comparacionMedio/', views.comparacionMedio, name='comparacionMedio'),
<<<<<<< HEAD
    path('consultaInsumos/', views.consultaInsumos, name='consultaInsumos'),
=======
    path('traspasosAprobados/<int:proyectoId>', views.traspasosAprobados, name='traspasosAprobados'),
    path('listadoProyectos/', views.listadoProyectos, name='listadoProyectos'),
>>>>>>> 9475c3777798f8ed5bd86154dcfe9b521431f481
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
