# utils/merge_data.py
import pandas as pd
from pathlib import Path
import datetime as dt
import numpy as np

def merge_data():
    """
    Fusiona los datasets de homicidios, clima y dólar en un único archivo.
    """
    print("Iniciando la fusión de datos...")
    
    # --- Cargar Datasets ---
    data_dir = Path(__file__).parent.parent / 'datos'
    
    try:
        homicidios_df = pd.read_csv(data_dir / 'homicidios.csv', parse_dates=['date'])
        robos_df = pd.read_csv(data_dir / 'robos.csv', parse_dates=['date'])
        clima_df = pd.read_csv(data_dir / 'clima.csv', parse_dates=['date'])
        # Algunos archivos de dólar pueden contener una fila fantasma con el símbolo.
        dolar_df = pd.read_csv(data_dir / 'dolar.csv')
        # Limpiar posibles filas inválidas y tipar correctamente
        if 'date' in dolar_df.columns:
            dolar_df['date'] = pd.to_datetime(dolar_df['date'], errors='coerce')
        if 'precio_dolar' in dolar_df.columns:
            dolar_df['precio_dolar'] = pd.to_numeric(dolar_df['precio_dolar'], errors='coerce')
        dolar_df = dolar_df.dropna(subset=['date', 'precio_dolar']).reset_index(drop=True)
        calendario_df = pd.read_csv(data_dir / 'calendario.csv', parse_dates=['date'])
    except FileNotFoundError as e:
        print(f"Error: No se encontró el archivo {e.filename}. Ejecuta los scripts de obtención de datos primero.")
        return

    # --- Fusionar Datos ---
    print("Fusionando datasets...")
    
    # Crear un DataFrame base con todas las fechas
    start_date = homicidios_df['date'].min()
    end_date = dt.datetime.now().date()
    
    # Asegurarse de que end_date no sea NaT
    if pd.isna(start_date):
        print("Error: La fecha de inicio en homicidios.csv es inválida.")
        return
        
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    final_df = pd.DataFrame(date_range, columns=['date'])

    # Fusionar homicidios
    final_df = pd.merge(final_df, homicidios_df, on='date', how='left')
    final_df['homicidios'].fillna(0, inplace=True) # Asumir 0 homicidios en días sin datos

    # Fusionar robos
    final_df = pd.merge(final_df, robos_df, on='date', how='left')
    final_df['robos'].fillna(0, inplace=True) # Asumir 0 robos en días sin datos

    # Fusionar clima
    final_df = pd.merge(final_df, clima_df, on='date', how='left')

    # Fusionar dólar
    final_df = pd.merge(final_df, dolar_df, on='date', how='left')
    
    # Fusionar datos de calendario
    final_df = pd.merge(final_df, calendario_df, on='date', how='left')
    
    # Interpolar valores faltantes para clima y dólar
    # Asegurar numéricos antes de interpolar
    for col in ['tavg', 'tmin', 'tmax', 'prcp', 'wspd', 'pres', 'precio_dolar']:
        if col in final_df.columns:
            final_df[col] = pd.to_numeric(final_df[col], errors='coerce')
    final_df[['tavg', 'tmin', 'tmax', 'prcp', 'wspd', 'pres', 'precio_dolar']] = \
        final_df[['tavg', 'tmin', 'tmax', 'prcp', 'wspd', 'pres', 'precio_dolar']].interpolate(method='linear')
    
    # Rellenar hacia adelante y hacia atrás por si quedan nulos en los extremos
    final_df.fillna(method='ffill', inplace=True)
    final_df.fillna(method='bfill', inplace=True)

    # --- Feature Engineering (Opcional, pero recomendado) ---
    print("Creando características adicionales...")
    final_df['dia_semana'] = final_df['date'].dt.day_name()
    final_df['dia_semana_num'] = final_df['date'].dt.weekday
    final_df['mes'] = final_df['date'].dt.month
    final_df['año'] = final_df['date'].dt.year
    final_df['semana'] = final_df['date'].dt.isocalendar().week.astype(int)
    final_df['dia_del_año'] = final_df['date'].dt.dayofyear
    final_df['quincena'] = np.where(final_df['date'].dt.day <= 15, 1, 2)
    # Señales sencillas útiles para modelos de conteo
    final_df['es_fin_semana'] = final_df['dia_semana_num'].isin([5, 6]).astype(int)
    final_df['inicio_mes'] = (final_df['date'].dt.day == 1).astype(int)
    # Último día del mes
    final_df['fin_mes'] = (final_df['date'] == (final_df['date'] + pd.offsets.MonthEnd(0))).astype(int)
    # Lluvia
    final_df['lluvia'] = (final_df['prcp'] > 0).astype(int)
    final_df['lluvia_fuerte'] = (final_df['prcp'] >= 10).astype(int)
    # Días calurosos/fríos relativos (percentiles globales simples)
    if 'tmax' in final_df.columns and 'tmin' in final_df.columns:
        tmax_p90 = final_df['tmax'].quantile(0.90)
        tmin_p10 = final_df['tmin'].quantile(0.10)
        final_df['dia_muy_caluroso'] = (final_df['tmax'] >= tmax_p90).astype(int)
        final_df['dia_muy_fresco'] = (final_df['tmin'] <= tmin_p10).astype(int)

    # --- Guardar Dataset Final ---
    output_path = data_dir.parent / 'Dataset_homicidios_Actualizado.csv'
    final_df.to_csv(output_path, index=False)
    
    print("Fusión completada.")
    print(f"Dataset final guardado en: {output_path}")
    print(f"Total de registros: {len(final_df)}")
    print(f"Rango de fechas: {final_df['date'].min().strftime('%Y-%m-%d')} a {final_df['date'].max().strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    merge_data()
