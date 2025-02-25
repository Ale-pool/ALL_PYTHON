# https://github.com/UB-Mannheim/tesseract/wiki # Instalacion de tesseractx
# Primero vamos a instalar las librerias necesarias para este script 
# vamos a usar Tesseract el cual es un motor de reconocimiento optico de caracteres (OCR)
# y vamos a utilizar pytesseract es un wrapper para python de tesseract
# usaremos pillow para manipular imagenes

# importe de las librerias necesarias

from PIL import Image
import pytesseract
import os

# Especificar la ruta de Tesseract manualmente
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Especificar la ruta de la imagen
image_path = "Model/ocr.png"

# Verificar si el archivo existe
if not os.path.exists(image_path):
    print(f"Error: No se encontró el archivo '{image_path}'. Verifica la ruta.")
else:
    # Cargar la imagen
    image = Image.open(image_path)

    # Aplicar OCR
    texto_extraido = pytesseract.image_to_string(image, lang='spa')

    # Mostrar el texto extraído
    print("TEXTO EXTRAÍDO DE LA IMAGEN:")
    print(texto_extraido)

    # Guardar el texto en un archivo
    with open("texto_extraido.txt", "w", encoding="utf-8") as archivo:
        archivo.write(texto_extraido)
    print("El texto se ha guardado en 'texto_extraido.txt'.")