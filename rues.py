from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
import time

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
            print("No se encontró el enlace de 'Información General'.")
            return info_general
        except NoSuchElementException:
            print("No se encontró el elemento de 'Información General'.")
            return info_general

        # Extraer información general
        try:
            data = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/main/div[2]/div[2]/div[1]/div/div[2]/div[1]/div"))
            )
            print(data.text)
            info_general['Información General'] = data.text
        except NoSuchElementException:
            print("No se encontró la información general.")
        
        return info_general
    
    def extraer_actividad_economica(self):
        try:
            actividad = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/div[2]/div[2]/div[1]/div/div[1]/div[2]/a/span"))
            )
            actividad.click()
            time.sleep(2)

            data = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/main/div[2]/div[2]/div[1]/div/div[2]/div[2]"))
            )
            print(data.text)
        except NoSuchElementException:
            print("No se encontró la información de actividad económica.")
        except TimeoutException:
            print("No se pudo cargar la información de actividad económica.")

    def ejecutar(self):
        self.configuracion_driver()
        try:
            self.driver.get(self.url)
            self.remover_aviso()
            self.buscar_nit()
            info_general = self.extraer_info_general()
            self.extraer_actividad_economica()

            if info_general:
                df = pd.DataFrame(list(info_general.items()), columns=["Campo", "Valor"])
                df.to_excel('informacion_empresa.xlsx', index=False)
                print("Información guardada en 'informacion_empresa.xlsx'")
            else:
                print("No se pudo extraer la información general.")
        finally:
            self.driver.quit()

if __name__ == "__main__":
    NIT = int(input("Ingrese el NIT de la empresa a buscar: "))  # NIT de la empresa a buscar
    EDGE_DRIVER_PATH = r'C:\WebDriver\msedgedriver.exe'
    url = "https://ruesfront.rues.org.co/"

    scraper = DatosRues(NIT, EDGE_DRIVER_PATH, url)
    scraper.ejecutar()