import requests

# URL para obtener el token
url_token = 'https://ruesapi.rues.org.co/WEB2/api/Token/ObtenerToken'

# Realizar la solicitud POST para obtener el token
response_token = requests.post(url_token)

# Verificar si la solicitud fue exitosa
if response_token.status_code == 200:
    # Extraer el token del encabezado de la respuesta
    token = response_token.headers.get('token:uesapi')  # El token está en este encabezado
    if token:
        print(f"Token obtenido: {token}")
    else:
        print("No se encontró el token en los encabezados de la respuesta.")
else:
    print(f"Error al obtener el token: {response_token.status_code}")


# URL para la consulta avanzada
url_consulta = 'https://ruesapi.rues.org.co/api/ConsultasRUES/BusquedaAvanzadaRM'

# Datos de la consulta (ajusta según sea necesario)
data_consulta = {
    # Aquí debes incluir los parámetros necesarios para la consulta avanzada
    # Por ejemplo:
    "nit": "891190346",  # Cambia este valor por el NIT que deseas consultar
    "otros_parametros": "valor"  # Ajusta según la API
}

# Encabezados de la solicitud (incluyendo el token)
headers = {
    'token:uesapi': token,  # Usamos el token obtenido
    'Content-Type': 'application/json'
}

# Realizar la solicitud POST para consultar
response_consulta = requests.post(url_consulta, json=data_consulta, headers=headers)

# Verificar si la solicitud fue exitosa
if response_consulta.status_code == 200:
    # Mostrar el resultado en formato JSON
    print(response_consulta.json())
else:
    print(f"Error en la consulta: {response_consulta.status_code}")