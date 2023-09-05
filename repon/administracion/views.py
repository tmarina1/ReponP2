from django.shortcuts import render

# Create your views here.
def landingAdmon(request):
    return render(request, "landingAdmon.html")

def CrearEmpresas(request):
    return render(request, "crearEmpresas.html")

def crearProyecto(request):
    return render(request,'crearProyecto.html')

def crearCoordinador(request):
    return render(request,'crearCoordinador.html')