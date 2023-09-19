import json

def extraerCiudadyDepartamento(ruta):
    departamentos = []
    ciudades = []
    with open(ruta) as archivo:
        datos = json.load(archivo)
        for dato in datos:
            departamentos.append(dato['departamento'])
            for ciudad in dato['ciudades']:
                ciudades.append(ciudad)
    return ciudades,departamentos