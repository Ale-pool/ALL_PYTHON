# para la realizacion de este script necesitaremos las siguientes librerias
# pandas - para leer y manipular archivos excel  (pip install pandas openpyxl)
# openpyxl - para trabajar con archivos excel
# smtplib - para enviar correos
# email - para construir correos electronicos

import pandas as pd

# vamos a leer el archivo excel

df = pd.read_excel(r'c:\Users\alexv\OneDrive\Documentos\datos_prueba.xlsx')

# ahora vamos a convertir el dataframe en un archivo html

html_table = df.to_html(index=False, border=1) # convertir el dataframe en una tabla html

# anadir estilo css para mejorar la presentacion de la tabla

html_content = f"""
    <html>
        <head>
            <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    font-family: Arial, sans-serif;
                }}
                th, td {{
                    border: 1px solid #dddddd;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                    color: #333;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
                tr:hover {{
                    background-color: #f1f1f1;
                }}
            </style>
        </head>
        <body>
            <h1>Tabla de Datos</h1>
            <h2>Este es un correo de prueba con una tabla de datos</h2>
            <p>Estimado usuario Valentina, a continuacion se presenta una tabla con los datos de prueba:
              por cuestiones de prueba y de test de la aplicacion, se estara enviando automaticamente este correo
                con la tabla de datos que se encuentra en el archivo excel adjunto, se enviara cada 2 horas durante
                la fecha Indicada en este correo datetime.datetime.now()
            </p>
            {html_table}
            <p>Cualquier comentario o sugerencia es bien recibida, ver el codigo en github a la direccion https://github.com/Ale-pool/ALL_PYTHON </p>
            <p>Saludos</p>
            <p>Alex</p>
        </body> 
    </html>
"""


# configurar el envio del correo electronico

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Configurar los detalles del correo
outlook_address = "avill@correo.iue.edu.co"
outlook_password = "Alexvillada123"
destinatario = "vcans@correo.iue.edu.co"
asunto = "Tabla de datos en HTML"
# "valetinacano2212@gmail.com"
# Crear el mensaje
mensaje = MIMEMultipart()
mensaje["From"] = outlook_address
mensaje["To"] = destinatario
mensaje["Subject"] = asunto

# Añadir el contenido HTML al mensaje
mensaje.attach(MIMEText(html_content, "html"))

# Enviar el correo
try:
    # Configurar el servidor SMTP (en este caso, Gmail)
    servidor = smtplib.SMTP("smtp.office365.com", 587)
    servidor.starttls()  # Encriptar la conexión
    servidor.login(outlook_address, outlook_password)  # Usa una contraseña de aplicación si usas Gmail
    servidor.sendmail(outlook_address, destinatario, mensaje.as_string())
    print("Correo enviado exitosamente.")
except Exception as e:
    print(f"Error al enviar el correo: {e}")
finally:
    servidor.quit()  # Cerrar la conexión con el servidor