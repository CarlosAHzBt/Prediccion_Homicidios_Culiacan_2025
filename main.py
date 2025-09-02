# main.py
import subprocess
import sys
from pathlib import Path

def run_script(script_name):
    """Ejecuta un script de Python y maneja los errores."""
    script_path = Path(__file__).parent / 'utils' / script_name
    try:
        print(f"--- Ejecutando {script_name} ---")
        result = subprocess.run([sys.executable, str(script_path)], check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errores:", result.stderr)
        print(f"--- {script_name} finalizado ---")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {script_name}:")
        print(e.stdout)
        print(e.stderr)
        return False
    except FileNotFoundError:
        print(f"Error: No se encontró el script {script_path}.")
        return False

def main():
    """
    Orquesta la ejecución de todos los scripts para actualizar los datos.
    """
    print("Iniciando pipeline de actualización de datos...")
    
    # Lista de scripts a ejecutar en orden
    scripts = [
        'get_homicidios.py',
        'get_robos.py',
        'get_clima.py',
        'get_dolar.py',
        'get_dias_pago.py',
        'merge_data.py'
    ]
    
    for script in scripts:
        if not run_script(script):
            print(f"El pipeline se detuvo debido a un error en {script}.")
            break
    else:
        print("Pipeline de actualización completado exitosamente.")

if __name__ == "__main__":
    main()
