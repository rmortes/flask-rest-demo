# flask-rest-demo
Demostración de aplicación mínima utilizando Python+Flask+Jinja+REST

## Primer paso: Setup

Para esta demostración vamos a usar:

- Python: El lenguaje de programación en el que va a estar escrito el servidor
- Flask: El framework que va a hacer funcionar el servidor
- Jinja: El motor de plantilla que nos va a ayudar a servir la web
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