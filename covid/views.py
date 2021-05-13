#Aqui estarán todas las rutas que tengan relacion con la aplicacion Covid
from covid import app
import csv 
import json

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
    fichero = open("data/provincias.csv", "r", encoding="utf8")

    dictreader = csv.DictReader(fichero, fieldnames=['codigo', 'provincia']) #Otra manera de hacer lo de arriba.. leer el fichero y que nos cree un dict al mismo tiempo
    for registro in dictreader:
        if registro['codigo'] == codigoProvincia:
            fichero.close()
            return registro['provincia']
    
    fichero.close()
    return "El valor no existe"

@app.route("/casos/<int:year/<int:mes>/<int:dia>")
def casos(year, mes, dia):
    