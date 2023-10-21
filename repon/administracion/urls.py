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
    path('comparacionMedio/', views.comparacionMedio, name='comparacionMedio'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
