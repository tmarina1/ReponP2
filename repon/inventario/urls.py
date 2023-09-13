from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.landingCoordinador, name='landingCoordinador'),
    path('opcionesCoordinador/<int:proyectoId>', views.opcionesCoordinador, name='opcionesCoordinador'),
    path('verInventario/<int:proyectoId>', views.inventario, name='inventario'),
    path('crearInventario/<int:proyectoId>', views.crearInventario, name='crearInventario'),
    path('subirArchivo/<int:proyectoId>', views.subirArchivo, name='subirArchivo')
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
