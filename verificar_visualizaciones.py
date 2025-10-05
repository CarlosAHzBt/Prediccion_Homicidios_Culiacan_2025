"""
Script simple para verificar las visualizaciones
"""
import os
from pathlib import Path

# Buscar archivos PNG
print("=" * 80)
print("BUSCANDO ARCHIVOS PNG EN EL PROYECTO")
print("=" * 80)
print()

raiz = Path(r"C:\Users\carlo\Documents\Codigo\Homicidios_cln_v2")

print(f"Buscando desde: {raiz}")
print()

png_files = list(raiz.rglob("*.png"))

# Filtrar solo los relevantes (no de librerías)
png_relevantes = [f for f in png_files if "data_tweets_culiacan" in str(f) or "visualizaciones" in str(f)]

if png_relevantes:
    print(f"✅ Encontrados {len(png_relevantes)} archivos PNG:")
    for f in png_relevantes:
        print(f"  - {f}")
        print(f"    Tamaño: {f.stat().st_size / 1024:.1f} KB")
        print()
else:
    print("❌ No se encontraron archivos PNG en data_tweets_culiacan o visualizaciones")
    print()
    print("Verificando carpetas creadas:")
    
    carpetas = [
        raiz / "data_tweets_culiacan" / "visualizaciones",
        raiz / "utils" / "scrapping" / "data_tweets_culiacan" / "visualizaciones",
    ]
    
    for carpeta in carpetas:
        print(f"\n  {carpeta}")
        if carpeta.exists():
            print(f"    ✅ Existe")
            archivos = list(carpeta.glob("*"))
            if archivos:
                print(f"    Archivos:")
                for archivo in archivos:
                    print(f"      - {archivo.name}")
            else:
                print(f"    (vacía)")
        else:
            print(f"    ❌ No existe")

print()
print("=" * 80)
