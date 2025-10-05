"""
Test simple de generación de gráfico
"""
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path

print("Test de generación de gráfico...")
print()

# Crear datos de prueba
datos = pd.DataFrame({
    'x': np.arange(10),
    'y': np.random.rand(10)
})

# Crear gráfico
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(datos['x'], datos['y'])
ax.set_title("Gráfico de Prueba")
ax.set_xlabel("X")
ax.set_ylabel("Y")

# Guardar
output_dir = Path("data_tweets_culiacan/visualizaciones")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "test_grafico.png"
print(f"Intentando guardar en: {output_file.absolute()}")

try:
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"✅ Guardado exitosamente!")
    print(f"  Archivo existe: {output_file.exists()}")
    if output_file.exists():
        print(f"  Tamaño: {output_file.stat().st_size / 1024:.1f} KB")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    plt.close()

print()
print("Listando archivos en el directorio:")
for f in output_dir.glob("*"):
    print(f"  - {f.name} ({f.stat().st_size / 1024:.1f} KB)")
