
# Ejemplo de uso del modelo entrenado
import joblib
import pandas as pd
import numpy as np

# Cargar modelo y escalador
model = joblib.load('../modelos/homicidios_predictor_20250901_204245.joblib')
scaler = joblib.load('../modelos/scaler_20250901_204245.joblib')

# Las características deben estar en este orden:
feature_names = ['homicidios_ma7', 'homicidios_ma30', 'robos', 'tavg', 'tmin', 'tmax', 'prcp', 'wspd', 'pres', 'precio_dolar', 'año', 'mes', 'dia', 'dia_semana_num', 'es_fin_semana', 'quincena', 'dias_desde_pago', 'dia_del_año', 'dia_año', 'semana_año', 'mes_sin', 'mes_cos', 'dia_semana_sin', 'dia_semana_cos', 'dia_año_sin', 'dia_año_cos', 'es_lunes', 'es_viernes', 'inicio_mes', 'fin_mes', 'homicidios_lag_1', 'homicidios_lag_2', 'homicidios_lag_3', 'homicidios_lag_7', 'homicidios_lag_14', 'homicidios_lag_30', 'homicidios_rolling_mean_3', 'homicidios_rolling_std_3', 'homicidios_rolling_max_3', 'homicidios_rolling_min_3', 'homicidios_rolling_mean_7', 'homicidios_rolling_std_7', 'homicidios_rolling_max_7', 'homicidios_rolling_min_7', 'homicidios_rolling_mean_14', 'homicidios_rolling_std_14', 'homicidios_rolling_max_14', 'homicidios_rolling_min_14', 'homicidios_rolling_mean_30', 'homicidios_rolling_std_30', 'homicidios_rolling_max_30', 'homicidios_rolling_min_30', 'homicidios_diff_1', 'homicidios_diff_7', 'homicidios_expanding_mean', 'homicidios_expanding_std', 'homicidios_volatility_7', 'homicidios_volatility_14', 'homicidios_volatility_30']

# Ejemplo de predicción (reemplazar con datos reales)
# X_new = ...  # DataFrame con las características
# X_new_scaled = scaler.transform(X_new[feature_names])
# prediction = model.predict(X_new_scaled)

print("Modelo cargado exitosamente")
print(f"Tipo: {type(model).__name__}")
print(f"Características: {len(feature_names)}")
