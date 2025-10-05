"""
Script de demostración del sistema de análisis de emociones en tweets
Ejecuta el pipeline completo con datos sintéticos
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("DEMOSTRACIÓN DEL SISTEMA DE ANÁLISIS DE EMOCIONES EN TWEETS")
print("=" * 80)
print()

# Configuración
DIAS_PRUEBA = 30  # Generar 30 días de datos de prueba
TWEETS_POR_DIA = 50  # 50 tweets por día
CARPETA_SALIDA = "../../data_tweets_culiacan"

print(f"Configuración:")
print(f"  - Días de prueba: {DIAS_PRUEBA}")
print(f"  - Tweets por día: {TWEETS_POR_DIA}")
print(f"  - Total tweets: {DIAS_PRUEBA * TWEETS_POR_DIA}")
print()

# Paso 1: Generar datos sintéticos
print("=" * 80)
print("PASO 1: GENERANDO DATOS SINTÉTICOS")
print("=" * 80)

# Templates de tweets por emoción
templates_por_emocion = {
    'alegria': [
        "¡Qué bonito día en Culiacán! El sol brillando hermoso 🌞",
        "Feliz de estar en Culiacán, la ciudad más bella de Sinaloa ❤️",
        "Excelente ambiente en Culiacán hoy, todo tranquilo 😊",
        "Me encanta vivir en Culiacán, gran ciudad 🏙️✨",
        "Qué orgullo ser de Culiacán Sinaloa 💪❤️",
    ],
    'tristeza': [
        "Otro día difícil en Culiacán, extraño la paz 😢",
        "Me duele ver lo que pasa en Culiacán últimamente 💔",
        "Qué tristeza la situación de Culiacán 😞",
        "Culiacán ya no es como antes, qué nostalgia",
        "Días oscuros para Culiacán Sinaloa 🖤",
    ],
    'ira': [
        "¡Ya basta! Culiacán merece mejor 😡",
        "Estoy harto de la inseguridad en Culiacán!",
        "Qué coraje la situación en Culiacán Sinaloa 😤",
        "Me da rabia lo que están haciendo con Culiacán",
        "No puede ser posible lo que pasa en Culiacán, ¡ya!",
    ],
    'miedo': [
        "Preocupado por la situación en Culiacán 😰",
        "Tengo miedo de salir en Culiacán últimamente",
        "¿Alguien más nervioso por Culiacán? 😨",
        "Situación tensa en Culiacán Sinaloa, cuidado",
        "Me da miedo pensar en el futuro de Culiacán 😔",
    ],
    'sorpresa': [
        "¡No puedo creer lo que vi en Culiacán! 😲",
        "¿En serio pasó eso en Culiacán? ¡WOW!",
        "Impresionante lo de Culiacán Sinaloa 😮",
        "¡Qué! ¿Eso en Culiacán? No lo esperaba",
        "Sorprendido por las noticias de Culiacán 🤯",
    ]
}

# Generar tweets
tweets_generados = []
fecha_inicio = datetime.now() - timedelta(days=DIAS_PRUEBA)

print(f"Generando {TWEETS_POR_DIA} tweets por día durante {DIAS_PRUEBA} días...")
print()

for dia in range(DIAS_PRUEBA):
    fecha = fecha_inicio + timedelta(days=dia)
    fecha_str = fecha.strftime("%Y-%m-%d")
    
    # Distribución realista de emociones (no uniforme)
    distribucion = {
        'alegria': 0.25,
        'tristeza': 0.20,
        'ira': 0.15,
        'miedo': 0.25,
        'sorpresa': 0.15
    }
    
    for i in range(TWEETS_POR_DIA):
        # Seleccionar emoción según distribución
        emocion = np.random.choice(
            list(distribucion.keys()),
            p=list(distribucion.values())
        )
        
        # Seleccionar template aleatorio
        texto = np.random.choice(templates_por_emocion[emocion])
        
        # Agregar variación
        variaciones = [
            texto,
            texto + " #Culiacán",
            texto + " #CuliacánSinaloa",
            f"{texto} 🙏",
        ]
        texto_final = np.random.choice(variaciones)
        
        tweets_generados.append({
            'fecha': fecha_str,
            'texto': texto_final,
            'emocion_real': emocion  # Para validación
        })
    
    if (dia + 1) % 10 == 0:
        print(f"  ✓ Generados {(dia + 1) * TWEETS_POR_DIA} tweets ({dia + 1}/{DIAS_PRUEBA} días)")

df_tweets = pd.DataFrame(tweets_generados)
print(f"\n✓ Total generados: {len(df_tweets)} tweets")
print(f"  Distribución de emociones:")
for emocion, count in df_tweets['emocion_real'].value_counts().items():
    porcentaje = (count / len(df_tweets)) * 100
    print(f"    - {emocion.capitalize()}: {count} ({porcentaje:.1f}%)")
print()

# Paso 2: Cargar el analizador
print("=" * 80)
print("PASO 2: CARGANDO MODELO DE ANÁLISIS DE EMOCIONES")
print("=" * 80)

try:
    from tweets_sentiments_test import TweetsEmotionAnalyzer
    
    print("Inicializando TweetsEmotionAnalyzer...")
    analizador = TweetsEmotionAnalyzer()
    print("✓ Analizador cargado correctamente")
    print()
    
except Exception as e:
    print(f"✗ Error al cargar el analizador: {e}")
    print()
    print("NOTA: El modelo pysentimiento se descargará automáticamente en la primera ejecución")
    print("      Esto puede tomar varios minutos dependiendo de tu conexión")
    print()
    sys.exit(1)

# Paso 3: Clasificar emociones
print("=" * 80)
print("PASO 3: CLASIFICANDO EMOCIONES CON MODELO PYSENTIMIENTO")
print("=" * 80)

print("Aplicando modelo a cada tweet...")
print("(Esto puede tardar unos minutos para el primer análisis)")
print()

try:
    # Clasificar en batches para mostrar progreso
    batch_size = 100
    total_batches = (len(df_tweets) + batch_size - 1) // batch_size
    
    emociones_predichas = []
    scores = []
    
    for i in range(0, len(df_tweets), batch_size):
        batch = df_tweets.iloc[i:i+batch_size]
        batch_num = i // batch_size + 1
        
        for _, row in batch.iterrows():
            resultado = analizador.clasificar_emocion(row['texto'])
            emociones_predichas.append(resultado['emocion'])
            scores.append(resultado['score'])
        
        print(f"  ✓ Procesado batch {batch_num}/{total_batches} ({len(emociones_predichas)}/{len(df_tweets)} tweets)")
    
    df_tweets['emocion_predicha'] = emociones_predichas
    df_tweets['score'] = scores
    
    print()
    print(f"✓ Clasificación completada: {len(df_tweets)} tweets analizados")
    print()
    
except Exception as e:
    print(f"✗ Error durante la clasificación: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Paso 4: Validar precisión
print("=" * 80)
print("PASO 4: VALIDANDO PRECISIÓN DEL MODELO")
print("=" * 80)

# Calcular accuracy
coincidencias = (df_tweets['emocion_real'] == df_tweets['emocion_predicha']).sum()
accuracy = (coincidencias / len(df_tweets)) * 100

print(f"Precisión global: {accuracy:.1f}% ({coincidencias}/{len(df_tweets)} correctos)")
print()

# Matriz de confusión simplificada
print("Comparación Emoción Real vs Predicha:")
print("-" * 60)
for emocion in ['alegria', 'tristeza', 'ira', 'miedo', 'sorpresa']:
    subset = df_tweets[df_tweets['emocion_real'] == emocion]
    if len(subset) > 0:
        correctos = (subset['emocion_predicha'] == emocion).sum()
        precision_emocion = (correctos / len(subset)) * 100
        print(f"  {emocion.capitalize():12} - {correctos:3}/{len(subset):3} correctos ({precision_emocion:5.1f}%)")
print()

# Paso 5: Agregación por día
print("=" * 80)
print("PASO 5: AGREGANDO DATOS POR DÍA")
print("=" * 80)

print("Calculando estadísticas diarias...")

# Preparar DataFrame para agregación
df_analisis = df_tweets[['fecha', 'texto', 'emocion_predicha', 'score']].copy()
df_analisis.columns = ['fecha', 'texto', 'emocion', 'score']

# Agregar por día
df_diario = analizador.agregar_por_dia(df_analisis)

print(f"✓ Datos agregados: {len(df_diario)} días")
print()
print("Primeros 5 días:")
print(df_diario.head().to_string(index=False))
print()
print("Últimos 5 días:")
print(df_diario.tail().to_string(index=False))
print()

# Paso 6: Guardar resultados
print("=" * 80)
print("PASO 6: GUARDANDO RESULTADOS")
print("=" * 80)

# Crear carpetas si no existen
os.makedirs(f"{CARPETA_SALIDA}/procesado", exist_ok=True)
os.makedirs(f"{CARPETA_SALIDA}/resultados", exist_ok=True)
os.makedirs(f"{CARPETA_SALIDA}/visualizaciones", exist_ok=True)

# Guardar CSVs
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

archivo_tweets = f"{CARPETA_SALIDA}/procesado/tweets_clasificados_DEMO_{timestamp}.csv"
archivo_diario = f"{CARPETA_SALIDA}/resultados/emociones_diarias_DEMO_{timestamp}.csv"

df_tweets.to_csv(archivo_tweets, index=False, encoding='utf-8-sig')
df_diario.to_csv(archivo_diario, index=False, encoding='utf-8-sig')

print(f"✓ Tweets clasificados guardados en:")
print(f"  {archivo_tweets}")
print()
print(f"✓ Resumen diario guardado en:")
print(f"  {archivo_diario}")
print()

# Paso 7: Generar visualizaciones
print("=" * 80)
print("PASO 7: GENERANDO VISUALIZACIONES")
print("=" * 80)

try:
    from visualizador_emociones import VisualizadorEmociones
    
    carpeta_viz = f"{CARPETA_SALIDA}/visualizaciones"
    
    print("Inicializando visualizador...")
    viz = VisualizadorEmociones(carpeta_viz)
    
    visualizaciones = [
        ("Serie Temporal de Porcentajes", lambda: viz.serie_temporal_porcentajes(df_diario)),
        ("Calendario de Emociones", lambda: viz.calendario_emociones(df_diario)),
        ("Distribución Anual", lambda: viz.distribucion_anual(df_diario)),
        ("Intensidad por Emoción", lambda: viz.intensidad_por_emocion(df_diario)),
        ("Días Más Intensos", lambda: viz.dias_mas_intensos(df_diario)),
        ("Evolución Mensual", lambda: viz.evolucion_mensual(df_diario)),
        ("Dashboard Completo", lambda: viz.dashboard_completo(df_diario)),
    ]
    
    for i, (nombre, func) in enumerate(visualizaciones, 1):
        print(f"  [{i}/7] Generando {nombre}...", end=" ")
        try:
            func()
            print("✓")
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print()
    print(f"✓ Visualizaciones guardadas en: {carpeta_viz}")
    print()
    
except Exception as e:
    print(f"✗ Error al generar visualizaciones: {e}")
    import traceback
    traceback.print_exc()
    print()

# Resumen final
print("=" * 80)
print("RESUMEN DE LA DEMOSTRACIÓN")
print("=" * 80)
print()
print(f"✓ Sistema de análisis de emociones funcionando correctamente")
print()
print(f"DATOS PROCESADOS:")
print(f"  - {len(df_tweets)} tweets clasificados")
print(f"  - {DIAS_PRUEBA} días analizados")
print(f"  - Precisión del modelo: {accuracy:.1f}%")
print(f"  - Score promedio: {df_tweets['score'].mean():.3f}")
print()
print(f"DISTRIBUCIÓN FINAL DE EMOCIONES:")
for emocion in ['alegria', 'tristeza', 'ira', 'miedo', 'sorpresa']:
    # Contar directamente del DataFrame de tweets clasificados
    count = (df_tweets['emocion_predicha'] == emocion).sum()
    pct = (count / len(df_tweets)) * 100
    print(f"  - {emocion.capitalize():12}: {pct:5.1f}%")
print()
print(f"ARCHIVOS GENERADOS:")
print(f"  - Tweets clasificados: {archivo_tweets}")
print(f"  - Resumen diario: {archivo_diario}")
if 'carpeta_viz' in locals():
    print(f"  - Visualizaciones: {carpeta_viz}/")
print()
print("=" * 80)
print("¡DEMOSTRACIÓN COMPLETADA CON ÉXITO!")
print("=" * 80)
print()
print("NOTA: Estos son datos sintéticos de demostración.")
print("Para análisis real, necesitas:")
print("  1. API de Twitter/X (recomendado para investigación académica)")
print("  2. Scraping de noticias locales (Ríodoce, Noroeste)")
print("  3. Otras fuentes de datos sobre Culiacán")
print()
print("¿Quieres que te ayude a configurar alguna de estas opciones?")
print()
