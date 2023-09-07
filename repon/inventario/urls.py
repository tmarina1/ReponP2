from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.landingCoordinador, name='landingCoordinador'),
    path('opcionesCoordinador/', views.opcionesCoordinador, name='opcionesCoordinador'),
    path('verInventario/', views.inventario, name='inventario'),
    path('crearInventario/', views.crearInventario),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
