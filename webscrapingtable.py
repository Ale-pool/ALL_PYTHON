# vamos a realizar un nuevo web scraping para sacar valores de una tabla importantes

import requests  # libreria para hacer peticiones a la web, get, post, put, delete 
from bs4 import BeautifulSoup   # libreria para hacer web scraping, parsear el html
import pandas as pd    # libreria para trabajar con dataframes, manipular y analizar datos

# obtenemos la url de la pagina

url = "https://www.superfinanciera.gov.co/publicaciones/10115493/superfinanciera-certifica-el-interes-bancario-corriente/#:~:text=La%20nueva%20certificaci%C3%B3n%20representa%20un,2025%20(16%2C59%25).&text=Las%20tasas%20de%20inter%C3%A9s%20bancario,28%20de%20febrero%20de%202025."

# solicitar la solicitud a la pagina web http:

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")  # parsear el html, el contenido de la pagina

# encontrar la tabla en el contenido html 

tables = soup.find_all('table') # encontrar la tabla en el contenido html

# vamos a extraer las filas de la tabla

# rows = tables[1].find_all('tr')  # encontrar todas las filas de la tabla

# vamos a extraer los datos de la tabla

# data = []

# for row in rows:
#     cols = row.find_all('td')  # encontrar todas las columnas de la fila
#     cols = [col.text.strip() for col in cols] # extraer el texto de cada columna, eliminar espacios en blanco
#     data.append(cols)  # agregar los datos de la fila a la lista de datos

# crear un dataframe con los datos
# df = pd.DataFrame(data[1:], columns=data[0])  # crear un dataframe con los datos, la primera fila es el encabezado

# print(df) # imprimir el dataframe


# si la pagina utiliza tablas dinamicas es posible que necesitemos utilizar librerias como selenium
# ya que selenium es una libreria que permite interactuar con paginas web dinamicas, hacer click, scroll, etc
# tambien podemos utilizar la libreria scrapy que es una libreria especializada en web scraping


#######################  Si quiero por ejemplo sacar, es decir optener un valor  #######################3
    # especifico de la tabla o de la url, como en la segunda tabla en la columna de usura(efectivo anual) en la fila credito productivo rural
                                # se puede hacer de la siguiente manera:


if len(tables) > 1:
    table = tables[1] # obtener la segunda tabla
    # estraer las filas de la tablas
    rows = table.find_all('tr')

    # bsucar la fila que contiene " Credito productivo rural"
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 0 and "Crédito popular productivo urbano" in cols[0].text.strip():
            #Extraer el valor de la columna usura(efectivo anual)
            usura_value = cols[2].text.strip() # extraer el valor de la columna usura(efectivo anual)
            print(f"La usura(efectivo anual) para el credito productivo rural es: {usura_value}")
            break
else:
    print("No se encontro la tabla")