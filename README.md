# flask-rest-demo
Demostración de aplicación mínima utilizando Python+Flask+Jinja2+REST

## Primer paso: Setup

Para esta demostración vamos a usar:

- Python: El lenguaje de programación en el que va a estar escrito el servidor
- Flask: El framework que va a hacer funcionar el servidor
- Jinja2: El motor de plantilla que nos va a ayudar a servir la web
- REST: El protocolo de comunicación del que nos vamos a servir

Para ejecutar el primer paso tendremos que instalar en nuestro sistema python, y asegurarnos que tanto el comando `python` como el comando `pip` funcionan. Para esta demostración voy a usar `python3.8`.

Una vez que Python esté instalado, ejecutamos `pip install -r requirements.txt` para instalar flask y jinja

## Segundo paso: Creamos la base del servidor

El segundo paso es comprobar que flask está funcionando y que podemos servir un hello world en nuestra aplicación

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello world!"

if __name__ == "__main__":
    app.run('0.0.0.0', 8080, debug=True)
```

Puede que debas permitir el acceso en tu firewall para que funcione, y ya deberías de recibir un `Hello world!` en [localhost:8080](localhost:8080)

## Tercer paso: Servir plantillas

¿Que es una plantilla? Puedes pensarla como html con agujeros, pero con Jinja2 puedes hacer decenas de cosas extra, como añadirles bucles o llamar a funciones.

En este paso a renderizar en '/' un archivo '.html'. Crea una carpeta 'templates' y añade 'index.html' tal que así:

```jinja2
<h1>Hello, world!</h1>
Numeros del {{ min_num }} al {{ max_num }}:

<ul>
{% for num in numeros %}
    <li>{{ num }}</li>
{% endfor %}
</ul>
```

Lo que esto va a hacer es imprimir autmáticamente una lista de los números que le digamos en el servidor. Intenta imprimir la plantilla en el servidor, añadiendo esta función, que lee un archivo del disco y te lo devuelve listo para ser impreso
```python
import jinja2
def render(filename, context={}):
    with open(f"templates/{filename}") as f:
        template = jinja2.Template(f.read())
    return template.render(context)
```

Y modificando el servidor para que, en lugar de devolver un texto devuelvas el archivo
```python
@app.route('/')
def index():
    return render("index.html")
```

Si a estas alturas los pruebas, verás que no hace nada. ¿Por que? Porque no tiene el contexto. En la plantilla tenemos las siguientes variables: `min_num`, `max_num` y `numeros`. Crealas en el código, y pásaselas

```python
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
```

¡Ahora la plantilla se ve como te tiene que ver!
