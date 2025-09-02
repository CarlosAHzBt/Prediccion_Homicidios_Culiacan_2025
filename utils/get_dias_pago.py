# utils/get_dias_pago.py
import pandas as pd
import datetime as dt
from pathlib import Path
import numpy as np

# --- Funciones para días festivos mexicanos ---

def es_año_bisiesto(año):
    """Verifica si un año es bisiesto"""
    return año % 4 == 0 and (año % 100 != 0 or año % 400 == 0)

def domingo_pascua(año):
    """Calcula el domingo de Pascua para un año dado"""
    # Algoritmo de Butcher
    a = año % 19
    b = año // 100
    c = año % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    n = (h + l - 7 * m + 114) // 31
    p = (h + l - 7 * m + 114) % 31
    return dt.date(año, n, p + 1)

def obtener_festivos_mexico(año):
    """
    Obtiene la lista de días festivos oficiales en México para un año dado.
    """
    festivos = []
    
    # Año Nuevo
    festivos.append(dt.date(año, 1, 1))
    
    # Día de la Constitución (primer lunes de febrero)
    primer_feb = dt.date(año, 2, 1)
    dias_hasta_lunes = (7 - primer_feb.weekday()) % 7
    if primer_feb.weekday() == 0:  # Si es lunes
        dia_constitucion = primer_feb
    else:
        dia_constitucion = primer_feb + dt.timedelta(days=dias_hasta_lunes)
    festivos.append(dia_constitucion)
    
    # Natalicio de Benito Juárez (tercer lunes de marzo)
    primer_marzo = dt.date(año, 3, 1)
    dias_hasta_lunes = (7 - primer_marzo.weekday()) % 7
    if primer_marzo.weekday() == 0:
        primer_lunes_marzo = primer_marzo
    else:
        primer_lunes_marzo = primer_marzo + dt.timedelta(days=dias_hasta_lunes)
    benito_juarez = primer_lunes_marzo + dt.timedelta(days=14)  # Tercer lunes
    festivos.append(benito_juarez)
    
    # Jueves Santo y Viernes Santo (dependen de Pascua)
    pascua = domingo_pascua(año)
    jueves_santo = pascua - dt.timedelta(days=3)
    viernes_santo = pascua - dt.timedelta(days=2)
    festivos.extend([jueves_santo, viernes_santo])
    
    # Día del Trabajo
    festivos.append(dt.date(año, 5, 1))
    
    # Día de la Independencia
    festivos.append(dt.date(año, 9, 16))
    
    # Día de Muertos
    festivos.append(dt.date(año, 11, 2))
    
    # Revolución Mexicana (tercer lunes de noviembre)
    primer_nov = dt.date(año, 11, 1)
    dias_hasta_lunes = (7 - primer_nov.weekday()) % 7
    if primer_nov.weekday() == 0:
        primer_lunes_nov = primer_nov
    else:
        primer_lunes_nov = primer_nov + dt.timedelta(days=dias_hasta_lunes)
    revolucion = primer_lunes_nov + dt.timedelta(days=14)  # Tercer lunes
    festivos.append(revolucion)
    
    # Navidad
    festivos.append(dt.date(año, 12, 25))
    
    return sorted(festivos)

def es_dia_pago(fecha):
    """
    Determina si una fecha es día de pago típico.
    Generalmente: días 15 y último día del mes, días 1 (salarios), viernes (pagos semanales)
    """
    dia = fecha.day
    
    # Día 15 del mes
    if dia == 15:
        return True
    
    # Último día del mes
    if fecha == fecha.replace(day=1) + pd.DateOffset(months=1) - pd.DateOffset(days=1):
        return True
    
    # Primer día del mes
    if dia == 1:
        return True
    
    # Viernes (pago semanal común)
    if fecha.weekday() == 4:  # 4 = viernes
        return True
    
    return False

def generar_datos_calendario(start_date, end_date):
    """
    Genera un DataFrame con información de calendario para un rango de fechas.
    """
    print("Generando datos de calendario y días especiales...")
    
    # Crear rango de fechas
    date_range = pd.date_range(start=start_date, end=end_date)
    
    # Crear DataFrame base
    df = pd.DataFrame({'date': date_range})
    
    # Información básica de fecha
    df['año'] = df['date'].dt.year
    df['mes'] = df['date'].dt.month
    df['dia'] = df['date'].dt.day
    df['dia_semana'] = df['date'].dt.day_name()
    df['dia_semana_num'] = df['date'].dt.weekday  # 0=lunes, 6=domingo
    df['es_fin_semana'] = df['dia_semana_num'].isin([5, 6])  # sábado y domingo
    
    # Días de pago
    df['es_dia_pago'] = df['date'].apply(es_dia_pago)
    
    # Días festivos
    años_unicos = df['año'].unique()
    todos_festivos = []
    for año in años_unicos:
        festivos_año = obtener_festivos_mexico(año)
        todos_festivos.extend(festivos_año)
    
    df['es_festivo'] = df['date'].dt.date.isin(todos_festivos)
    
    # Día hábil (no es fin de semana ni festivo)
    df['es_dia_habil'] = ~(df['es_fin_semana'] | df['es_festivo'])
    
    # Días después de festivos (pueden tener patrones especiales)
    df['despues_festivo'] = df['es_festivo'].shift(1, fill_value=False)
    
    # Días antes de festivos
    df['antes_festivo'] = df['es_festivo'].shift(-1, fill_value=False)
    
    # Período de quincena
    df['quincena'] = np.where(df['dia'] <= 15, 1, 2)
    
    # Días desde último día de pago
    df['dias_desde_pago'] = 0
    for i in range(1, len(df)):
        if df.loc[i, 'es_dia_pago']:
            df.loc[i, 'dias_desde_pago'] = 0
        else:
            df.loc[i, 'dias_desde_pago'] = df.loc[i-1, 'dias_desde_pago'] + 1
    
    return df

def main():
    """
    Función principal para ejecutar el script de forma independiente.
    """
    print("Iniciando la generación de datos de días de pago y festivos...")
    
    # Definir rutas de salida
    output_dir = Path(__file__).parent.parent / 'datos'
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / 'calendario.csv'
    
    # Rango de fechas: desde una fecha de inicio hasta el día actual
    start_date = dt.date(2024, 7, 1)  # Ajustar según necesidades
    end_date = dt.date.today()
    
    # Generar datos
    calendario_df = generar_datos_calendario(start_date, end_date)
    
    # Guardar datos
    if not calendario_df.empty:
        calendario_df.to_csv(output_path, index=False)
        print(f"Datos de calendario guardados en: {output_path}")
        print(f"Total de días procesados: {len(calendario_df)}")
        print(f"Días de pago: {calendario_df['es_dia_pago'].sum()}")
        print(f"Días festivos: {calendario_df['es_festivo'].sum()}")
        print(f"Días hábiles: {calendario_df['es_dia_habil'].sum()}")
    else:
        print("No se generó el archivo CSV de calendario.")

if __name__ == "__main__":
    main()
