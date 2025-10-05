"""
Script de prueba y validación del sistema de análisis de emociones
Incluye tests unitarios y ejemplos de datos de prueba
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import json


def generar_datos_prueba(n_dias: int = 30, tweets_por_dia: int = 100):
    """
    Genera datos de prueba sintéticos para testear el sistema
    
    Args:
        n_dias: Número de días a generar
        tweets_por_dia: Tweets por día (promedio)
    
    Returns:
        DataFrame con tweets sintéticos
    """
    print(f"Generando {n_dias} días con ~{tweets_por_dia} tweets/día...")
    
    # Plantillas de tweets por emoción
    plantillas = {
        'alegria': [
            "¡Qué bonito día en Culiacán! ☀️",
            "Me encanta mi ciudad 💚",
            "Feliz de estar en Culiacán",
            "Gran tarde en el Parque 87 🎉",
            "Los Dorados ganaron! ⚾️🎊"
        ],
        'tristeza': [
            "Extraño Culiacán 😢",
            "Qué triste situación",
            "Lloro por mi ciudad",
            "Perdimos el partido 😔",
            "Día gris en Culiacán"
        ],
        'ira': [
            "¡Esto no puede seguir así! 😤",
            "Indignante la situación",
            "Estoy molesto con las autoridades",
            "Qué rabia da esto!",
            "No es justo lo que pasa 😡"
        ],
        'miedo': [
            "Me da miedo salir 😨",
            "Situación preocupante",
            "No me siento seguro",
            "Tengo temor por la violencia",
            "Atemoriza la inseguridad"
        ],
        'sorpresa': [
            "¡No puedo creerlo! 😲",
            "Wow, increíble noticia",
            "Inesperado resultado",
            "Sorprendente lo que pasó",
            "¡Vaya! No me lo esperaba 🤯"
        ],
        'neutral': [
            "El clima hoy en Culiacán",
            "Reporte del día",
            "Información general",
            "Datos estadísticos",
            "Actualización de noticias"
        ]
    }
    
    tweets = []
    fecha_inicio = datetime(2025, 1, 1)
    
    for dia in range(n_dias):
        fecha = fecha_inicio + timedelta(days=dia)
        
        # Variar el número de tweets por día
        n_tweets = np.random.poisson(tweets_por_dia)
        
        # Distribución de emociones (puede variar por día)
        # Simular eventos: algunos días más tristes, otros más alegres
        if dia % 7 == 0:  # Domingos más alegres
            probs = [0.5, 0.1, 0.1, 0.1, 0.1, 0.1]
        elif dia % 5 == 0:  # Eventos negativos ocasionales
            probs = [0.1, 0.3, 0.3, 0.2, 0.05, 0.05]
        else:  # Días normales
            probs = [0.25, 0.2, 0.2, 0.15, 0.1, 0.1]
        
        emociones_dia = np.random.choice(
            list(plantillas.keys()),
            size=n_tweets,
            p=probs
        )
        
        for i, emocion in enumerate(emociones_dia):
            tweet = {
                'id': f"{fecha.strftime('%Y%m%d')}_{i:04d}",
                'date': (fecha + timedelta(hours=np.random.randint(0, 24),
                                         minutes=np.random.randint(0, 60))).isoformat(),
                'content': np.random.choice(plantillas[emocion]),
                'lang': 'es',
                'user': {'username': f'user_{np.random.randint(1, 500)}'},
                'emocion_real': emocion  # Ground truth para validación
            }
            tweets.append(tweet)
    
    df = pd.DataFrame(tweets)
    print(f"✅ Generados {len(df)} tweets")
    return df


def guardar_datos_prueba(df: pd.DataFrame, directorio: str = "data_tweets_culiacan/test"):
    """
    Guarda datos de prueba en formato JSONL por día
    
    Args:
        df: DataFrame con tweets
        directorio: Directorio donde guardar
    """
    dir_path = Path(directorio)
    dir_path.mkdir(parents=True, exist_ok=True)
    
    df['date_obj'] = pd.to_datetime(df['date'])
    df['fecha'] = df['date_obj'].dt.date
    
    for fecha, grupo in df.groupby('fecha'):
        archivo = dir_path / f"tweets_{fecha}.jsonl"
        # Excluir columna de ground truth
        grupo_sin_gt = grupo.drop(columns=['emocion_real', 'date_obj', 'fecha'])
        grupo_sin_gt.to_json(archivo, orient='records', lines=True, force_ascii=False)
    
    print(f"✅ Datos guardados en: {directorio}")
    print(f"   Archivos creados: {len(df['fecha'].unique())}")


def validar_clasificacion(df_clasificado: pd.DataFrame, mostrar_errores: bool = True):
    """
    Valida la clasificación contra ground truth
    
    Args:
        df_clasificado: DataFrame con tweets clasificados
        mostrar_errores: Si True, muestra ejemplos de errores
    
    Returns:
        Dict con métricas de validación
    """
    if 'emocion_real' not in df_clasificado.columns:
        print("⚠️  No hay ground truth para validar")
        return None
    
    print("\n" + "=" * 70)
    print("VALIDACIÓN DE CLASIFICACIÓN")
    print("=" * 70)
    
    # Calcular accuracy
    df_clasificado['correcto'] = df_clasificado['emocion'] == df_clasificado['emocion_real']
    accuracy = df_clasificado['correcto'].mean()
    
    print(f"\n📊 Accuracy global: {accuracy:.2%}")
    
    # Matriz de confusión
    from collections import defaultdict
    confusion = defaultdict(lambda: defaultdict(int))
    
    for _, row in df_clasificado.iterrows():
        confusion[row['emocion_real']][row['emocion']] += 1
    
    # Métricas por emoción
    emociones = ['alegria', 'tristeza', 'ira', 'miedo', 'sorpresa', 'neutral']
    
    print("\n📈 Métricas por emoción:")
    print("-" * 70)
    print(f"{'Emoción':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
    print("-" * 70)
    
    metricas = {}
    
    for emocion in emociones:
        # True Positives
        tp = confusion[emocion][emocion]
        
        # False Positives
        fp = sum(confusion[otra][emocion] for otra in emociones if otra != emocion)
        
        # False Negatives
        fn = sum(confusion[emocion][otra] for otra in emociones if otra != emocion)
        
        # Calcular métricas
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        metricas[emocion] = {
            'precision': precision,
            'recall': recall,
            'f1': f1
        }
        
        print(f"{emocion:<12} {precision:<12.2%} {recall:<12.2%} {f1:<12.2%}")
    
    # Mostrar errores comunes
    if mostrar_errores:
        print("\n❌ Errores más comunes:")
        print("-" * 70)
        
        errores = df_clasificado[~df_clasificado['correcto']]
        
        if len(errores) > 0:
            errores_resumen = errores.groupby(['emocion_real', 'emocion']).size().nlargest(10)
            
            for (real, predicho), count in errores_resumen.items():
                pct = count / len(df_clasificado) * 100
                print(f"  {real:10} → {predicho:10} : {count:4} veces ({pct:.1f}%)")
        
        # Ejemplos de errores
        print("\n📝 Ejemplos de errores:")
        print("-" * 70)
        
        ejemplos = errores.sample(min(5, len(errores)))
        for _, row in ejemplos.iterrows():
            print(f"\nTexto: {row['content']}")
            print(f"  Real: {row['emocion_real']:10} | Predicho: {row['emocion']:10}")
    
    return {
        'accuracy': accuracy,
        'metricas_por_emocion': metricas,
        'matriz_confusion': dict(confusion)
    }


def test_pipeline_completo():
    """Test del pipeline completo con datos sintéticos"""
    print("\n" + "=" * 70)
    print("TEST DEL PIPELINE COMPLETO")
    print("=" * 70)
    
    try:
        # 1. Generar datos de prueba
        print("\n1️⃣  Generando datos de prueba...")
        df_test = generar_datos_prueba(n_dias=7, tweets_por_dia=50)
        
        # 2. Guardar en formato correcto
        print("\n2️⃣  Guardando datos...")
        test_dir = "data_tweets_culiacan/test"
        guardar_datos_prueba(df_test, test_dir)
        
        # 3. Crear analizador y procesar
        print("\n3️⃣  Procesando con el analizador...")
        from tweets_sentiments_test import TweetsEmotionAnalyzer
        
        analyzer = TweetsEmotionAnalyzer(config_override={
            'dir_raw': test_dir,
            'dir_procesados': 'data_tweets_culiacan/test_procesados',
            'dir_resultados': 'data_tweets_culiacan/test_resultados'
        })
        
        # Cargar y procesar
        df_tweets = analyzer.cargar_tweets_raw()
        print(f"   Tweets cargados: {len(df_tweets)}")
        
        # Agregar ground truth antes de limpiar
        df_tweets = df_tweets.merge(
            df_test[['id', 'emocion_real']],
            on='id',
            how='left'
        )
        
        df_tweets = analyzer.limpiar_tweets(df_tweets)
        print(f"   Tweets después de limpieza: {len(df_tweets)}")
        
        df_tweets = analyzer.clasificar_tweets(df_tweets)
        print(f"   Tweets clasificados: {len(df_tweets)}")
        
        # 4. Validar clasificación
        print("\n4️⃣  Validando clasificación...")
        metricas = validar_clasificacion(df_tweets)
        
        # 5. Continuar con agregación
        print("\n5️⃣  Agregando por día...")
        df_diario = analyzer.agregar_por_dia(df_tweets)
        print(f"   Días procesados: {len(df_diario)}")
        
        # 6. Análisis
        print("\n6️⃣  Generando análisis...")
        analisis = analyzer.analisis_anual(df_diario)
        
        from tweets_sentiments_test import mostrar_resumen_rapido
        mostrar_resumen_rapido(analisis)
        
        # 7. Guardar resultados
        print("\n7️⃣  Guardando resultados...")
        analyzer.guardar_resultados(df_tweets, df_diario, analisis, sufijo="test")
        
        print("\n" + "=" * 70)
        print("✅ TEST COMPLETADO EXITOSAMENTE")
        print("=" * 70)
        
        return {
            'metricas': metricas,
            'tweets': df_tweets,
            'diario': df_diario,
            'analisis': analisis
        }
        
    except Exception as e:
        print(f"\n❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
        return None


def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas"""
    print("\n" + "=" * 70)
    print("VERIFICANDO DEPENDENCIAS")
    print("=" * 70 + "\n")
    
    dependencias = {
        'pandas': 'pandas',
        'numpy': 'numpy',
        'matplotlib': 'matplotlib.pyplot',
        'seaborn': 'seaborn',
        'tqdm': 'tqdm',
        'pysentimiento': 'pysentimiento'
    }
    
    faltantes = []
    instaladas = []
    
    for nombre, modulo in dependencias.items():
        try:
            __import__(modulo)
            instaladas.append(nombre)
            print(f"✅ {nombre:<15} - OK")
        except ImportError:
            faltantes.append(nombre)
            print(f"❌ {nombre:<15} - NO INSTALADO")
    
    print("\n" + "-" * 70)
    
    if faltantes:
        print(f"\n⚠️  Faltan {len(faltantes)} dependencias:")
        print(f"\nPara instalar, ejecuta:")
        print(f"pip install {' '.join(faltantes)}")
        return False
    else:
        print(f"\n✅ Todas las dependencias están instaladas ({len(instaladas)}/{len(dependencias)})")
        return True


def test_modelo_emocion():
    """Test específico del modelo de clasificación de emociones"""
    print("\n" + "=" * 70)
    print("TEST DEL MODELO DE EMOCIONES")
    print("=" * 70 + "\n")
    
    try:
        from tweets_sentiments_test import TweetsEmotionAnalyzer
        
        analyzer = TweetsEmotionAnalyzer()
        analyzer.cargar_modelo_emocion()
        
        # Casos de prueba
        casos = [
            ("¡Qué feliz estoy en Culiacán! 😊", "alegria"),
            ("Estoy muy triste por la situación 😢", "tristeza"),
            ("Me da mucho miedo salir 😨", "miedo"),
            ("¡Qué coraje me da esto! 😡", "ira"),
            ("¡No puedo creer esto! 😲", "sorpresa"),
            ("El clima está a 25 grados", "neutral")
        ]
        
        print("Clasificando casos de prueba:\n")
        print(f"{'Texto':<50} {'Esperado':<12} {'Predicho':<12} {'Match'}")
        print("-" * 80)
        
        correctos = 0
        
        for texto, esperado in casos:
            predicho = analyzer.clasificar_emocion(texto)
            match = "✅" if predicho == esperado else "❌"
            
            if predicho == esperado:
                correctos += 1
            
            # Truncar texto si es muy largo
            texto_corto = texto[:47] + "..." if len(texto) > 50 else texto
            print(f"{texto_corto:<50} {esperado:<12} {predicho:<12} {match}")
        
        accuracy = correctos / len(casos)
        print("\n" + "-" * 80)
        print(f"Accuracy en casos de prueba: {accuracy:.1%} ({correctos}/{len(casos)})")
        
        return accuracy >= 0.5  # Al menos 50% de acierto
        
    except Exception as e:
        print(f"\n❌ Error en test del modelo: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║          TEST Y VALIDACIÓN DEL SISTEMA DE EMOCIONES              ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Menú de tests
    while True:
        print("\nSelecciona un test:")
        print("\n  1️⃣  Verificar dependencias")
        print("  2️⃣  Test del modelo de emociones")
        print("  3️⃣  Generar datos de prueba")
        print("  4️⃣  Test del pipeline completo")
        print("  5️⃣  Ejecutar todos los tests")
        print("  0️⃣  Salir")
        print("\n" + "-" * 70)
        
        try:
            opcion = input("\nOpción: ").strip()
            
            if opcion == "1":
                verificar_dependencias()
            
            elif opcion == "2":
                if verificar_dependencias():
                    test_modelo_emocion()
                else:
                    print("\n⚠️  Instala las dependencias primero")
            
            elif opcion == "3":
                n_dias = int(input("Número de días (default 30): ") or "30")
                tweets_dia = int(input("Tweets por día (default 100): ") or "100")
                df = generar_datos_prueba(n_dias, tweets_dia)
                guardar_datos_prueba(df)
                print(f"\n✅ Datos guardados en: data_tweets_culiacan/test/")
            
            elif opcion == "4":
                if verificar_dependencias():
                    test_pipeline_completo()
                else:
                    print("\n⚠️  Instala las dependencias primero")
            
            elif opcion == "5":
                print("\n🚀 EJECUTANDO SUITE COMPLETA DE TESTS\n")
                
                # Test 1: Dependencias
                if not verificar_dependencias():
                    print("\n❌ Tests abortados. Instala las dependencias.")
                    continue
                
                # Test 2: Modelo
                modelo_ok = test_modelo_emocion()
                
                # Test 3: Pipeline
                if modelo_ok:
                    resultados = test_pipeline_completo()
                    
                    if resultados:
                        print("\n" + "=" * 70)
                        print("✅ TODOS LOS TESTS PASARON")
                        print("=" * 70)
                    else:
                        print("\n" + "=" * 70)
                        print("❌ ALGUNOS TESTS FALLARON")
                        print("=" * 70)
                else:
                    print("\n⚠️  Pipeline test omitido por fallo en modelo")
            
            elif opcion == "0":
                print("\n👋 ¡Hasta luego!\n")
                break
            
            else:
                print("\n❌ Opción no válida")
            
            input("\nPresiona ENTER para continuar...")
            
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\nPresiona ENTER para continuar...")
