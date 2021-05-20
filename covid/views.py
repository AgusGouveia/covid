#Aqui estarán todas las rutas que tengan relacion con la aplicacion Covid
from flask import render_template, request 
from covid import app
import csv 
import json
from datetime import date

@app.route("/provincias") #definimos la ruta
def provincias():
    fichero = open("data/provincias.csv", "r", encoding="utf8") #abrimos el fichero en formato leer
    csvreader = csv.reader(fichero, delimiter=",")

    lista = []
    for registro in csvreader:
        d = {'codigo': registro[0], 'valor': registro[1]}
        lista.append(d)

    fichero.close()
    print(lista)
    return json.dumps(lista)

@app.route("/provincia/<codigoProvincia>") #<> es para meter un parametro
def laprovincia(codigoProvincia):
    fichero = open("data/provincias.csv", "r",)

    dictreader = csv.DictReader(fichero, fieldnames=['codigo', 'provincia']) #Otra manera de hacer lo de arriba.. leer el fichero y que nos cree un dict al mismo tiempo
    for registro in dictreader:
        if registro['codigo'] == codigoProvincia:
            fichero.close()
            return registro['provincia']
    
    fichero.close()
    return "El valor no existe"

@app.route("/casos/<int:year>", defaults={'mes': None})
@app.route("/casos/<int:year>/<int:mes>")
@app.route('/casos/<int:year>/<int:mes>/<int:dia>') #Con el int obligamos a que los parametros sea un entero, sino, da un error.
def casos(year, mes, dia=None): #El none tambien podríamos hacerlo arriba, es lo mismo.

    if not mes:
        fecha = "{:04d}".format(year)
    elif not dia: 
        fecha = "{:04d}-{:02d}".format(year, mes)
    else: 
        fecha = "{:04d}-{:02d}-{:02d}".format(year, mes, dia) #el formato rellenara los espacios que me hagan falta con 0 a la izq.

    fichero = open("data/casos_diagnostico_provincia.csv", "r")
    dictReader = csv.DictReader(fichero)

    res = {
        'num_casos': 0,
        'num_casos_prueba_pcr': 0,
        'num_casos_prueba_test_ac': 0,
        'num_casos_prueba_ag': 0,
        'num_casos_prueba_elisa': 0,
        'num_casos_prueba_desconocida': 0
    }
    
    for registro in dictReader: #Recorremos el diccionario
        if fecha in registro['fecha']:
            for clave in res:
                res[clave] += int(registro[clave]) #Acumulamos nuestros casos utilizando el dicc
        elif registro ['fecha'] > fecha:
            break
    
    fichero.close()
    return json.dumps(res) #me asegura que cualquier estructura de dato que meta me la aceptará porque la convierte en un json
 
    
@app.route("/incidenciasdiarias", methods = ['GET', 'POST'])
def incidencia():
    formulario = {
        'provincia': '',
        'fecha': str(date.today()),
        'num_casos_prueba_pcr': 0,
        'num_casos_prueba_test_ac': 0, 
        'num_casos_prueba_ag': 0,
        'num_casos_prueba_elisa': 0,
        'num_casos_prueba_desconocida': 0
    }

    fichero = open('data/provincias.csv', 'r')
    csvreader = csv.reader(fichero, delimiter=",")
    next(csvreader)
    lista = []

    for registro in csvreader:
        d = {'codigo': registro[0], 'descripcion': registro[1]}
        lista.append(d)

    fichero.close()

    if request.method == 'GET':
        return render_template("alta.html", datos=formulario, 
                               provincias=lista, error="")
    for clave in formulario:
        formulario[clave] = request.form[clave]
    #validar que num_casos en general es no negativo
    num_pcr = request.form['num_casos_prueba_pcr']
    try:
        num_pcr = int(num_pcr)
        if num_pcr < 0:
            raise ValueError('Debe ser no negativo')
    except ValueError:
        return render_template("alta.html", datos=formulario, error = "PCR no puede ser negativa")
    return 'Ha hecho un post'

@app.route("/jinjaestirao")
def j1():
    return render_template("prueba.txt", provincias=[{'codigo': 'M', 'descripcion': 'Madrid'},
                                                     {'codigo': 'CC', 'descripcion': 'Cáceres'}
                                                    ])