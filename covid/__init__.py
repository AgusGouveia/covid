#Aqui crearemos nuestra aplicación
from flask import Flask

app = Flask(__name__)

from covid import views