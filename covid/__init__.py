#Aqui crearemos nuestra aplicación
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Ya está funcionando!"