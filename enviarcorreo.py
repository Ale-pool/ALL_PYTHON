# Bueno para realizar este script comenzaremos utilizando estas librerias necesarias

import smtplib  # libreria para enviar correos
from email.mime.multipart import MIMEMultipart # libreria para enviar correos
from email.mime.text import MIMEText # libreria para enviar correos


# vamos a configurar el servidor smtp de gmail

smtp_server = "smtp.gmail.com" # servidor smtp de gmail
smtp_port = 587 # puerto de gmail

# credenciales de la cuenta de correo
email_address = "avila@"
email_password = "qewe"


# crear mensaje

msg = MIMEMultipart()
msg['From'] = email_address
msg['To'] = "luisjalds@gmail.com"
msg['subject'] = "Prueba de envio de correo"

# cuerpo del mensaje en html

html = """

<html>
   <body>
        <h1> Hola, Como estas </h1>
        <h2> espero que te encuentres bien </h2>
        <p> Este es un correo de prueba </p>
        <p> generado automaticamente con python </p>
        <p> Saludos </p>
        <a href="https://alexvillada.neocities.org/"> Ir a mi portafolio</a>
        <p> Esto es un mensaje creado con python, asi que puedes ignoralo </p>
        <p> me avisas si te llego </p>
   </body>
"""


# adjuntar el cuerpo del mensaje en html

msg.attach(MIMEText(html, 'html'))

# enviar el correo

try:
    # iniciar la conexion con el servidor smtp
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls() # iniciar la conexion tls
    server.login(email_address, email_password) # iniciar sesion en el servidor smtp
    
    # enviar el correo
    server.sendmail(email_address, msg['To'], msg.as_string()) # enviar el correo
    print("Correo enviado exitosamente")

except Exception as e:
    print("Error al enviar el correo:", e)

finally:
    # cerrar la conexion con el servidor
    server.quit()