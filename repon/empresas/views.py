from django.shortcuts import render

def Empresas(request):
    return render(request, "empresas.html")

def CrearEmpresas(request):
    return render(request, "crearEmpresas.html")