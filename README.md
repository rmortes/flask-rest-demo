# flask-rest-demo
Demostración de aplicación mínima utilizando Python+Flask+Jinja2+REST

## Primer paso: Setup

Para esta demostración vamos a usar:

- Python: El lenguaje de programación en el que va a estar escrito el servidor
- Flask: El framework que va a hacer funcionar el servidor
- Jinja2: El motor de plantilla que nos va a ayudar a servir la web
- REST: El protocolo de comunicación del que nos vamos a servir

Para ejecutar el primer paso tendremos que instalar en nuestro sistema python, y asegurarnos que tanto el comando `python` como el comando `pip` funcionan. Para esta demostración voy a usar `python3.8`.

Una vez que Python esté instalado, ejecutamos `pip install -r requirements.txt` para instalar flask, jinja2 y requests

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

## Cuarto paso: Pasando argumentos

¿Y si tengo que pasarle argumentos a una URL?
Pongamos el ejemplo de querer especificar, en la URl, que número quiero que sea el primero, y cual quiero que sea el último. En este caso podríamos usar una caracterísitica de Flask para pasar argumentos a una función de vista.

Poganmos que la nueva ruta va a ser `/n/0/10/`. Para eso creamos una nueva función:
```python
@app.route('/n/<int:min_num>/<int:max_num>/')
def n(min_num, max_num):
    numeros = range(min_num, max_num) # Esta función crea una array con todos los números de min a max, por ejemplo [0,1,2,3,4,5,6,7,8,9]
    context = {
        "min_num": min_num,
        "max_num": max_num,
        "numeros": numeros
    }
    return render("index.html", context)
```

Intenta acceder ahora a [localhost:8080/n/7/12/](localhost:8080/n/7/12). ¡Todo está funcionando!

## Quinto paso: Llamando a REST

Ahora que podemos mostrar los datos, es hora de conseguirlos. Para este ejemplo voy a utilizar la API de [SigUA](https://www.sigua.ua.es/), más concreamente, el punto de enlace para recuperar [todos los departamentos](https://www.sigua.ua.es/api/pub/departamentosigua/all/items). Según la [documentación oficial](https://bitbucket.org/SIGUA/apirest-doc/src/master/specs.mkd), este punto de enlace devuelve una array de objetos con la siguiente forma:
```json
{"properties":{
    "count_geometrias": {
        "type":"integer",
        "required":true,
        "description":"Recuento de registros de geometría vinculados a la unidad organizativa."
    },
    "count_ubicaciones": {
        "type":"number",
        "required":true,
        "description":"Recuento de registros de ubicación de personal vinculado a la unidad organizativa."
    },
    "id": {
        "type":"string",
        "required":true
    },
    "nombre": {\d{2}
        "type":"string",
        "required":true
        "description":"Nombre de la unidad organizativa."
    }}}
```

Para recuperar todos estos datos en un formato cómodo para python, no hemos de hacer más que una llamada REST, y convertir el resultado de JSON a un objeto de python. Esto lo vamos a hacer, sencillamente, con el módulo `requests`.

Vamos a crear una nueva plantilla llamada `datos.html`, que va a contener la esctructura para imprimir una tabla en HTML, y una nueva función en la url `/d`
```html
<h1>Datos</h1>
<table style="width:100%">
  <tr>
    {% for title in titles %}<th>{{title}}</th>{% endfor %}
  </tr>
  {% for row in results %}
  <tr>
    {% for col in row.values() %}<td>{{col}}</td>{% endfor %}
  </tr>
  {% endfor %}
</table>
```
```python
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
```

Y así, con una cantidad mínima de código, puedes mostrar datos REST cómodamente en tu navegador