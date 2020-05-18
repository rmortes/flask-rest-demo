from flask import Flask
app = Flask(__name__)

import jinja2
def render(filename, context={}):
    with open(f"templates/{filename}") as f:
        template = jinja2.Template(f.read())
    return template.render(context)

import requests

@app.route('/')
def index():
    min_num = 0
    max_num = 10
    numeros = range(min_num, max_num) # Esta función crea una array con todos los números de min a max, por ejemplo [0,1,2,3,4,5,6,7,8,9]
    context = {
        "min_num": min_num,
        "max_num": max_num,
        "numeros": numeros
    }
    return render("index.html", context)

@app.route('/n/<int:min_num>/<int:max_num>/')
def n(min_num, max_num):
    numeros = range(min_num, max_num) # Esta función crea una array con todos los números de min a max, por ejemplo [0,1,2,3,4,5,6,7,8,9]
    context = {
        "min_num": min_num,
        "max_num": max_num,
        "numeros": numeros
    }
    return render("index.html", context)

@app.route('/d/')
def d():
    titles = ["id", "nombre", "ubicaciones", "geometrías"]
    r = requests.get("https://www.sigua.ua.es/api/pub/departamentosigua/all/items")
    results = r.json()
    context = {
        "titles": titles,
        "results": results,
    }
    return render("datos.html", context)

if __name__ == "__main__":
    app.run('0.0.0.0', 8080, debug=True)