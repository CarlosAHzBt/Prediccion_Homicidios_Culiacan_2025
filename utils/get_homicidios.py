# utils/get_homicidios.py
import pandas as pd
import re
import datetime as dt
from pathlib import Path
import time
import sys

# Para web scraping
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# --- Constantes y Configuración ---

# Regex para extraer datos de Flourish
REGEX_DL = re.compile(r",\s*(\d{2}-[a-z]{3}-\d{2}):\s*(\d+)", re.I)
MES = {"ene":"jan","feb":"feb","mar":"mar","abr":"apr","may":"may","jun":"jun",
       "jul":"jul","ago":"aug","sep":"sep","oct":"oct","nov":"nov","dic":"dec"}

HO_URL = "https://flo.uri.sh/visualisation/19405940/embed?auto=1"
RB_URL = "https://flo.uri.sh/visualisation/21616394/embed" # URL para robos, por si se necesita

# --- Funciones Auxiliares ---

def date_es(txt: str) -> dt.date:
    """Convierte fecha en español a formato date"""
    try:
        d, m, y = txt.split("-")
        return dt.datetime.strptime(f"{d}-{MES[m.lower()]}-{y}", "%d-%b-%y").date()
    except (ValueError, KeyError) as e:
        print(f"Error al procesar fecha: {txt}. Error: {e}", file=sys.stderr)
        return None

def get_driver():
    """Configura y devuelve un driver de Chrome para scraping"""
    opt = Options()
    opt.add_argument("--headless=new")
    opt.add_argument("--disable-gpu")
    opt.add_argument("--no-sandbox")
    opt.add_argument("--disable-dev-shm-usage")
    opt.add_argument("--disable-logging")
    opt.add_argument("--log-level=3")
    
    try:
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=opt)
    except Exception as e:
        print(f"Error al configurar el driver de Chrome: {e}", file=sys.stderr)
        return None

# --- Función Principal de Scraping ---

def scrape_flourish(url: str, col: str, max_retries: int = 3) -> pd.DataFrame:
    """
    Realiza scraping de datos de una visualización de Flourish.
    
    Args:
        url (str): La URL de la visualización de Flourish.
        col (str): El nombre de la columna para los datos extraídos.
        max_retries (int): Número máximo de reintentos.

    Returns:
        pd.DataFrame: Un DataFrame con 'date' y la columna especificada.
    """
    for attempt in range(max_retries):
        driver = None
        try:
            print(f"Intento {attempt + 1}/{max_retries} para obtener datos de {col}...")
            driver = get_driver()
            if not driver:
                print("Driver no disponible, saltando intento.", file=sys.stderr)
                time.sleep(5)
                continue

            driver.get(url)
            
            # Espera a que los elementos de datos carguen usando un selector más específico
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "path.data-point[aria-label]"))
            )
            
            # Extraer datos directamente de los elementos
            registros = []
            elements = driver.find_elements(By.CSS_SELECTOR, "path.data-point[aria-label]")
            
            for el in elements:
                match = REGEX_DL.search(el.get_attribute("aria-label"))
                if match:
                    fecha_str, valor = match.groups()
                    registros.append({"fecha_str": fecha_str, col: int(valor)})

            if not registros:
                print(f"No se encontraron datos en el intento {attempt + 1}", file=sys.stderr)
                time.sleep(5)
                continue

            # Procesar y limpiar datos
            df = pd.DataFrame(registros)
            df["date"] = df["fecha_str"].apply(date_es)
            df = df.dropna(subset=['date']) # Eliminar fechas que no se pudieron procesar
            df[col] = pd.to_numeric(df[col])
            df = df.groupby("date")[col].sum().reset_index()
            df = df.sort_values("date", ascending=True).reset_index(drop=True)
            
            print(f"Datos de {col} obtenidos exitosamente.")
            return df[["date", col]]

        except Exception as e:
            print(f"Error en el intento {attempt + 1} para {col}: {e}", file=sys.stderr)
            time.sleep(5)
        finally:
            if driver:
                driver.quit()
    
    print(f"No se pudieron obtener los datos de {col} después de {max_retries} intentos.", file=sys.stderr)
    return pd.DataFrame()

# --- Bloque de Ejecución ---

def main():
    """
    Función principal para ejecutar el script de forma independiente.
    """
    print("Iniciando la actualización de datos de homicidios...")
    
    # Definir rutas de salida
    output_dir = Path(__file__).parent.parent / 'datos'
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / 'homicidios.csv'

    # Obtener datos
    homicidios_df = scrape_flourish(HO_URL, "homicidios")

    # Calcular promedio móvil de homicidios
    if not homicidios_df.empty:
        print("Calculando promedio móvil de homicidios...")
        # Promedio móvil de 7 días
        homicidios_df['homicidios_ma7'] = homicidios_df['homicidios'].rolling(window=7, center=True).mean()
        # Promedio móvil de 30 días
        homicidios_df['homicidios_ma30'] = homicidios_df['homicidios'].rolling(window=30, center=True).mean()

    # Guardar datos
    if not homicidios_df.empty:
        homicidios_df.to_csv(output_path, index=False)
        print(f"Datos de homicidios guardados en: {output_path}")
    else:
        print("No se generó el archivo CSV de homicidios porque no se obtuvieron datos.")

if __name__ == "__main__":
    main()
