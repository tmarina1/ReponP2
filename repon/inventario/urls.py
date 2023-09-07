from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.landingCoordinador, name='landingCoordinador'),
    path('opcionesCoordinador/', views.opcionesCoordinador, name='opcionesCoordinador'),
    path('verInventario/', views.inventario, name='inventario'),
]