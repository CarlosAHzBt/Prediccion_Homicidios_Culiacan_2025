"""
Ejemplo completo de uso del sistema de análisis de emociones en tweets
Este script muestra todo el flujo de trabajo desde la recolección hasta la visualización
"""

from tweets_sentiments_test import TweetsEmotionAnalyzer, mostrar_resumen_rapido
from visualizador_emociones import crear_visualizaciones
import pandas as pd
from pathlib import Path


def ejemplo_1_generar_script_recoleccion():
    """
    PASO 1: Generar el script de PowerShell para recolectar tweets
    
    Este paso genera un archivo .ps1 que puedes ejecutar en PowerShell
    para descargar todos los tweets del período especificado.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 1: GENERAR SCRIPT DE RECOLECCIÓN")
    print("=" * 70)
    
    # Crear instancia del analizador
    analyzer = TweetsEmotionAnalyzer()
    
    # Generar script de recolección
    script_path = analyzer.generar_script_recoleccion(
        output_file="recolectar_tweets_culiacan.ps1"
    )
    
    print(f"\n✅ Script generado: {script_path}")
    print("\n📝 SIGUIENTE PASO:")
    print("   1. Abre PowerShell")
    print("   2. Navega al directorio del proyecto")
    print("   3. Ejecuta: .\\recolectar_tweets_culiacan.ps1")
    print("\n⚠️  NOTA: La recolección de un año completo puede tomar varias horas.")
    print("   Puedes pausar y reanudar el script sin problemas.\n")


def ejemplo_2_analisis_rapido():
    """
    PASO 2: Análisis de una muestra pequeña (para pruebas)
    
    Este ejemplo muestra cómo analizar tweets de unos pocos días
    sin tener que esperar la recolección completa.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 2: ANÁLISIS RÁPIDO (MUESTRA)")
    print("=" * 70)
    
    # Configuración para solo una semana (prueba)
    config_prueba = {
        'fecha_inicio': '2025-01-01',
        'fecha_fin': '2025-01-07'
    }
    
    analyzer = TweetsEmotionAnalyzer(config_override=config_prueba)
    
    # Generar comandos para una semana
    print("\n📋 Comandos para recolectar una semana de prueba:")
    print("-" * 70)
    for i in range(7):
        from datetime import datetime, timedelta
        fecha = datetime(2025, 1, 1) + timedelta(days=i)
        fecha_str = fecha.strftime("%Y-%m-%d")
        comando = analyzer.generar_comando_snscrape(fecha_str)
        print(f"\n# Día {i+1}:")
        print(comando)
    
    print("\n💡 TIP: Ejecuta estos comandos manualmente en PowerShell para probar")


def ejemplo_3_procesar_tweets_recolectados():
    """
    PASO 3: Procesar tweets ya recolectados
    
    Una vez que hayas recolectado tweets, este paso los procesa,
    clasifica emociones y genera el análisis completo.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 3: PROCESAR TWEETS RECOLECTADOS")
    print("=" * 70)
    
    # Verificar si hay datos
    data_dir = Path("data_tweets_culiacan/raw")
    archivos = list(data_dir.glob("tweets_*.jsonl")) if data_dir.exists() else []
    
    if not archivos:
        print("\n⚠️  No se encontraron tweets recolectados.")
        print("   Primero ejecuta el script de recolección (Ejemplo 1).")
        return
    
    print(f"\n✅ Encontrados {len(archivos)} archivos de tweets")
    print("\n🔄 Iniciando procesamiento completo...")
    print("   (Esto puede tomar varios minutos dependiendo del volumen)\n")
    
    # Crear analizador y ejecutar pipeline completo
    analyzer = TweetsEmotionAnalyzer()
    
    try:
        resultados = analyzer.pipeline_completo(desde_raw=True)
        
        if resultados:
            print("\n" + "=" * 70)
            print("✅ PROCESAMIENTO COMPLETADO")
            print("=" * 70)
            
            # Mostrar resumen
            mostrar_resumen_rapido(resultados['analisis'])
            
            # Información de archivos generados
            print("\n📁 Archivos generados:")
            print(f"   - Tweets clasificados: data_tweets_culiacan/resultados/")
            print(f"   - Resumen diario: data_tweets_culiacan/resultados/")
            print(f"   - Análisis anual: data_tweets_culiacan/resultados/")
            
            return resultados
        
    except Exception as e:
        print(f"\n❌ Error en el procesamiento: {e}")
        print("   Verifica que tengas instaladas las dependencias:")
        print("   pip install pysentimiento pandas numpy tqdm")


def ejemplo_4_generar_visualizaciones():
    """
    PASO 4: Generar visualizaciones
    
    Crea todos los gráficos y visualizaciones del análisis.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 4: GENERAR VISUALIZACIONES")
    print("=" * 70)
    
    # Buscar archivo de resumen diario
    resultados_dir = Path("data_tweets_culiacan/resultados")
    archivos_resumen = list(resultados_dir.glob("resumen_diario_*.csv")) if resultados_dir.exists() else []
    
    if not archivos_resumen:
        print("\n⚠️  No se encontró archivo de resumen diario.")
        print("   Primero procesa los tweets (Ejemplo 3).")
        return
    
    # Usar el archivo más reciente
    archivo_mas_reciente = max(archivos_resumen, key=lambda p: p.stat().st_mtime)
    
    print(f"\n📊 Cargando datos desde: {archivo_mas_reciente.name}")
    
    # Cargar datos
    df_diario = pd.read_csv(archivo_mas_reciente)
    
    print(f"   - Días con datos: {len(df_diario)}")
    print(f"   - Total de tweets: {df_diario['n_total'].sum():,}")
    
    # Generar visualizaciones
    print("\n🎨 Generando visualizaciones...")
    crear_visualizaciones(df_diario)
    
    print("\n📁 Visualizaciones guardadas en: data_tweets_culiacan/visualizaciones/")


def ejemplo_5_analisis_personalizado():
    """
    PASO 5: Análisis personalizado
    
    Ejemplo de cómo hacer análisis adicionales con los datos procesados.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 5: ANÁLISIS PERSONALIZADO")
    print("=" * 70)
    
    # Cargar datos procesados
    resultados_dir = Path("data_tweets_culiacan/resultados")
    archivo_diario = list(resultados_dir.glob("resumen_diario_*.csv"))
    
    if not archivo_diario:
        print("\n⚠️  No hay datos para analizar.")
        return
    
    df = pd.read_csv(archivo_diario[0])
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    print("\n📊 ANÁLISIS PERSONALIZADOS:")
    print("-" * 70)
    
    # 1. Día de la semana más emotivo
    df['dia_semana'] = df['fecha'].dt.day_name()
    dias_semana_es = {
        'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
        'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
    }
    df['dia_semana_es'] = df['dia_semana'].map(dias_semana_es)
    
    print("\n1️⃣  EMOCIONES POR DÍA DE LA SEMANA:")
    for dia in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']:
        df_dia = df[df['dia_semana_es'] == dia]
        if not df_dia.empty:
            emocion_comun = df_dia['ganador_del_dia'].mode()[0]
            print(f"   {dia:10} → {emocion_comun.capitalize()}")
    
    # 2. Mes más emotivo
    df['mes'] = df['fecha'].dt.month
    print("\n2️⃣  EMOCIÓN DOMINANTE POR MES:")
    for mes in range(1, 13):
        df_mes = df[df['mes'] == mes]
        if not df_mes.empty:
            emocion_comun = df_mes['ganador_del_dia'].mode()[0]
            meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                    'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
            print(f"   {meses[mes-1]:3} → {emocion_comun.capitalize()}")
    
    # 3. Racha más larga de una emoción
    print("\n3️⃣  RACHA MÁS LARGA POR EMOCIÓN:")
    df_sorted = df.sort_values('fecha')
    
    for emocion in ['alegria', 'tristeza', 'ira', 'miedo', 'sorpresa']:
        racha_actual = 0
        racha_max = 0
        fecha_inicio_max = None
        fecha_fin_max = None
        fecha_inicio = None
        
        for idx, row in df_sorted.iterrows():
            if row['ganador_del_dia'] == emocion:
                if racha_actual == 0:
                    fecha_inicio = row['fecha']
                racha_actual += 1
                if racha_actual > racha_max:
                    racha_max = racha_actual
                    fecha_inicio_max = fecha_inicio
                    fecha_fin_max = row['fecha']
            else:
                racha_actual = 0
        
        if racha_max > 0:
            print(f"   {emocion.capitalize():10} → {racha_max} días consecutivos")
    
    # 4. Correlación entre volumen y emociones
    print("\n4️⃣  DÍAS CON MÁS TWEETS:")
    top_volumen = df.nlargest(5, 'n_total')[['fecha', 'n_total', 'ganador_del_dia']]
    for _, row in top_volumen.iterrows():
        fecha_str = row['fecha'].strftime('%Y-%m-%d')
        print(f"   {fecha_str} → {row['n_total']:4} tweets ({row['ganador_del_dia'].capitalize()})")


def menu_interactivo():
    """Menú interactivo para ejecutar los diferentes ejemplos"""
    while True:
        print("\n" + "=" * 70)
        print("SISTEMA DE ANÁLISIS DE EMOCIONES EN TWEETS - CULIACÁN")
        print("=" * 70)
        print("\nSelecciona una opción:")
        print("\n  1️⃣  Generar script de recolección de tweets")
        print("  2️⃣  Mostrar comandos para muestra de prueba")
        print("  3️⃣  Procesar tweets recolectados")
        print("  4️⃣  Generar visualizaciones")
        print("  5️⃣  Análisis personalizados")
        print("  6️⃣  Ejecutar pipeline completo (3 + 4)")
        print("  0️⃣  Salir")
        print("\n" + "-" * 70)
        
        try:
            opcion = input("\nOpción: ").strip()
            
            if opcion == "1":
                ejemplo_1_generar_script_recoleccion()
            elif opcion == "2":
                ejemplo_2_analisis_rapido()
            elif opcion == "3":
                ejemplo_3_procesar_tweets_recolectados()
            elif opcion == "4":
                ejemplo_4_generar_visualizaciones()
            elif opcion == "5":
                ejemplo_5_analisis_personalizado()
            elif opcion == "6":
                print("\n🚀 Ejecutando pipeline completo...\n")
                resultados = ejemplo_3_procesar_tweets_recolectados()
                if resultados:
                    ejemplo_4_generar_visualizaciones()
            elif opcion == "0":
                print("\n👋 ¡Hasta luego!\n")
                break
            else:
                print("\n❌ Opción no válida. Intenta de nuevo.")
            
            input("\nPresiona ENTER para continuar...")
            
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\nPresiona ENTER para continuar...")


if __name__ == "__main__":
    # Mostrar información inicial
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║     SISTEMA DE ANÁLISIS DE EMOCIONES EN TWEETS                   ║
    ║     Proyecto: Predicción de Homicidios en Culiacán              ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    
    Este sistema te permite:
    
    ✅ Recolectar tweets históricos sobre Culiacán
    ✅ Clasificar emociones automáticamente (5 categorías)
    ✅ Analizar tendencias temporales
    ✅ Generar visualizaciones profesionales
    ✅ Exportar datos para integración con modelos predictivos
    
    📋 REQUISITOS:
       - snscrape (pip install snscrape)
       - pysentimiento (pip install pysentimiento)
       - pandas, numpy, matplotlib, seaborn
    
    """)
    
    # Ejecutar menú interactivo
    menu_interactivo()
