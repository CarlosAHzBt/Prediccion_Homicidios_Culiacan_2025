"""Script de debug para visualizaciones"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import sys
import traceback

# Ruta objetivo (misma que usa el visualizador)
dir_salida = Path("../../data_tweets_culiacan/visualizaciones")

print(f"📁 Ruta objetivo (relativa): {dir_salida}")
print(f"📁 Ruta absoluta: {dir_salida.resolve()}")
print(f"📁 Existe: {dir_salida.exists()}")
print(f"📁 Es directorio: {dir_salida.is_dir() if dir_salida.exists() else 'N/A'}")
print()

# Intentar crear el directorio
try:
    dir_salida.mkdir(parents=True, exist_ok=True)
    print("✅ Directorio creado/verificado")
except Exception as e:
    print(f"❌ Error creando directorio: {e}")
    traceback.print_exc()
print()

# Intentar crear un gráfico simple
try:
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])
    ax.set_title('Test de guardado')
    
    archivo = "test_debug.png"
    ruta = dir_salida / archivo
    
    print(f"💾 Intentando guardar en: {ruta}")
    print(f"💾 Ruta absoluta: {ruta.resolve()}")
    
    plt.savefig(ruta, dpi=300, bbox_inches='tight')
    
    # Verificar que se guardó
    if ruta.exists():
        size = ruta.stat().st_size
        print(f"✅ Archivo guardado exitosamente!")
        print(f"   Tamaño: {size:,} bytes")
    else:
        print(f"❌ Archivo NO se guardó (no existe después de savefig)")
        
except Exception as e:
    print(f"❌ Error guardando: {e}")
    traceback.print_exc()
