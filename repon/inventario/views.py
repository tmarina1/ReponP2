from django.shortcuts import render

def inventario(request):
    return render(request, "inventario.html")

def landingCoordinador(request):
    return render(request, "landingCoordinador.html")

def opcionesCoordinador(request):
    return render(request, "opcionesCoordinador.html")

def subirArchivo(request):
    return render(request, "subirArchivo.html")