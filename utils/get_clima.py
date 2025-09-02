# utils/get_clima.py
import pandas as pd
import numpy as np
import datetime as dt
from pathlib import Path
import time
import requests
import sys

# --- Constantes y Configuración ---

CULIACAN_LAT = 24.840216
CULIACAN_LON = -107.385207

# --- Clase para Manejar APIs del Clima ---

class WeatherAPIManager:
    """
    Maneja la obtención de datos climáticos, usando una API real si está configurada,
    o generando datos realistas como fallback.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "open-weather13.p.rapidapi.com"
        })

    def get_forecast_from_api(self, lat, lon, target_date):
        """Intenta obtener el pronóstico de la API de RapidAPI."""
        if not self.api_key:
            return None

        url = "https://open-weather13.p.rapidapi.com/fivedaysforcast"
        querystring = {"latitude": str(lat), "longitude": str(lon)}
        
        try:
            response = self.session.get(url, params=querystring, timeout=10)
            response.raise_for_status()
            # Aquí se necesitaría lógica para parsear la respuesta de la API
            # y encontrar el día correcto. Por ahora, se asume que no funciona
            # y se pasa al fallback.
            # print(f"Respuesta de la API: {response.json()}") # Para depuración
            return None # Forzamos fallback por ahora
        except requests.exceptions.RequestException as e:
            print(f"Error en la API del clima: {e}", file=sys.stderr)
            return None

    def get_realistic_fallback(self, target_date):
        """Genera datos climáticos realistas para Culiacán."""
        date_obj = dt.datetime.strptime(target_date, '%Y-%m-%d')
        
        clima_culiacan = {
            1: (18.5, 13.0, 24.0), 2: (21.0, 15.0, 27.0), 3: (24.5, 18.0, 31.0),
            4: (27.5, 21.0, 34.0), 5: (30.0, 23.0, 37.0), 6: (32.0, 25.0, 39.0),
            7: (29.0, 24.0, 34.0), 8: (29.0, 24.0, 34.0), 9: (28.5, 23.0, 34.0),
            10: (26.0, 20.0, 32.0), 11: (22.0, 16.0, 28.0), 12: (19.0, 13.0, 25.0)
        }
        
        temp_prom, min_tipica, max_tipica = clima_culiacan.get(date_obj.month, (25.0, 18.0, 32.0))
        
        np.random.seed(date_obj.timetuple().tm_yday)
        temp_avg = temp_prom + np.random.normal(0, 1.0)
        
        rango_tipico = max_tipica - min_tipica
        rango_diario = max(9, min(15, rango_tipico + np.random.normal(0, 0.5)))
        
        temp_max = temp_avg + (rango_diario * 0.55)
        temp_min = temp_avg - (rango_diario * 0.45)
        
        if date_obj.month in [6, 7, 8, 9]: prob_lluvia, lluvia_base = 0.25, 5.0
        elif date_obj.month in [12, 1, 2, 3]: prob_lluvia, lluvia_base = 0.02, 1.0
        else: prob_lluvia, lluvia_base = 0.10, 3.0
        
        prcp = lluvia_base * np.random.exponential(1.5) if np.random.random() < prob_lluvia else 0
        
        wspd = np.random.uniform(3, 12)
        pres = np.random.normal(1012, 5)
        
        return {
            'tavg': round(temp_avg, 1), 'tmin': round(temp_min, 1), 'tmax': round(temp_max, 1),
            'prcp': round(prcp, 1), 'wspd': round(wspd, 1), 'pres': round(pres, 1)
        }

    def get_weather_for_date(self, lat, lon, target_date):
        """Obtiene datos del clima para una fecha, usando API o fallback."""
        api_data = self.get_forecast_from_api(lat, lon, target_date)
        if api_data:
            return api_data
        return self.get_realistic_fallback(target_date)

# --- Bloque de Ejecución ---

def main():
    """
    Genera un archivo CSV con datos climáticos para un rango de fechas.
    """
    print("Iniciando la generación de datos climáticos...")
    
    # Rango de fechas: desde una fecha de inicio hasta el día actual.
    start_date = dt.date(2024, 9, 9)
    end_date = dt.date.today()
    date_range = pd.date_range(start=start_date, end=end_date)

    # API Key (opcional, dejar como None si no se tiene)
    # RAPIDAPI_KEY = "TU_API_KEY_AQUI" 
    RAPIDAPI_KEY = None
    
    weather_manager = WeatherAPIManager(api_key=RAPIDAPI_KEY)
    clima_data = []

    for target_date in date_range:
        fecha_str = target_date.strftime('%Y-%m-%d')
        print(f"Obteniendo clima para: {fecha_str}")
        clima = weather_manager.get_weather_for_date(CULIACAN_LAT, CULIACAN_LON, fecha_str)
        clima['date'] = target_date
        clima_data.append(clima)
        time.sleep(0.1) # Pequeña pausa para no saturar

    clima_df = pd.DataFrame(clima_data)
    
    # Definir rutas de salida
    output_dir = Path(__file__).parent.parent / 'datos'
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / 'clima.csv'

    # Guardar datos
    if not clima_df.empty:
        clima_df.to_csv(output_path, index=False)
        print(f"Datos del clima guardados en: {output_path}")
    else:
        print("No se generó el archivo CSV del clima.")

if __name__ == "__main__":
    main()
