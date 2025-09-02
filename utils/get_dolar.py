# utils/get_dolar.py
import pandas as pd
import yfinance as yf
import datetime as dt
from pathlib import Path
import sys

# --- Función Principal ---

def get_dolar_data(start_date, end_date):
    """
    Descarga los datos del tipo de cambio USD/MXN desde Yahoo Finance.

    Args:
        start_date (dt.date): Fecha de inicio para la descarga de datos.
        end_date (dt.date): Fecha de fin para la descarga de datos.

    Returns:
        pd.DataFrame: Un DataFrame con 'date' y 'precio_dolar'.
    """
    print("Descargando datos del tipo de cambio USD/MXN...")
    try:
        # Descargar datos para el par USD/MXN
        usd_df = yf.download('USDMXN=X', start=start_date, end=end_date + dt.timedelta(days=1))
        
        if usd_df.empty:
            print("No se pudieron descargar los datos del dólar.", file=sys.stderr)
            return pd.DataFrame()

        # Procesar datos
        usd_df = usd_df[['Close']].copy()
        usd_df.rename(columns={'Close': 'precio_dolar'}, inplace=True)
        usd_df.reset_index(inplace=True)
        usd_df.rename(columns={'Date': 'date'}, inplace=True)
        
        # Asegurarse de que la fecha no tenga zona horaria
        usd_df['date'] = usd_df['date'].dt.tz_localize(None)
        
        print("Datos del dólar obtenidos y procesados exitosamente.")
        return usd_df

    except Exception as e:
        print(f"Error al descargar los datos del dólar: {e}", file=sys.stderr)
        return pd.DataFrame()

# --- Bloque de Ejecución ---

def main():
    """
    Función principal para ejecutar el script de forma independiente.
    """
    print("Iniciando la actualización de datos del dólar...")
    
    # Rango de fechas
    start_date = dt.date(2024, 9, 9)
    end_date = dt.date.today()

    # Obtener datos
    dolar_df = get_dolar_data(start_date, end_date)

    # Definir rutas de salida
    output_dir = Path(__file__).parent.parent / 'datos'
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / 'dolar.csv'

    # Guardar datos
    if not dolar_df.empty:
        dolar_df.to_csv(output_path, index=False)
        print(f"Datos del dólar guardados en: {output_path}")
    else:
        print("No se generó el archivo CSV del dólar.")

if __name__ == "__main__":
    main()
