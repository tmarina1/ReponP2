import json
'''
Esta función tiene como finalidad leer un archivo tipo JSON y extraer de allí por medio de listas las ciudades y los departamentos de colombia para posteriormente aplicarlos
en los templates y asi poder dar una recomendación asertiva al usuario. 
'''
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