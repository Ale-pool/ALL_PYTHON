import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class ValidarOrdenPago:
    def __init__(self, datos_orden_pago, datos_tabla):
        """
        Inicializa la clase con los datos de la orden de pago y la tabla generada.
        
        :param datos_orden_pago: Diccionario con los datos de la orden de pago (OCR).
        :param datos_tabla: Diccionario con los datos de la tabla generada.
        """
        self.datos_orden_pago = datos_orden_pago
        self.datos_tabla = datos_tabla
        self.alertas = []  # Lista para almacenar alertas de discrepancias

    def validar_campos(self):
        """
        Compara los campos clave entre la orden de pago y la tabla.
        Genera alertas si hay discrepancias.
        """
        # Campos clave a validar
        campos_a_validar = [
            "numero_orden_archivo",
            "no_de_orden",
            "tipo_transaccion",
            "valor_neto",
            "codigo",
            "numero_cta_a_debitar",
            "identificacion"
        ]

        for campo in campos_a_validar:
            valor_orden = self.datos_orden_pago.get(campo)
            valor_tabla = self.datos_tabla.get(campo)

            if valor_orden != valor_tabla:
                self.alertas.append(
                    f"Alerta: Discrepancia en '{campo}'. "
                    f"Orden: {valor_orden}, Tabla: {valor_tabla}"
                )

    def mostrar_alertas(self):
        """
        Muestra las alertas generadas durante la validación.
        """
        if not self.alertas:
            print("¡Todo en orden! No se encontraron discrepancias.")
        else:
            print("Se encontraron las siguientes alertas:")
            for alerta in self.alertas:
                print(alerta)
    

    def enviar_alertas_por_correo(self, destinatario, remitente, password):
        """
        Envía las alertas por correo electrónico en formato HTML.
        
        :param destinatario: Correo electrónico del destinatario.
        :param remitente: Correo electrónico del remitente.
        :param password: Contraseña del correo del remitente.
        """
        if not self.alertas:
            print("No hay alertas para enviar.")
            return

        # Crear el mensaje de correo
        mensaje = MIMEMultipart()
        mensaje['From'] = remitente
        mensaje['To'] = destinatario
        mensaje['Subject'] = "Alertas de Validación de Orden de Pago"

        # Crear el cuerpo del correo en HTML
        html = f"""
        <html>
            <body>
                <h2>Alertas de Validación de Orden de Pago</h2>
                <p>Se encontraron las siguientes discrepancias:</p>
                <ul>
        """
        for alerta in self.alertas:
            html += f"<li>{alerta}</li>"
        html += """
                </ul>
                <p>Por favor, revise los datos y tome las acciones necesarias.</p>
            </body>
        </html>
        """

        # Adjuntar el cuerpo HTML al mensaje
        mensaje.attach(MIMEText(html, 'html'))

        # Enviar el correo
        try:
            with smtplib.SMTP('smtp.office365.com', 587) as servidor:
                servidor.starttls()  # Encriptación TLS
                servidor.login(remitente, password)
                servidor.sendmail(remitente, destinatario, mensaje.as_string())
            print("Correo enviado exitosamente.")
        except Exception as e:
            print(f"Error al enviar el correo: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    # Datos de ejemplo de la orden de pago (OCR)
    datos_orden_pago = {
        "numero_orden": "1991746",
        "tipo_transaccion": "PAGO PROVEEDORES",
        "valor_bruto": "$226,678,291.00",
        "valor_neto": "$226,678,291.00",
        "beneficiario": "Proveedor A",
        "moneda": "COP"
    }

    # Datos de ejemplo de la tabla generada
    datos_tabla = {
        "numero_orden": "1991746",
        "tipo_transaccion": "PAGO PROVEEDORES",
        "valor_bruto": "$226,678,291.00",
        "valor_neto": "$226,678,291.00",
        "beneficiario": "Proveedor B",  # Discrepancia en el beneficiario
        "moneda": "COP"
    }

    # Crear instancia de la clase y validar
    validador = ValidarOrdenPago(datos_orden_pago, datos_tabla)
    validador.validar_campos()
    validador.mostrar_alertas()

    # Enviar alertas por correo (configura tus credenciales de Outlook)
    destinatario = "auditor@empresa.com"  # Correo del auditor
    remitente = "tucorreo@outlook.com"   # Tu correo de Outlook
    password = "tucontraseña"            # Tu contraseña de Outlook

    validador.enviar_alertas_por_correo(destinatario, remitente, password)