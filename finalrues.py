
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
import time
import numpy as np


class DatosRues:
    def __init__(self, nit, driver_path, url):
        self.nit = nit
        self.driver_path = driver_path
        self.url = url
        self.driver = None

    def configuracion_driver(self):
        options = webdriver.EdgeOptions()
        # options.add_argument("--headless")  # Ejecutar en modo sin cabeza (opcional)
        service = Service(self.driver_path)
        self.driver = webdriver.Edge(service=service, options=options)

    def remover_aviso(self):
        try:
            button_aviso = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'swal2-close'))
            )
            button_aviso.click()
        except TimeoutException:
            print("No se encontró el aviso o ya fue eliminado.")

    def buscar_nit(self):
     try:
        nit_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        nit_input.send_keys(self.nit)

        btn_buscar = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//form//button[contains(text(), 'Buscar')]"))
        )
        btn_buscar.click()
     except TimeoutException:
        print("TimeoutException: No se encontró el campo de entrada NIT.")
        print(self.driver.page_source)  # Imprimir el código fuente de la página para depuración
        self.driver.save_screenshot('screenshot.png')  # Guardar una captura de pantalla para depuración

    def extraer_info_general(self):
        try:
            # Hacer clic en el botón de información general
            info = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/main/div/div/div/div/div[2]/div[2]/div/div[1]/a"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", info)
            time.sleep(2)
            info = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/div/div/div/div/div[2]/div[2]/div/div[1]/a"))
            )
            info.click()
        except (TimeoutException, NoSuchElementException):
            print(f"No se encontró información para el NIT: {self.nit}")
            return [""] * 15 + [self.nit]  # Devuelve cadenas vacías para todas las columnas y el NIT en "no_informacion"

        # Extraer información general
        try:
            data = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/main/div[2]/div[2]/div[1]/div/div[2]/div[1]/div"))
            )
            info_general = data.text
            print(info_general)

            # Procesar la información general
            info_lines = info_general.split('\n')
            data_dic = {}
            for i in range(0, len(info_lines), 2):
                key = info_lines[i].strip()
                value = info_lines[i + 1].strip() if i + 1 < len(info_lines) else ""
                if key == "Identificación":
                    value_split = value.split()
                    value = value_split[1] if len(value_split) > 1 else ""
                data_dic[key] = value

            # Obtener la información de la actividad económica
            actividad = self.driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div[1]/div/div[1]/div[2]/a/span")
            actividad.click()
            actingo = self.driver.find_element(By.ID, "detail-tabs-tabpane-pestana_economica")
            actingo_text = actingo.text
            print(actingo_text)

            actividad_numeros = ''.join(filter(str.isdigit, actingo_text))
            data_dic["Actividad Económica"] = actividad_numeros

            # Definir las columnas y obtener los valores
            columnas = [
                'Identificación', 'Categoria de la Matrícula', 'Tipo de Sociedad', 'Tipo Organización', 'Cámara de Comercio',
                'Número de Matrícula', 'Fecha de Matrícula', 'Fecha de Vigencia', 'Estado de la matrícula',
                'Fecha de renovación', 'Último año renovado', 'Fecha de Actualización', 'Emprendimiento Social',
                'Extinción de Dominio', 'Actividad Económica'
            ]
            valores = [data_dic.get(col, "") for col in columnas]  # Usar cadenas vacías para valores faltantes
            return valores + [""]  # Devuelve cadena vacía en "no_informacion" para NITs con información
        except NoSuchElementException:
            print(f"No se encontró la información general para el NIT: {self.nit}")
            return [""] * 15 + [self.nit]

    def ejecutar(self):
        self.configuracion_driver()
        try:
            self.driver.get(self.url)
            self.remover_aviso()
            self.buscar_nit()
            return self.extraer_info_general()
        finally:
            self.driver.quit()


def main():
    # Leer los NITs desde el archivo Excel
    nits_df = pd.read_excel('data.xlsx')
    nits = nits_df['identificacion_benef'].tolist()

    EDGE_DRIVER_PATH = r'C:\WebDriver\msedgedriver.exe'
    url = "https://ruesfront.rues.org.co/"

    resultados = []
    columnas = [
        'Identificación', 'Categoria de la Matrícula', 'Tipo de Sociedad', 'Tipo Organización', 'Cámara de Comercio',
        'Número de Matrícula', 'Fecha de Matrícula', 'Fecha de Vigencia', 'Estado de la matrícula',
        'Fecha de renovación', 'Último año renovado', 'Fecha de Actualización', 'Emprendimiento Social',
        'Extinción de Dominio', 'Actividad Económica', "No_información"
    ]

    for nit in nits:
        scraper = DatosRues(nit, EDGE_DRIVER_PATH, url)
        valores = scraper.ejecutar()
        resultados.append(valores)

    # Crear el DataFrame y guardar en Excel
    df = pd.DataFrame(resultados, columns=columnas)
    df.to_excel('Resultado_rues.xlsx', index=False, na_rep="")  # Usar cadena vacía para valores faltantes


if __name__ == "__main__":
    main()