"""
Script para generar el script de recolección con tu configuración personalizada
"""
from tweets_sentiments_test import TweetsEmotionAnalyzer
from datetime import datetime

# Crear analizador
analyzer = TweetsEmotionAnalyzer()

# Mostrar configuración
print("\n" + "=" * 70)
print("CONFIGURACIÓN PERSONALIZADA")
print("=" * 70)
print(f"\n📅 Período: {analyzer.config['fecha_inicio']} → {analyzer.config['fecha_fin']}")
print(f"📝 Palabras clave: {', '.join(analyzer.config['palabras'])}")
print(f"💬 Incluye respuestas: Sí")
print(f"🔄 Excluye retweets: Sí")
print(f"🌍 Idioma: {analyzer.config['idioma']}")

# Calcular estadísticas
inicio = datetime.strptime(analyzer.config['fecha_inicio'], "%Y-%m-%d")
fin = datetime.strptime(analyzer.config['fecha_fin'], "%Y-%m-%d")
dias = (fin - inicio).days + 1

print(f"\n📊 Total de días a recolectar: {dias}")
print(f"⏱️  Tiempo estimado: {dias//60}-{dias//30} horas")

# Generar script
print("\n" + "=" * 70)
print("GENERANDO SCRIPT DE RECOLECCIÓN")
print("=" * 70)

script_path = analyzer.generar_script_recoleccion('recolectar_tweets_culiacan.ps1')

print(f"\n✅ Script generado: {script_path}")
print("\n📋 SIGUIENTES PASOS:")
print("   1. Revisa el script generado:")
print(f"      notepad {script_path}")
print("   2. Ejecuta el script en PowerShell:")
print(f"      .\\{script_path}")
print("\n⚠️  NOTA: La recolección de 395 días puede tomar 6-7 horas.")
print("   Puedes pausar (Ctrl+C) y reanudar sin problemas.\n")
print("=" * 70)
