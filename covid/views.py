#Aqui estarán todas las rutas que tengan relacion con la aplicacion Covid
from covid import app

@app.route("/")
def index():
    return "Ya está funcionando desde views!"