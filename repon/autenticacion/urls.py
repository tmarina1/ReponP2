from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.registro, name="registro"),
    path('inicioSesion/', views.inicioSesion, name="inicioSesion"),
    path('recuperarClave/', views.recuperarClave, name="recuperarClave"),
]