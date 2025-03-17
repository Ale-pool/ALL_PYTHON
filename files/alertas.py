# from orquestador.steps import Step
import pandas as pd

class Alertas():
    def ejecutar(self):
        print("Ejecutando alertas")
        # Leer el archivo de alertas
        alertas = pd.read_csv("alertas.csv")
        print(alertas)
        print("Alertas ejecutadas")
        return alertas
    

    # despues se tiene la primer alerta en relación a identificacion
    # se tiene la segunda alerta en relacion al estado si es diferente a "activo"
    # en relacion a fecha de renovacion, por ejemplo si la fecha de renovacion es menor a la fecha actual alerta en relacion a la fecha de renovacion
    # alerta en relacion a la fecha de actualizacion, si la fecha de actualizacion es menor a la fecha actual