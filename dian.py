import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os
import pandas as pd
import time
import pyodbc


#  
def extraer_datos(query):
        lz_con = pyodbc.connect("DSN=impala-virtual-prd", autocommit=True)
        data = pd.read_sql(query, lz_con)
        lz_con.close()
        return data



class DianRutScraper:
    def __init__(self, nit):
        self.nit = nit
        self.driver = None
        self.data = {"NIT": nit, "DV": None, "Razón Social": None, "Fecha Actual": None, "Estado": None}

    def initialize_driver(self):
        options = uc.ChromeOptions()
        self.driver = uc.Chrome(options=options)
        time.sleep(5)
        self.driver.execute_script("window.open('https://muisca.dian.gov.co/WebRutMuisca/DefConsultaEstadoRUT.faces;jsessionid=CFC77365AD7F9859A905646B25050D7E.nodo30Rutmuisca', '_blank')")
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(12)

    def search_nit(self):
        try:
            inicio = WebDriverWait(self.driver, 40).until(
                EC.presence_of_element_located((By.ID, "vistaConsultaEstadoRUT:formConsultaEstadoRUT:numNit"))
            )
            inicio.send_keys(self.nit)
            inicio.send_keys(Keys.RETURN)
        except TimeoutException:
            print("El tiempo de espera ha sido superado")

    def extract_dv(self):
        try:
            dv = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tipoFilaNormalVerde"))
            )
            self.data["DV"] = dv.text
        except TimeoutException:
            print("No se pudo extraer el DV")

    def extract_table_data(self):
        try:
            table = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:formulario"]/tbody/tr[2]/td/table'))
            )
            rows = table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) == 2:
                    key = cells[0].text.strip()
                    value = cells[1].text.strip()
                    if key == "Razón Social":
                        self.data["Razón Social"] = value
                    elif key == "Fecha Actual":
                        self.data["Fecha Actual"] = value
                    elif key == "Estado":
                        self.data["Estado"] = value
        except TimeoutException:
            print("El tiempo de espera ha sido superado")

    def save_to_excel(self, filename="informacion_rut.xlsx"):
        df = pd.DataFrame([self.data])
        df.to_excel(filename, index=False)
        print(f"Datos guardados en {filename}")

    def close_driver(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Error al cerrar el navegador: {e}")

    def run(self):
        self.initialize_driver()
        self.search_nit()
        self.extract_dv()
        self.extract_table_data()
        self.save_to_excel()
        time.sleep(40)
        self.close_driver()

# Ejemplo de uso
if __name__ == "__main__":
    nit = 800142383
    scraper = DianRutScraper(nit)
    scraper.run()