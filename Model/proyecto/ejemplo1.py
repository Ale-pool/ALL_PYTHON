# vamos a instalar las librerias necesarias para el desarrollo de la prueba
# pip install scikit-learn matplotlib

#cargar los datos y entrenar el modelo
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# Datos de ejemplo: transacciones financieras (monto, hora del día)
# Supongamos que las anomalías son transacciones con montos muy altos o en horas inusuales.
X = np.array([[100, 12], [150, 14], [200, 15], [50, 10], [300, 3], [500, 2], [1000, 1]])

# crear modelo y entrenar el modelo
modelo = IsolationForest(n_estimators=100, contamination=0.1) # contamination es la fracción de anomalías esperadas
modelo.fit(X)


# predecir si una transacción es normal (1) o una anomalía (-1) usando el modelo entrenado
predicciones = modelo.predict(X)
print("predicciones: ", predicciones)

# puntuaciones de anomalias ( cuanto más negativo, más anómalo)
puntuaciones_anomalias = modelo.decision_function(X)
print("puntuaciones de anomalias: ", puntuaciones_anomalias)




# visualizar los resultados
plt.scatter(X[:, 0], X[:, 1], c=predicciones, cmap='viridis', edgecolors='k')
plt.xlabel('Monto de la transacción')
plt.ylabel('Hora del día')
plt.title('Detección de anomalías en transacciones financieras')
plt.colorbar(label='Predicción de anomalía (1: normal, -1: anomalía)')
plt.show()
