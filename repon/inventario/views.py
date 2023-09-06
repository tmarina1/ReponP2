from django.shortcuts import render

def Inventario(request):
    return render(request, "inventario.html")

def crearInventario(request):
    return render(request, "crearInventario.html")
