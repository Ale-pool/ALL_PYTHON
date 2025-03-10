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

from selenium import webdriver
from selenium.webdriver.common.by import By
import time  
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

# nit = int(input("Ingrese el NIT: "))
nit = 800150280
edge_driver_path = r'C:\WebDriver\msedgedriver.exe'
Service = Service(edge_driver_path)
driver = webdriver.Edge(service=Service)

# abrir la pagina
driver.get("https://ruesfront.rues.org.co/")

# eliminar el aviso 
button_aviso = driver.find_element(By.XPATH, "/html/body/div[2]/div/button")
button_aviso.click()

# ingresar el nit
nit_input = driver.find_element(By.ID, "search")
nit_input.send_keys(nit)

# hacer click en buscar

btn_buscar = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div[2]/form/button[2]")
btn_buscar.click()



# vamos a ver la información general
try:
    # desplazarse hasta el elemento
    info = wait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/main/div/div/div/div/div[2]/div[2]/div/div[1]/a"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", info)
    time.sleep(2)  # agregar un pequeño retraso
    info = wait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/div/div/div/div/div[2]/div[2]/div/div[1]/a"))
    )
    info.click()
except Exception as e:
    print(f"No se encuentra la información: {e}")


time.sleep(8)
driver.quit()