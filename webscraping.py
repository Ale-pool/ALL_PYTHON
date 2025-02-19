from selenium.webdriver import Chrome # Import the Chrome class from selenium.webdriver
from webdriver_manager.chrome import ChromeDriverManager # importamos el ChromeDriverManager 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time

# segun lo que queremos hacer es tomar en cuenta nuestro usuario y contraseña como varibles globales

USER = 'standard_user'
PASSWORD = 'secret_sauce'
NAME = 'Alex'
LASTNAME = 'Villada'
POSTAL = '055420'
def main():
    service = Service(ChromeDriverManager().install()) # instala el driver
    option = webdriver.ChromeOptions() # aqui puedo pasar opciones para el navegador
    # option.add_argument("--incognito") # abre el navegador en modo incognito
    option.add_argument("window-size=1920,1080") # tamaño de la ventana
    driver = Chrome(service=service, options=option)  # inicializa el driver con el servicio y las opciones
    driver.get("https://www.saucedemo.com/v1/") # abre la pagina
    # login
    user_input = driver.find_element(By.ID, "user-name") # busca el elemento por ID
    user_input.send_keys(USER)  # enviamos el texto USER
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(PASSWORD) # enviamos el texto PASSWORD
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click() # clickeamos el boton login

    # comprar

    botones = driver.find_elements(By.XPATH, "//button[contains(@class, 'btn_primary') and contains(@class, 'btn_inventory')]")
    botones[0].click() # clickeamos el segundo boton
    botones[5].click() 
    # btn1 = driver.find_element(By.XPATH, "//button[contains(@class, 'btn_primary') and contains(@class, 'btn_inventory')]") # busca el elemento por XPATH, se puede usar tambien el metodo find_element_by_xpath
    # BTN2 = driver.find_element(By.NAME, "btn_primary btn_inventory") # busca el elemento por NAME
    carrito = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    carrito.click()
    checa = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[3]/div/div[2]/a[2]")  
    checa.click()

    # llenar información
    name = driver.find_element(By.ID, "first-name")
    name.send_keys(NAME)
    lastname = driver.find_element(By.ID, "last-name")
    lastname.send_keys(LASTNAME)
    postalcode = driver.find_element(By.ID, "postal-code")
    postalcode.send_keys(POSTAL)

    # continuar
    seguir = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[3]/div/form/div[2]/input")
    seguir.click()

    # finalizar

    fin = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[3]/div/div[2]/div[8]/a[2]")
    fin.click()
    # btn1.click() # clickeamos el boton
    time.sleep(8) # espera 5 segundos
    driver.quit() # cierra el navegador

if __name__ == "__main__":
    main()
