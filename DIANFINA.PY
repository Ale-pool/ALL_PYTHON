import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys 
import pandas as pd
import time

class DianRutScraper:
    def __init__(self):
        self.driver = None
        self.resultados = []  # Lista para almacenar los resultados de cada NIT

    def initialize_driver(self):
        options = uc.ChromeOptions()
        self.driver = uc.Chrome(options=options)
        time.sleep(5)
        self.driver.execute_script("window.open('https://muisca.dian.gov.co/WebRutMuisca/DefConsultaEstadoRUT.faces;jsessionid=CFC77365AD7F9859A905646B25050D7E.nodo30Rutmuisca', '_blank')")
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(12)

    def buscar_nit(self, nit):
        try:
            inicio = WebDriverWait(self.driver, 40).until(
                EC.presence_of_element_located((By.ID, "vistaConsultaEstadoRUT:formConsultaEstadoRUT:numNit"))
            )
            inicio.clear()  # Limpiar el campo antes de escribir
            inicio.send_keys(nit)
            inicio.send_keys(Keys.RETURN)
        except TimeoutException:
            print(f"El tiempo de espera ha sido superado para el NIT: {nit}")

    def extract_dv(self):
        try:
            dv = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tipoFilaNormalVerde"))
            )
            return dv.text
        except TimeoutException:
            print("No se pudo extraer el DV")
            return None

    def extract_table_data(self):
        data = {"NIT": None, "DV": None, "Razón Social": None, "Fecha Actual": None, "Estado": None}
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
                        data["Razón Social"] = value
                    elif key == "Fecha Actual":
                        data["Fecha Actual"] = value
                    elif key == "Estado":
                        data["Estado"] = value
        except TimeoutException:
            print("El tiempo de espera ha sido superado para extraer datos de la tabla")
        return data

    def save_to_excel(self, filename="informacion_rut.xlsx"):
        df = pd.DataFrame(self.resultados)
        df.to_excel(filename, index=False)
        print(f"Datos guardados en {filename}")

    def close_driver(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Error al cerrar el navegador: {e}")

    def run(self, nits):
        self.initialize_driver()
        for nit in nits:
            self.buscar_nit(nit)
            dv = self.extract_dv()
            table_data = self.extract_table_data()
            table_data["NIT"] = nit
            table_data["DV"] = dv
            self.resultados.append(table_data)
            time.sleep(5)  # Espera entre consultas para evitar sobrecargar el servidor
        self.save_to_excel()
        self.close_driver()

# Función para extraer datos desde Impala (simulada)
def extraer_datos(query):
    # Simulación de una consulta a Impala
    # En un entorno real, aquí se conectaría a Impala y ejecutaría la consulta
    print(f"Ejecutando consulta: {query}")
    # Simulamos un DataFrame con algunos NITs
    data = {"identificacion_benef": [800150280, 800142383, 900123456, 800987654]}
    return pd.DataFrame(data)

# Ejemplo de uso
if __name__ == "__main__":
    # Obtener los NITs desde Impala
    query = "select distinct identificacion_benef from proceso_auditoria.radegre limit 10"
    nits_df = extraer_datos(query)
    nits = nits_df['identificacion_benef'].tolist()

    # Ejecutar el scraper para todos los NITs
    scraper = DianRutScraper()
    scraper.run(nits)