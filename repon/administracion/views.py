from django.shortcuts import render

# Create your views here.
def Empresas(request):
    return render(request, "empresas.html")

def CrearEmpresas(request):
    return render(request, "crearEmpresas.html")

def crearProyecto(request):
    return render(request,'crearProyecto.html')
