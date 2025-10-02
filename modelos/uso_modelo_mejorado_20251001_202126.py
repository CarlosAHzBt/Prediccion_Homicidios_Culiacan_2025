# Script de uso del modelo mejorado
# Generado: 20251001_202126

from joblib import load
import pandas as pd
import numpy as np

# Cargar modelo
model = load('modelo_mejorado_RF_improved_20251001_202126.joblib')

# Ejemplo de predicción
# X_new debe tener las mismas 57 features
# X_new = pd.DataFrame(...)  # Con las features correctas
# prediccion = model.predict(X_new)

print("Modelo cargado. Features requeridas: 57")
print("MAE en validación: 2.554")
