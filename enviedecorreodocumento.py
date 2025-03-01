# par el desarrollo de esta prueba vamos a utilizar las siguientes librerias:
# la instacion de una libreria que permita manipular archivos word
# Las bibliotecas principales son pywin32 para interactuar con Outlook,
# python-docx para manejar documentos de Word, y smtplib para enviar correos. (pip install pywin32 python-docx)
"""
Este ejemplo es practico ya que se utiliza la biblioteca pywin32 para 
interactuar directamente con Outlook, lo cual no requiere autenticación 
explícita (usuario y contraseña) porque utiliza la sesión de Outlook que
 ya está abierta en tu computadora.

"""
import win32com.client as win32 # esta libreria nos permite interactuar con outlook
import os # esta libreria nos permite manipular archivos
from docx import Document # esta libreria nos permite manipular archivos word

# configuración del correo:

destinatario = "aheredia@correo.iue.edu.co"   # aheredia@correo.iue.edu.co
asunto = "Objectivos de proyecto"
cuerpo_correo = """
<html>
<body>
    <h1 style="color: #0044cc;">Hola, Alexander Heredia</h1>
    <p>Espero que te encuentres bien. Adjunto encontrarás el documento Word con los objetivos.</p>
    <p>Por favor, revisa el archivo y no dudes en contactarme si tienes alguna pregunta.</p>
    <p>Saludos,</p>
    <p> Envio programado de correo automatizado</p>
    <p><strong>Agradeceria si me avisaras si te llego el correo</strong></p>
    <p><strong>Alexander Villada</strong></p>
    <p><em>Practicante</em></p>
    <p><em>Bancolombia</em></p>

</body>
</html>
"""

# ruta del archivo word

ruta_documento = r'C:\Users\alexv\OneDrive\Escritorio\PRACTICAS_PROFESIONALES\Bancolombia\proyecto\DEFINICION DE OBJECTIVOS PROYECTO.docx'

#crea el correo
try:
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0) # el 0 indica que es un correo nuevo, 1 sería un correo de respuesta
    mail.To = destinatario
    mail.Subject = asunto
    mail.HTMLBody = cuerpo_correo
 # Adjuntar el archivo word
    mail.Attachments.Add(ruta_documento)
  # Enviar el correo
    mail.Send()
    print("Correo enviado exitosamente")
except Exception as e:
    print(f"Error al enviar el correo: {e}")

