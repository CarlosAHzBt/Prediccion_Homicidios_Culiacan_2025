"""
Visualizador de análisis de emociones en tweets
Genera gráficos y visualizaciones del análisis temporal
"""

import matplotlib
matplotlib.use('Agg')  # Backend sin GUI para servidores/scripts

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
import calendar
from typing import Optional

# Configuración de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Colores por emoción
COLORES_EMOCIONES = {
    'alegria': '#FFD700',    # Dorado
    'tristeza': '#4169E1',   # Azul
    'ira': '#DC143C',        # Rojo
    'miedo': '#9370DB',      # Púrpura
    'sorpresa': '#FF8C00',   # Naranja
    'neutral': '#808080'     # Gris
}


class VisualizadorEmociones:
    """Genera visualizaciones del análisis de emociones"""
    
    def __init__(self, dir_salida: str = "data_tweets_culiacan/visualizaciones"):
        self.dir_salida = Path(dir_salida)
        self.dir_salida.mkdir(parents=True, exist_ok=True)
        
        # Configurar matplotlib para español
        plt.rcParams['axes.unicode_minus'] = False
        
    def serie_temporal_porcentajes(self, df: pd.DataFrame, 
                                   guardar: bool = True,
                                   archivo: str = "serie_temporal_emociones.png"):
        """
        Gráfico de serie temporal con porcentajes por emoción
        
        Args:
            df: DataFrame con resumen diario
            guardar: Si True, guarda el gráfico
            archivo: Nombre del archivo de salida
        """
        fig, ax = plt.subplots(figsize=(16, 8))
        
        # Asegurar que fecha es datetime
        df = df.copy()
        df['fecha'] = pd.to_datetime(df['fecha'])
        df = df.sort_values('fecha')
        
        # Graficar cada emoción
        emociones = ['alegria', 'tristeza', 'ira', 'miedo', 'sorpresa']
        
        for emocion in emociones:
            col = f'pct_{emocion}'
            if col in df.columns:
                ax.plot(df['fecha'], df[col], 
                       label=emocion.capitalize(),
                       color=COLORES_EMOCIONES[emocion],
                       linewidth=2.5,
                       alpha=0.8)
        
        ax.set_xlabel('Fecha', fontsize=12, fontweight='bold')
        ax.set_ylabel('Porcentaje (%)', fontsize=12, fontweight='bold')
        ax.set_title('Evolución Temporal de Emociones en Tweets sobre Culiacán',
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper left', fontsize=10, framealpha=0.9)
        ax.grid(True, alpha=0.3)
        
        # Rotar etiquetas del eje x
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        
        if guardar:
            ruta = self.dir_salida / archivo
            plt.savefig(ruta, dpi=300, bbox_inches='tight')
            print(f"✅ Serie temporal guardada: {ruta}")
        
        return fig, ax
    
    def calendario_emociones(self, df: pd.DataFrame,
                            guardar: bool = True,
                            archivo: str = "calendario_emociones.png"):
        """
        Heatmap tipo calendario con la emoción ganadora de cada día
        
        Args:
            df: DataFrame con resumen diario
            guardar: Si True, guarda el gráfico
            archivo: Nombre del archivo de salida
        """
        df = df.copy()
        df['fecha'] = pd.to_datetime(df['fecha'])
        
        # Extraer año, mes, día
        df['año'] = df['fecha'].dt.year
        df['mes'] = df['fecha'].dt.month
        df['dia'] = df['fecha'].dt.day
        
        años = sorted(df['año'].unique())
        
        # Crear figura con subplots por año
        n_años = len(años)
        fig, axes = plt.subplots(n_años, 1, figsize=(18, 5 * n_años))
        
        if n_años == 1:
            axes = [axes]
        
        for idx, año in enumerate(años):
            ax = axes[idx]
            df_año = df[df['año'] == año]
            
            # Crear matriz 12 (meses) x 31 (días)
            matriz = np.full((12, 31), np.nan)
            
            for _, row in df_año.iterrows():
                mes = row['mes'] - 1  # 0-indexed
                dia = row['dia'] - 1  # 0-indexed
                
                # Codificar emoción como número
                emocion_map = {
                    'alegria': 0, 'tristeza': 1, 'ira': 2,
                    'miedo': 3, 'sorpresa': 4, 'neutral': 5
                }
                matriz[mes, dia] = emocion_map.get(row['ganador_del_dia'], 5)
            
            # Crear el heatmap
            im = ax.imshow(matriz, aspect='auto', cmap='tab10', 
                          interpolation='nearest', vmin=0, vmax=5)
            
            # Configurar ejes
            ax.set_yticks(range(12))
            ax.set_yticklabels(['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                              'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
            ax.set_xticks(range(0, 31, 5))
            ax.set_xticklabels(range(1, 32, 5))
            ax.set_xlabel('Día del mes', fontsize=10)
            ax.set_title(f'Calendario de Emociones - {año}', 
                        fontsize=12, fontweight='bold')
            
            # Grid
            ax.set_xticks(np.arange(31) - 0.5, minor=True)
            ax.set_yticks(np.arange(12) - 0.5, minor=True)
            ax.grid(which='minor', color='white', linestyle='-', linewidth=0.5)
        
        # Leyenda común
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=COLORES_EMOCIONES['alegria'], label='Alegría'),
            Patch(facecolor=COLORES_EMOCIONES['tristeza'], label='Tristeza'),
            Patch(facecolor=COLORES_EMOCIONES['ira'], label='Ira'),
            Patch(facecolor=COLORES_EMOCIONES['miedo'], label='Miedo'),
            Patch(facecolor=COLORES_EMOCIONES['sorpresa'], label='Sorpresa'),
            Patch(facecolor=COLORES_EMOCIONES['neutral'], label='Neutral')
        ]
        fig.legend(handles=legend_elements, loc='upper center', 
                  ncol=6, bbox_to_anchor=(0.5, 1.02), fontsize=10)
        
        plt.tight_layout()
        
        if guardar:
            ruta = self.dir_salida / archivo
            plt.savefig(ruta, dpi=300, bbox_inches='tight')
            print(f"✅ Calendario guardado: {ruta}")
        
        return fig, axes
    
    def distribucion_anual(self, df: pd.DataFrame,
                          guardar: bool = True,
                          archivo: str = "distribucion_anual.png"):
        """
        Gráfico de barras con distribución de días ganadores
        
        Args:
            df: DataFrame con resumen diario
            guardar: Si True, guarda el gráfico
            archivo: Nombre del archivo de salida
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Contar ganadores
        ganadores = df['ganador_del_dia'].value_counts()
        
        # Gráfico 1: Barras
        colores = [COLORES_EMOCIONES.get(e, '#808080') for e in ganadores.index]
        ganadores.plot(kind='bar', ax=ax1, color=colores, edgecolor='black')
        ax1.set_title('Días Ganados por Emoción', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Emoción', fontsize=12)
        ax1.set_ylabel('Número de días', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(axis='y', alpha=0.3)
        
        # Agregar valores en las barras
        for i, v in enumerate(ganadores.values):
            ax1.text(i, v + 1, str(v), ha='center', va='bottom', fontweight='bold')
        
        # Gráfico 2: Pie chart
        ax2.pie(ganadores.values, labels=ganadores.index, autopct='%1.1f%%',
               colors=colores, startangle=90, textprops={'fontsize': 10})
        ax2.set_title('Proporción de Días Ganados', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if guardar:
            ruta = self.dir_salida / archivo
            plt.savefig(ruta, dpi=300, bbox_inches='tight')
            print(f"✅ Distribución anual guardada: {ruta}")
        
        return fig, (ax1, ax2)
    
    def intensidad_por_emocion(self, df: pd.DataFrame,
                              guardar: bool = True,
                              archivo: str = "intensidad_emociones.png"):
        """
        Box plots de intensidad por emoción
        
        Args:
            df: DataFrame con resumen diario
            guardar: Si True, guarda el gráfico
            archivo: Nombre del archivo de salida
        """
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Preparar datos para boxplot
        datos_plot = []
        labels_plot = []
        colores_plot = []
        
        emociones = ['alegria', 'tristeza', 'ira', 'miedo', 'sorpresa', 'neutral']
        
        for emocion in emociones:
            col = f'pct_{emocion}'
            if col in df.columns:
                datos_plot.append(df[col].dropna())
                labels_plot.append(emocion.capitalize())
                colores_plot.append(COLORES_EMOCIONES.get(emocion, '#808080'))
        
        # Crear boxplot
        bp = ax.boxplot(datos_plot, labels=labels_plot, patch_artist=True,
                       showmeans=True, meanline=True)
        
        # Colorear cajas
        for patch, color in zip(bp['boxes'], colores_plot):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)
        
        ax.set_title('Distribución de Intensidad por Emoción', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_ylabel('Porcentaje (%)', fontsize=12)
        ax.set_xlabel('Emoción', fontsize=12)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if guardar:
            ruta = self.dir_salida / archivo
            plt.savefig(ruta, dpi=300, bbox_inches='tight')
            print(f"✅ Intensidad guardada: {ruta}")
        
        return fig, ax
    
    def dias_mas_intensos(self, df: pd.DataFrame, top_n: int = 10,
                         guardar: bool = True,
                         archivo: str = "dias_mas_intensos.png"):
        """
        Top N días más intensos (con mayor polarización emocional)
        
        Args:
            df: DataFrame con resumen diario
            top_n: Número de días a mostrar
            guardar: Si True, guarda el gráfico
            archivo: Nombre del archivo de salida
        """
        df = df.copy()
        df['fecha'] = pd.to_datetime(df['fecha'])
        
        # Ordenar por intensidad
        top_dias = df.nlargest(top_n, 'intensidad')
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Crear barras
        colores = [COLORES_EMOCIONES.get(e, '#808080') 
                  for e in top_dias['ganador_del_dia']]
        
        fechas_str = top_dias['fecha'].dt.strftime('%Y-%m-%d')
        
        bars = ax.barh(range(len(top_dias)), top_dias['intensidad'], 
                       color=colores, edgecolor='black')
        
        ax.set_yticks(range(len(top_dias)))
        ax.set_yticklabels(fechas_str)
        ax.set_xlabel('Intensidad (%)', fontsize=12, fontweight='bold')
        ax.set_title(f'Top {top_n} Días con Mayor Intensidad Emocional',
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3)
        
        # Agregar etiquetas de emoción
        for i, (idx, row) in enumerate(top_dias.iterrows()):
            ax.text(row['intensidad'] + 1, i, 
                   f"{row['ganador_del_dia'].capitalize()} ({row['n_total']} tweets)",
                   va='center', fontsize=9)
        
        plt.tight_layout()
        
        if guardar:
            ruta = self.dir_salida / archivo
            plt.savefig(ruta, dpi=300, bbox_inches='tight')
            print(f"✅ Días más intensos guardado: {ruta}")
        
        return fig, ax
    
    def evolucion_mensual(self, df: pd.DataFrame,
                         guardar: bool = True,
                         archivo: str = "evolucion_mensual.png"):
        """
        Evolución agregada por mes
        
        Args:
            df: DataFrame con resumen diario
            guardar: Si True, guarda el gráfico
            archivo: Nombre del archivo de salida
        """
        df = df.copy()
        df['fecha'] = pd.to_datetime(df['fecha'])
        df['año_mes'] = df['fecha'].dt.to_period('M')
        
        # Agregar por mes
        emociones = ['alegria', 'tristeza', 'ira', 'miedo', 'sorpresa']
        
        mensuales = []
        for año_mes, grupo in df.groupby('año_mes'):
            registro = {'año_mes': str(año_mes)}
            for emocion in emociones:
                col = f'pct_{emocion}'
                registro[emocion] = grupo[col].mean()
            mensuales.append(registro)
        
        df_mensual = pd.DataFrame(mensuales)
        
        fig, ax = plt.subplots(figsize=(16, 8))
        
        x = range(len(df_mensual))
        width = 0.15
        
        for i, emocion in enumerate(emociones):
            offset = (i - 2) * width
            ax.bar([p + offset for p in x], df_mensual[emocion],
                  width=width, label=emocion.capitalize(),
                  color=COLORES_EMOCIONES[emocion], alpha=0.8)
        
        ax.set_xticks(x)
        ax.set_xticklabels(df_mensual['año_mes'], rotation=45, ha='right')
        ax.set_xlabel('Mes', fontsize=12, fontweight='bold')
        ax.set_ylabel('Porcentaje promedio (%)', fontsize=12, fontweight='bold')
        ax.set_title('Evolución Mensual de Emociones',
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper left')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if guardar:
            ruta = self.dir_salida / archivo
            plt.savefig(ruta, dpi=300, bbox_inches='tight')
            print(f"✅ Evolución mensual guardada: {ruta}")
        
        return fig, ax
    
    def dashboard_completo(self, df: pd.DataFrame,
                          guardar: bool = True,
                          archivo: str = "dashboard_completo.png"):
        """
        Dashboard completo con múltiples visualizaciones
        
        Args:
            df: DataFrame con resumen diario
            guardar: Si True, guarda el gráfico
            archivo: Nombre del archivo de salida
        """
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        df = df.copy()
        df['fecha'] = pd.to_datetime(df['fecha'])
        df = df.sort_values('fecha')
        
        # 1. Serie temporal (ocupa 2 columnas)
        ax1 = fig.add_subplot(gs[0, :2])
        emociones = ['alegria', 'tristeza', 'ira', 'miedo', 'sorpresa']
        for emocion in emociones:
            col = f'pct_{emocion}'
            if col in df.columns:
                ax1.plot(df['fecha'], df[col], label=emocion.capitalize(),
                        color=COLORES_EMOCIONES[emocion], linewidth=2)
        ax1.set_title('Serie Temporal de Emociones', fontweight='bold')
        ax1.legend(loc='upper left', fontsize=8)
        ax1.grid(alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. Distribución de ganadores (pie)
        ax2 = fig.add_subplot(gs[0, 2])
        ganadores = df['ganador_del_dia'].value_counts()
        colores = [COLORES_EMOCIONES.get(e, '#808080') for e in ganadores.index]
        ax2.pie(ganadores.values, labels=ganadores.index, autopct='%1.1f%%',
               colors=colores, textprops={'fontsize': 8})
        ax2.set_title('Distribución de Días', fontweight='bold')
        
        # 3. Box plots (ocupa 2 columnas)
        ax3 = fig.add_subplot(gs[1, :2])
        datos_plot = []
        labels_plot = []
        colores_plot = []
        for emocion in emociones:
            col = f'pct_{emocion}'
            if col in df.columns:
                datos_plot.append(df[col].dropna())
                labels_plot.append(emocion.capitalize())
                colores_plot.append(COLORES_EMOCIONES[emocion])
        bp = ax3.boxplot(datos_plot, labels=labels_plot, patch_artist=True)
        for patch, color in zip(bp['boxes'], colores_plot):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)
        ax3.set_title('Distribución de Intensidades', fontweight='bold')
        ax3.grid(axis='y', alpha=0.3)
        
        # 4. Top 5 días intensos
        ax4 = fig.add_subplot(gs[1, 2])
        top_5 = df.nlargest(5, 'intensidad')
        colores_top = [COLORES_EMOCIONES.get(e, '#808080') 
                      for e in top_5['ganador_del_dia']]
        fechas_str = top_5['fecha'].dt.strftime('%m-%d')
        ax4.barh(range(len(top_5)), top_5['intensidad'], color=colores_top)
        ax4.set_yticks(range(len(top_5)))
        ax4.set_yticklabels(fechas_str, fontsize=8)
        ax4.set_title('Top 5 Días Intensos', fontweight='bold')
        ax4.grid(axis='x', alpha=0.3)
        
        # 5. Tweets por día (línea)
        ax5 = fig.add_subplot(gs[2, :])
        ax5.plot(df['fecha'], df['n_total'], color='steelblue', linewidth=1.5)
        ax5.fill_between(df['fecha'], df['n_total'], alpha=0.3, color='steelblue')
        ax5.set_title('Volumen de Tweets por Día', fontweight='bold')
        ax5.set_ylabel('Número de tweets')
        ax5.grid(alpha=0.3)
        ax5.tick_params(axis='x', rotation=45)
        
        # Título general
        fig.suptitle('Dashboard de Análisis de Emociones - Tweets sobre Culiacán',
                    fontsize=16, fontweight='bold', y=0.995)
        
        if guardar:
            ruta = self.dir_salida / archivo
            plt.savefig(ruta, dpi=300, bbox_inches='tight')
            print(f"✅ Dashboard guardado: {ruta}")
        
        return fig


def crear_visualizaciones(df_diario: pd.DataFrame, 
                         dir_salida: str = "data_tweets_culiacan/visualizaciones"):
    """
    Función de conveniencia para crear todas las visualizaciones
    
    Args:
        df_diario: DataFrame con resumen diario
        dir_salida: Directorio donde guardar las visualizaciones
    """
    print("\n" + "=" * 60)
    print("GENERANDO VISUALIZACIONES")
    print("=" * 60 + "\n")
    
    viz = VisualizadorEmociones(dir_salida)
    
    # Generar todas las visualizaciones
    viz.serie_temporal_porcentajes(df_diario)
    viz.calendario_emociones(df_diario)
    viz.distribucion_anual(df_diario)
    viz.intensidad_por_emocion(df_diario)
    viz.dias_mas_intensos(df_diario)
    viz.evolucion_mensual(df_diario)
    viz.dashboard_completo(df_diario)
    
    print("\n" + "=" * 60)
    print(f"✅ VISUALIZACIONES COMPLETADAS")
    print(f"📁 Ubicación: {dir_salida}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    # Ejemplo de uso
    print("""
    Para usar el visualizador:
    
    1. Desde el pipeline completo:
        from tweets_sentiments_test import TweetsEmotionAnalyzer
        analyzer = TweetsEmotionAnalyzer()
        resultados = analyzer.pipeline_completo()
        crear_visualizaciones(resultados['diario'])
    
    2. Desde archivo CSV existente:
        import pandas as pd
        df = pd.read_csv('data_tweets_culiacan/resultados/resumen_diario.csv')
        crear_visualizaciones(df)
    """)
