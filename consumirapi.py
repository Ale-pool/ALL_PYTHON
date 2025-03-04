"""
Una API (Interfaz de Programación de Aplicaciones) es un conjunto de reglas 
y protocolos que permite que diferentes aplicaciones se comuniquen entre sí. 
Básicamente, es una forma de solicitar y recibir datos de un servidor.

"""

import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

# hacer la solicitud get
response = requests.get(url)  # hacer una solicitud get a la url

# verificar si la solicitud fue exitosa (estado 200)

if response.status_code == 200:
    #convertir la respuesta a json
    data = response.json()
    print(data)
else:
    print(f"Error al hacer la solicitud: {response.status_code}")


    # Paso 5: Entender la respuesta

print(data['title'])  # Imprime el título del post

# vamos a hacer una solicitud post

import requests

url = "https://jsonplaceholder.typicode.com/posts"
new_post = {
    "title": "foo",
    "body": "bar",
    "userId": 1
}

response = requests.post(url, json=new_post)

if response.status_code == 201:  # 201 significa "Creado"
    print(response.json())
else:
    print(f"Error: {response.status_code}")


# put request

import requests

url = "https://jsonplaceholder.typicode.com/posts/1"
updated_post = {
    "title": "foo updated",
    "body": "bar updated",
    "userId": 1
}

response = requests.put(url, json=updated_post)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")


# delete request

import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

response = requests.delete(url)

if response.status_code == 200:
    print("Post eliminado")
else:
    print(f"Error: {response.status_code}")


"""
Paso 7: Manejar errores y excepciones
Es importante manejar errores y excepciones para que tu aplicación no se rompa si algo sale mal. 
Puedes usar bloques try-except para esto:"""


import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

try:
    response = requests.get(url)
    response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa
    data = response.json()
    print(data)
except requests.exceptions.HTTPError as errh:
    print(f"Error HTTP: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"Error de conexión: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Timeout: {errt}")
except requests.exceptions.RequestException as err:
    print(f"Error: {err}")


"""
Paso 8: Autenticación y headers
Algunas APIs requieren autenticación. Esto se puede hacer mediante headers o parámetros de la URL. 
Aquí tienes un ejemplo con headers:
"""

import requests

url = "https://api.github.com/user"
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")


"""
Paso 9: Paginación y parámetros de consulta
Algunas APIs devuelven grandes cantidades de datos y utilizan paginación.
 Puedes manejar esto con parámetros de consulta:
"""
import requests

url = "https://jsonplaceholder.typicode.com/posts"
params = {
    "_limit": 10,  # Limitar a 10 resultados
    "_page": 2     # Página 2
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")