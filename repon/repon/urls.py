"""
URL configuration for repon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
<<<<<<< HEAD
from django.urls import path
from autenticacion import views as vistaAut

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vistaAut.registro, name='registro')
=======
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('autentificacion.urls')),
    path('inventario/', include('inventario.urls')),
    path('empresa/', include('empresas.urls')),
>>>>>>> fa4116448c01b6a679da05377743c416c3b2106c
]
