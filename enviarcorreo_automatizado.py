import pandas as pd
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import time
import schedule

# Función para enviar el correo
def enviar_correo():
    # Leer el archivo Excel
    df = pd.read_excel(r'c:\Users\alexv\OneDrive\Documentos\datos_prueba.xlsx')

    # Convertir el DataFrame en una tabla HTML
    html_table = df.to_html(index=False, border=1)

    # Obtener la fecha y hora actual
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Añadir estilo CSS para mejorar la presentación de la tabla
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
                <p>Estimado usuario Valentina, a continuación se presenta una tabla con los datos de prueba:
                  por cuestiones de prueba y de test de la aplicación, se estará enviando automáticamente este correo
                    con la tabla de datos que se encuentra en el archivo Excel adjunto. Se enviará cada 2 horas durante
                    la fecha indicada en este correo: {fecha_actual}
                </p>
                {html_table}
                <p>Cualquier comentario o sugerencia es bien recibida. Ver el código en GitHub a la dirección: 
                <a href="https://github.com/Ale-pool/ALL_PYTHON">https://github.com/Ale-pool/ALL_PYTHON</a></p>
                <p>Saludos,</p>
                <p>Alex</p>
            </body>
        </html>
    """

    # Configurar los detalles del correo
    outlook_address = "avillad"
    outlook_password = "bd"  # Usar variables de entorno para la contraseña
    destinatario = "luisjalds@gmail.com"
    asunto = "Tabla de datos en HTML"

    # Crear el mensaje
    mensaje = MIMEMultipart()
    mensaje["From"] = outlook_address
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto

    # Añadir el contenido HTML al mensaje
    mensaje.attach(MIMEText(html_content, "html"))

    # Enviar el correo
    try:
        # Configurar el servidor SMTP de Outlook
        servidor = smtplib.SMTP("smtp.gmail.com", 587)    # gmail
        servidor.starttls()  # Encriptar la conexión
        servidor.login(outlook_address, outlook_password)
        servidor.sendmail(outlook_address, destinatario, mensaje.as_string())
        print(f"Correo enviado exitosamente el {fecha_actual}.")
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")
    finally:
        servidor.quit()  # Cerrar la conexión con el servidor

# Programar el envío del correo cada 2 horas
schedule.every(2).hours.do(enviar_correo)

# Bucle para mantener el script en ejecución
print("El programa está en ejecución. Presiona Ctrl+C para detenerlo.")
while True:
    schedule.run_pending()
    time.sleep(1)  # Esperar 1 segundo antes de revisar nuevamente la programación






# si queremos en el ciclo while que se ejecute en relación a una fecha predeterminada podemos hacerlo de la siguiente manera
# from datetime import datetime

# # Definir el período de ejecución
# fecha_inicio = datetime(2023, 10, 1)  # 1 de octubre de 2023
# fecha_fin = datetime(2023, 10, 5)     # 5 de octubre de 2023

# while True:
#     ahora = datetime.now()
#     if fecha_inicio <= ahora <= fecha_fin:
#         schedule.run_pending()
#     elif ahora > fecha_fin:
#         print("El período de ejecución ha terminado.")
#         break
#     time.sleep(1)  # Esperar 1 segundo antes de revisar nuevamente la programación
# # esto nos permitira que el ciclo while se ejecute en un rango de fechas determinado