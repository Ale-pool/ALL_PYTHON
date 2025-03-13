from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
import time
import numpy as np  # Para usar NaN

class DatosRues:
    def __init__(self, nit, driver_path, url):
        self.nit = nit
        self.driver_path = driver_path
        self.url = url
        self.driver = None

    def configuracion_driver(self):
        service = Service(self.driver_path)
        self.driver = webdriver.Edge(service=service)

    def remover_aviso(self):
        try:
            button_aviso = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/button"))
            )
            button_aviso.click()
        except TimeoutException:
            print("No se encontró el aviso o ya fue eliminado.")

    def buscar_nit(self):
        nit_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        nit_input.send_keys(self.nit)

        btn_buscar = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//form//button[contains(text(), 'Buscar')]"))
        )
        btn_buscar.click()

    def extraer_info_general(self):
        info_general = {}
        try:
            info = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/main/div/div/div/div/div[2]/div[2]/div/div[1]/a"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", info)
            time.sleep(2)
            info = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/div/div/div/div/div[2]/div[2]/div/div[1]/a"))
            )
            info.click()
        except TimeoutException:
            print(f"No se encontró información para el NIT: {self.nit}")
            return None  # Retorna None si no se encuentra información
        except NoSuchElementException:
            print(f"No se encontró información para el NIT: {self.nit}")
            return None  # Retorna None si no se encuentra información

        # Extraer información general
        try:
            data = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/main/div[2]/div[2]/div[1]/div/div[2]/div[1]/div"))
            )                                              
            info_general = data.text
            print(info_general)

            info_lines = info_general.split('\n')  # Separar la información por líneas
            data_dic = {}
            for i in range(0, len(info_lines), 2):   # Recorrer la información general
                key = info_lines[i].strip()
                value = info_lines[i+1].strip() if i+ 1 < len(info_lines) else ""
                if key in "Identificación":
                    value = value.split()[1]
                data_dic[key] = value
            
            # Obtener la información de la actividad económica
            actividad = self.driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div[1]/div/div[1]/div[2]/a/span")
            actividad.click()
            actingo = self.driver.find_element(By.ID, "detail-tabs-tabpane-pestana_economica")
            actingo_text = actingo.text
            print(actingo_text)

            data_dic["Actividad Económica"] = actingo_text
            columnas = ['Identificación', 'Categoria de la Matrícula','Tipo de Sociedad','Tipo Organización','Cámara de Comercio',
                        'Número de Matrícula','Fecha de Matrícula','Fecha de Vigencia','Estado de la matrícula',
                        'Fecha de renovación', 'Último año renovado', 'Fecha de Actualización', 'Emprendimiento Social','Extinción de Dominio', 'Actividad Económica']
            valores = [data_dic.get(col, np.nan) for col in columnas]  # Usar np.nan para valores faltantes
            return valores
        except NoSuchElementException:
            print(f"No se encontró la información general para el NIT: {self.nit}")
            return None  # Retorna None si no se encuentra información
        
        return None

    def ejecutar(self):
        self.configuracion_driver()
        try:
            self.driver.get(self.url)
            self.remover_aviso()
            self.buscar_nit()
            return self.extraer_info_general()
        finally:
            self.driver.quit()

if __name__ == "__main__":
    # Leer los NITs desde el archivo Excel
    nits_df = pd.read_excel('data.xlsx')
    nits = nits_df['identifi_benefi'].tolist()

    EDGE_DRIVER_PATH = r'C:\WebDriver\msedgedriver.exe'
    url = "https://ruesfront.rues.org.co/"

    resultados = []
    for nit in nits:
        scraper = DatosRues(nit, EDGE_DRIVER_PATH, url)
        resultado = scraper.ejecutar()
        if resultado is not None:
            resultados.append(resultado)
        else:
            # Si no se encuentra información, se añade una fila con NaN para todas las columnas
            columnas = ['Identificación', 'Categoria de la Matrícula','Tipo de Sociedad','Tipo Organización','Cámara de Comercio',
                        'Número de Matrícula','Fecha de Matrícula','Fecha de Vigencia','Estado de la matrícula',
                        'Fecha de renovación', 'Último año renovado', 'Fecha de Actualización', 'Emprendimiento Social','Extinción de Dominio', 'Actividad Económica']
            resultados.append([np.nan] * len(columnas))  # Añade una fila de NaN

    # Guardar los resultados en un nuevo archivo Excel
    columnas = ['Identificación', 'Categoria de la Matrícula','Tipo de Sociedad','Tipo Organización','Cámara de Comercio',
                'Número de Matrícula','Fecha de Matrícula','Fecha de Vigencia','Estado de la matrícula',
                'Fecha de renovación', 'Último año renovado', 'Fecha de Actualización', 'Emprendimiento Social','Extinción de Dominio', 'Actividad Económica']
    resultados_df = pd.DataFrame(resultados, columns=columnas)
    resultados_df.to_excel('resultados_nits.xlsx', index=False)