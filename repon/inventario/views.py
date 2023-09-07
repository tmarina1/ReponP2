from django.shortcuts import render

def inventario(request):
    return render(request, "inventario.html")

def landingCoordinador(request):
    return render(request, "landingCoordinador.html")