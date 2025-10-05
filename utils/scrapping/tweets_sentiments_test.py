"""
Sistema de análisis de emociones en tweets sobre Culiacán
Autor: Carlos
Fecha: 2025-10-04

Este módulo permite:
1. Recolectar tweets históricos sobre Culiacán usando snscrape
2. Clasificar emociones usando pysentimiento (5 categorías + neutral)
3. Agregar por día y determinar "emoción del día"
4. Generar análisis anuales y visualizaciones
"""

import pandas as pd
import numpy as np
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from tqdm import tqdm
import warnings

warnings.filterwarnings('ignore')

# Importaciones locales
from config_tweets import *


class TweetsEmotionAnalyzer:
    """Clase principal para análisis de emociones en tweets"""
    
    def __init__(self, config_override: Optional[Dict] = None):
        """
        Inicializa el analizador
        
        Args:
            config_override: Diccionario con configuraciones a sobrescribir
        """
        self.config = self._setup_config(config_override)
        self._setup_logging()
        self._setup_directories()
        self.analyzer = None
        
    def _setup_config(self, override: Optional[Dict]) -> Dict:
        """Configura parámetros del sistema"""
        config = {
            'fecha_inicio': ANIO_INICIO,
            'fecha_fin': ANIO_FIN,
            'zona': ZONA_HORARIA,
            'palabras': PALABRAS_CLAVE,
            'idioma': IDIOMA,
            'incluir_neutral': INCLUIR_NEUTRAL_COMO_GANADOR,
            'dir_raw': DIR_DATOS_RAW,
            'dir_procesados': DIR_DATOS_PROCESADOS,
            'dir_resultados': DIR_RESULTADOS,
            'dir_viz': DIR_VISUALIZACIONES,
        }
        if override:
            config.update(override)
        return config
    
    def _setup_logging(self):
        """Configura el sistema de logging"""
        logging.basicConfig(
            level=getattr(logging, LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(LOG_FILE),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _setup_directories(self):
        """Crea directorios necesarios"""
        for dir_path in [self.config['dir_raw'], 
                         self.config['dir_procesados'],
                         self.config['dir_resultados'],
                         self.config['dir_viz']]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Directorios creados/verificados")
    
    def generar_comando_snscrape(self, fecha: str) -> str:
        """
        Genera comando snscrape para un día específico
        
        Args:
            fecha: Fecha en formato YYYY-MM-DD
            
        Returns:
            String con el comando completo
        """
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
        fecha_siguiente = (fecha_dt + timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Construir query de búsqueda
        palabras_query = " OR ".join(self.config['palabras'])
        
        filtros = []
        if EXCLUIR_RETWEETS:
            filtros.append("-filter:retweets")
        if EXCLUIR_REPLIES:
            filtros.append("-filter:replies")
        if SOLO_VERIFICADOS:
            filtros.append("filter:verified")
            
        filtros_str = " ".join(filtros)
        
        query = f'"{palabras_query} lang:{self.config["idioma"]} since:{fecha} until:{fecha_siguiente} {filtros_str}"'
        
        output_file = Path(self.config['dir_raw']) / f"tweets_{fecha}.jsonl"
        
        comando = f'snscrape --jsonl twitter-search {query} > {output_file}'
        
        return comando
    
    def generar_script_recoleccion(self, output_file: str = "recolectar_tweets.ps1"):
        """
        Genera script PowerShell para recolectar todos los días del rango
        
        Args:
            output_file: Nombre del archivo de script a generar
        """
        inicio = datetime.strptime(self.config['fecha_inicio'], "%Y-%m-%d")
        fin = datetime.strptime(self.config['fecha_fin'], "%Y-%m-%d")
        
        lineas = [
            "# Script de recolección de tweets sobre Culiacán",
            f"# Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"# Período: {self.config['fecha_inicio']} a {self.config['fecha_fin']}",
            "",
            "Write-Host 'Iniciando recolección de tweets...' -ForegroundColor Green",
            ""
        ]
        
        fecha_actual = inicio
        contador = 0
        
        while fecha_actual <= fin:
            fecha_str = fecha_actual.strftime("%Y-%m-%d")
            comando = self.generar_comando_snscrape(fecha_str)
            
            lineas.append(f"# Día {contador + 1}: {fecha_str}")
            lineas.append(f"Write-Host 'Recolectando {fecha_str}...' -ForegroundColor Cyan")
            lineas.append(comando)
            lineas.append("")
            
            fecha_actual += timedelta(days=1)
            contador += 1
        
        lineas.append(f"Write-Host 'Completado! {contador} días recolectados.' -ForegroundColor Green")
        
        script_path = Path(output_file)
        script_path.write_text("\n".join(lineas), encoding='utf-8')
        
        self.logger.info(f"Script de recolección generado: {output_file}")
        self.logger.info(f"Total de días a recolectar: {contador}")
        
        return str(script_path)
    
    def cargar_tweets_raw(self) -> pd.DataFrame:
        """
        Carga todos los tweets recolectados desde archivos JSONL
        
        Returns:
            DataFrame con todos los tweets
        """
        self.logger.info("Cargando tweets desde archivos raw...")
        
        data_dir = Path(self.config['dir_raw'])
        archivos = sorted(data_dir.glob("tweets_*.jsonl"))
        
        if not archivos:
            self.logger.warning(f"No se encontraron archivos en {data_dir}")
            return pd.DataFrame()
        
        frames = []
        errores = 0
        
        for archivo in tqdm(archivos, desc="Cargando archivos"):
            try:
                df = pd.read_json(archivo, lines=True)
                if not df.empty and 'date' in df.columns:
                    df['archivo_origen'] = archivo.name
                    frames.append(df)
            except Exception as e:
                self.logger.error(f"Error cargando {archivo}: {e}")
                errores += 1
        
        if not frames:
            self.logger.warning("No se pudieron cargar tweets")
            return pd.DataFrame()
        
        tweets = pd.concat(frames, ignore_index=True)
        
        self.logger.info(f"Tweets cargados: {len(tweets):,}")
        self.logger.info(f"Archivos procesados: {len(frames)}/{len(archivos)}")
        if errores > 0:
            self.logger.warning(f"Archivos con error: {errores}")
        
        return tweets
    
    def limpiar_tweets(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia y filtra los tweets
        
        Args:
            df: DataFrame con tweets raw
            
        Returns:
            DataFrame limpio
        """
        self.logger.info("Limpiando tweets...")
        inicial = len(df)
        
        if df.empty:
            return df
        
        # Convertir fechas a zona horaria correcta
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], utc=True)
            df['date'] = df['date'].dt.tz_convert(self.config['zona'])
            df['fecha'] = df['date'].dt.date
            df['hora'] = df['date'].dt.hour
        
        # Asegurar que existe columna de contenido
        if 'content' not in df.columns and 'rawContent' in df.columns:
            df['content'] = df['rawContent']
        
        # Filtros básicos
        df = df[df['content'].notna()].copy()
        df = df[df['content'].str.len() >= MIN_CARACTERES].copy()
        
        # Remover spam
        patron_spam = '|'.join(PALABRAS_SPAM)
        df = df[~df['content'].str.lower().str.contains(patron_spam, na=False)].copy()
        
        # Filtrar por idioma si está disponible
        if 'lang' in df.columns:
            df = df[df['lang'] == self.config['idioma']].copy()
        
        # Remover duplicados
        if 'id' in df.columns:
            df = df.drop_duplicates(subset=['id'])
        else:
            df = df.drop_duplicates(subset=['content'])
        
        # Filtrar bots (usuarios que tuitean demasiado)
        if 'user' in df.columns:
            try:
                df['username'] = df['user'].apply(lambda x: x.get('username', '') if isinstance(x, dict) else '')
                tweets_por_usuario_dia = df.groupby(['fecha', 'username']).size()
                usuarios_normales = tweets_por_usuario_dia[tweets_por_usuario_dia <= MAX_TWEETS_POR_USUARIO_DIA].index
                df = df[df.apply(lambda x: (x['fecha'], x['username']) in usuarios_normales, axis=1)].copy()
            except Exception as e:
                self.logger.warning(f"No se pudo filtrar por usuario: {e}")
        
        final = len(df)
        self.logger.info(f"Tweets después de limpieza: {final:,} ({inicial-final:,} removidos)")
        
        return df
    
    def cargar_modelo_emocion(self):
        """Carga el modelo de análisis de emociones"""
        if self.analyzer is None:
            self.logger.info("Cargando modelo de emociones...")
            try:
                from pysentimiento import create_analyzer
                self.analyzer = create_analyzer(task=MODELO_EMOCION, lang=MODELO_LANG)
                self.logger.info("Modelo cargado exitosamente")
            except ImportError:
                self.logger.error("pysentimiento no instalado. Ejecuta: pip install pysentimiento")
                raise
            except Exception as e:
                self.logger.error(f"Error cargando modelo: {e}")
                raise
    
    def clasificar_emocion(self, texto: str) -> dict:
        """
        Clasifica la emoción de un texto
        
        Args:
            texto: Texto a clasificar
            
        Returns:
            Dict con 'emocion' y 'score'
        """
        if self.analyzer is None:
            self.cargar_modelo_emocion()
        
        try:
            resultado = self.analyzer.predict(texto)
            
            # Extraer la etiqueta y probabilidad según la estructura del resultado
            if hasattr(resultado, 'output'):
                label = resultado.output
                score = getattr(resultado, 'probas', {}).get(label, 0.5) if hasattr(resultado, 'probas') else 0.5
            elif hasattr(resultado, 'label'):
                label = resultado.label
                score = getattr(resultado, 'score', 0.5)
            elif hasattr(resultado, 'probas'):
                label = max(resultado.probas, key=resultado.probas.get)
                score = resultado.probas[label]
            else:
                label = 'neutral'
                score = 0.5
            
            # Mapear a nuestras 5 categorías
            label_lower = str(label).lower()
            emocion = MAPEO_EMOCIONES.get(label_lower, 'neutral')
            
            return {
                'emocion': emocion,
                'score': float(score)
            }
            
        except Exception as e:
            self.logger.debug(f"Error clasificando: {e}")
            return {
                'emocion': 'neutral',
                'score': 0.5
            }
    
    def clasificar_tweets(self, df: pd.DataFrame, batch_size: int = None) -> pd.DataFrame:
        """
        Clasifica emociones de todos los tweets
        
        Args:
            df: DataFrame con tweets
            batch_size: Tamaño de lote para procesamiento
            
        Returns:
            DataFrame con columnas 'emocion' y 'score'
        """
        if df.empty:
            return df
        
        self.cargar_modelo_emocion()
        
        batch_size = batch_size or BATCH_SIZE
        self.logger.info(f"Clasificando {len(df):,} tweets...")
        
        emociones = []
        scores = []
        
        for i in tqdm(range(0, len(df), batch_size), desc="Clasificando emociones"):
            batch = df.iloc[i:i+batch_size]
            batch_resultados = batch['content'].apply(self.clasificar_emocion)
            
            for resultado in batch_resultados:
                emociones.append(resultado['emocion'])
                scores.append(resultado['score'])
        
        df['emocion'] = emociones
        df['score'] = scores
        
        # Estadísticas
        dist = df['emocion'].value_counts()
        self.logger.info(f"Distribución de emociones:\n{dist}")
        
        return df
    
    def agregar_por_dia(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Agrega tweets por día y calcula estadísticas
        
        Args:
            df: DataFrame con tweets clasificados
            
        Returns:
            DataFrame con resumen diario
        """
        self.logger.info("Agregando por día...")
        
        if df.empty:
            return pd.DataFrame()
        
        # Contar por fecha y emoción
        counts = df.groupby(['fecha', 'emocion']).size().unstack(fill_value=0)
        
        # Asegurar todas las columnas
        todas_emociones = EMOCIONES_PRINCIPALES + ['neutral']
        for col in todas_emociones:
            if col not in counts.columns:
                counts[col] = 0
        
        # Reordenar columnas
        counts = counts[todas_emociones]
        
        # Total del día
        counts['n_total'] = counts.sum(axis=1)
        
        # Calcular porcentajes
        for emocion in todas_emociones:
            counts[f'pct_{emocion}'] = (counts[emocion] / counts['n_total'] * 100).round(2)
        
        # Determinar ganador del día
        def calcular_ganador(row):
            emociones_evaluar = EMOCIONES_PRINCIPALES.copy()
            
            if self.config['incluir_neutral']:
                emociones_evaluar.append('neutral')
            
            # Encontrar la emoción con mayor porcentaje
            mejor = max(emociones_evaluar, key=lambda e: row[f'pct_{e}'])
            
            return mejor
        
        counts['ganador_del_dia'] = counts.apply(calcular_ganador, axis=1)
        counts['intensidad'] = counts.apply(
            lambda row: row[f"pct_{row['ganador_del_dia']}"], axis=1
        )
        
        resultado = counts.reset_index()
        
        self.logger.info(f"Días procesados: {len(resultado)}")
        
        return resultado
    
    def analisis_anual(self, df_diario: pd.DataFrame) -> Dict:
        """
        Genera análisis del año completo
        
        Args:
            df_diario: DataFrame con resumen diario
            
        Returns:
            Diccionario con métricas anuales
        """
        self.logger.info("Generando análisis anual...")
        
        if df_diario.empty:
            return {}
        
        analisis = {
            'periodo': {
                'inicio': str(df_diario['fecha'].min()),
                'fin': str(df_diario['fecha'].max()),
                'dias_analizados': len(df_diario)
            },
            'tweets_totales': int(df_diario['n_total'].sum()),
            'promedio_tweets_dia': float(df_diario['n_total'].mean()),
            'emocion_anual_moda': df_diario['ganador_del_dia'].mode()[0],
            'distribucion_ganadores': df_diario['ganador_del_dia'].value_counts().to_dict(),
            'promedios_porcentuales': {},
            'dias_mas_emotivos': {},
            'estadisticas_por_emocion': {}
        }
        
        # Promedios porcentuales por emoción
        for emocion in EMOCIONES_PRINCIPALES + ['neutral']:
            col = f'pct_{emocion}'
            if col in df_diario.columns:
                analisis['promedios_porcentuales'][emocion] = float(df_diario[col].mean())
        
        # Top 10 días más intensos por emoción
        for emocion in EMOCIONES_PRINCIPALES:
            top_dias = df_diario[df_diario['ganador_del_dia'] == emocion].nlargest(5, 'intensidad')
            analisis['dias_mas_emotivos'][emocion] = [
                {
                    'fecha': str(row['fecha']),
                    'intensidad': float(row['intensidad']),
                    'tweets': int(row['n_total'])
                }
                for _, row in top_dias.iterrows()
            ]
        
        # Estadísticas por emoción
        for emocion in EMOCIONES_PRINCIPALES + ['neutral']:
            analisis['estadisticas_por_emocion'][emocion] = {
                'total_tweets': int(df_diario[emocion].sum()),
                'dias_como_ganador': int((df_diario['ganador_del_dia'] == emocion).sum()),
                'porcentaje_medio': float(df_diario[f'pct_{emocion}'].mean()),
                'porcentaje_max': float(df_diario[f'pct_{emocion}'].max())
            }
        
        return analisis
    
    def guardar_resultados(self, df_tweets: pd.DataFrame, df_diario: pd.DataFrame, 
                          analisis: Dict, sufijo: str = ""):
        """
        Guarda todos los resultados del análisis
        
        Args:
            df_tweets: DataFrame con tweets clasificados
            df_diario: DataFrame con resumen diario
            analisis: Diccionario con análisis anual
            sufijo: Sufijo para nombres de archivo
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sufijo = f"_{sufijo}" if sufijo else f"_{timestamp}"
        
        dir_resultados = Path(self.config['dir_resultados'])
        
        # Guardar tweets clasificados
        if not df_tweets.empty:
            tweets_file = dir_resultados / f"tweets_clasificados{sufijo}.csv"
            df_tweets.to_csv(tweets_file, index=False, encoding='utf-8-sig')
            self.logger.info(f"Tweets clasificados guardados: {tweets_file}")
        
        # Guardar resumen diario
        if not df_diario.empty:
            diario_file = dir_resultados / f"resumen_diario{sufijo}.csv"
            df_diario.to_csv(diario_file, index=False, encoding='utf-8-sig')
            self.logger.info(f"Resumen diario guardado: {diario_file}")
        
        # Guardar análisis anual
        if analisis:
            analisis_file = dir_resultados / f"analisis_anual{sufijo}.json"
            with open(analisis_file, 'w', encoding='utf-8') as f:
                json.dump(analisis, f, indent=2, ensure_ascii=False, default=str)
            self.logger.info(f"Análisis anual guardado: {analisis_file}")
        
        # Guardar resumen textual
        self._generar_reporte_texto(analisis, dir_resultados / f"reporte{sufijo}.txt")
    
    def _generar_reporte_texto(self, analisis: Dict, archivo: Path):
        """Genera un reporte en texto plano del análisis"""
        lineas = [
            "=" * 80,
            "ANÁLISIS DE EMOCIONES EN TWEETS SOBRE CULIACÁN",
            "=" * 80,
            "",
            f"Período: {analisis['periodo']['inicio']} a {analisis['periodo']['fin']}",
            f"Días analizados: {analisis['periodo']['dias_analizados']}",
            f"Total de tweets: {analisis['tweets_totales']:,}",
            f"Promedio diario: {analisis['promedio_tweets_dia']:.1f} tweets",
            "",
            "=" * 80,
            "EMOCIÓN PREDOMINANTE DEL AÑO",
            "=" * 80,
            f"→ {analisis['emocion_anual_moda'].upper()}",
            "",
            "Distribución de días ganadores:",
        ]
        
        for emocion, dias in sorted(analisis['distribucion_ganadores'].items(), 
                                    key=lambda x: x[1], reverse=True):
            pct = (dias / analisis['periodo']['dias_analizados']) * 100
            lineas.append(f"  {emocion:12} : {dias:3} días ({pct:5.1f}%)")
        
        lineas.extend([
            "",
            "=" * 80,
            "PROMEDIOS PORCENTUALES POR EMOCIÓN",
            "=" * 80
        ])
        
        for emocion in EMOCIONES_PRINCIPALES + ['neutral']:
            if emocion in analisis['promedios_porcentuales']:
                pct = analisis['promedios_porcentuales'][emocion]
                lineas.append(f"  {emocion:12} : {pct:5.2f}%")
        
        lineas.extend([
            "",
            "=" * 80,
            "DÍAS MÁS INTENSOS POR EMOCIÓN",
            "=" * 80
        ])
        
        for emocion in EMOCIONES_PRINCIPALES:
            if emocion in analisis['dias_mas_emotivos']:
                dias = analisis['dias_mas_emotivos'][emocion]
                if dias:
                    lineas.append(f"\n{emocion.upper()}:")
                    for dia in dias[:3]:
                        lineas.append(f"  {dia['fecha']} - {dia['intensidad']:.1f}% ({dia['tweets']} tweets)")
        
        archivo.write_text("\n".join(lineas), encoding='utf-8')
        self.logger.info(f"Reporte generado: {archivo}")
    
    def pipeline_completo(self, desde_raw: bool = True):
        """
        Ejecuta el pipeline completo de análisis
        
        Args:
            desde_raw: Si True, carga desde archivos raw. Si False, espera tweets ya cargados.
        """
        self.logger.info("=" * 80)
        self.logger.info("INICIANDO PIPELINE DE ANÁLISIS DE EMOCIONES")
        self.logger.info("=" * 80)
        
        try:
            # 1. Cargar tweets
            if desde_raw:
                df_tweets = self.cargar_tweets_raw()
            else:
                self.logger.warning("Debes proporcionar los tweets manualmente")
                return None
            
            if df_tweets.empty:
                self.logger.error("No hay tweets para procesar")
                return None
            
            # 2. Limpiar
            df_tweets = self.limpiar_tweets(df_tweets)
            
            if df_tweets.empty:
                self.logger.error("No hay tweets después de limpieza")
                return None
            
            # 3. Clasificar emociones
            df_tweets = self.clasificar_tweets(df_tweets)
            
            # 4. Agregar por día
            df_diario = self.agregar_por_dia(df_tweets)
            
            # 5. Análisis anual
            analisis = self.analisis_anual(df_diario)
            
            # 6. Guardar resultados
            self.guardar_resultados(df_tweets, df_diario, analisis)
            
            self.logger.info("=" * 80)
            self.logger.info("PIPELINE COMPLETADO EXITOSAMENTE")
            self.logger.info("=" * 80)
            
            return {
                'tweets': df_tweets,
                'diario': df_diario,
                'analisis': analisis
            }
            
        except Exception as e:
            self.logger.error(f"Error en pipeline: {e}", exc_info=True)
            raise


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def mostrar_resumen_rapido(analisis: Dict):
    """Muestra un resumen rápido del análisis en consola"""
    print("\n" + "=" * 60)
    print("RESUMEN RÁPIDO - ANÁLISIS DE EMOCIONES")
    print("=" * 60)
    print(f"\n📅 Período: {analisis['periodo']['inicio']} → {analisis['periodo']['fin']}")
    print(f"📊 Total tweets: {analisis['tweets_totales']:,}")
    print(f"📈 Promedio/día: {analisis['promedio_tweets_dia']:.0f}")
    print(f"\n🏆 EMOCIÓN DEL AÑO: {analisis['emocion_anual_moda'].upper()}")
    print("\n📊 Distribución:")
    for emocion, dias in sorted(analisis['distribucion_ganadores'].items(), 
                                key=lambda x: x[1], reverse=True):
        pct = (dias / analisis['periodo']['dias_analizados']) * 100
        barra = "█" * int(pct / 2)
        print(f"  {emocion:10} │{barra:50}│ {pct:5.1f}%")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    # Ejemplo de uso básico
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  ANALIZADOR DE EMOCIONES EN TWEETS SOBRE CULIACÁN           ║
    ╚══════════════════════════════════════════════════════════════╝
    
    Pasos para usar este sistema:
    
    1️⃣  GENERAR SCRIPT DE RECOLECCIÓN:
        analyzer = TweetsEmotionAnalyzer()
        analyzer.generar_script_recoleccion("recolectar.ps1")
    
    2️⃣  EJECUTAR RECOLECCIÓN:
        Ejecuta el script generado en PowerShell
        (Esto tomará varias horas para un año completo)
    
    3️⃣  PROCESAR Y ANALIZAR:
        resultados = analyzer.pipeline_completo()
    
    4️⃣  VISUALIZAR:
        from visualizador_emociones import crear_visualizaciones
        crear_visualizaciones(resultados['diario'])
    
    """)
    
    # Crear instancia
    analyzer = TweetsEmotionAnalyzer()
    
    # Generar script de recolección
    print("Generando script de recolección...")
    script = analyzer.generar_script_recoleccion("recolectar_tweets_culiacan.ps1")
    print(f"✅ Script generado: {script}")
    print("\nEjecútalo en PowerShell para iniciar la recolección.")
