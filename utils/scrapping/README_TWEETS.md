# Sistema de Análisis de Emociones en Tweets sobre Culiacán

Este módulo permite analizar emociones en tweets históricos relacionados con Culiacán, clasificándolos en 5 categorías emocionales principales: **alegría, tristeza, ira, miedo y sorpresa** (+ neutral).

## 🎯 Características

- ✅ Recolección automatizada de tweets históricos
- ✅ Clasificación de emociones usando modelos de NLP (pysentimiento)
- ✅ Análisis temporal diario, mensual y anual
- ✅ Visualizaciones profesionales
- ✅ Exportación de datos para integración con modelos predictivos

## 📦 Instalación

### 1. Instalar dependencias

```powershell
pip install -r requirements_tweets.txt
```

### 2. Verificar instalación de snscrape

```powershell
snscrape --version
```

Si hay problemas, instala manualmente:
```powershell
pip install snscrape --upgrade
```

## 🚀 Uso Rápido

### Opción 1: Menú Interactivo (Recomendado)

```powershell
python ejemplo_uso_completo.py
```

Esto abre un menú donde puedes:
1. Generar script de recolección
2. Procesar tweets
3. Generar visualizaciones
4. Análisis personalizados

### Opción 2: Código Python

```python
from tweets_sentiments_test import TweetsEmotionAnalyzer
from visualizador_emociones import crear_visualizaciones

# 1. Crear analizador
analyzer = TweetsEmotionAnalyzer()

# 2. Generar script de recolección
analyzer.generar_script_recoleccion("recolectar.ps1")

# 3. Ejecutar el script en PowerShell
# .\recolectar.ps1

# 4. Procesar tweets
resultados = analyzer.pipeline_completo()

# 5. Generar visualizaciones
crear_visualizaciones(resultados['diario'])
```

## 📋 Flujo de Trabajo Completo

### Paso 1: Configurar Parámetros

Edita `config_tweets.py` para ajustar:
- Fechas de inicio/fin
- Palabras clave de búsqueda
- Filtros (retweets, replies, etc.)
- Parámetros del modelo

### Paso 2: Generar Script de Recolección

```python
from tweets_sentiments_test import TweetsEmotionAnalyzer

analyzer = TweetsEmotionAnalyzer()
script = analyzer.generar_script_recoleccion("recolectar_tweets.ps1")
print(f"Script generado: {script}")
```

Esto genera un archivo `.ps1` con comandos snscrape para cada día.

### Paso 3: Recolectar Tweets

Ejecuta el script generado:

```powershell
.\recolectar_tweets.ps1
```

⏱️ **Tiempo estimado**: 
- 1 mes: ~30 minutos
- 1 año: 4-6 horas

Los tweets se guardan en: `data_tweets_culiacan/raw/`

### Paso 4: Procesar y Clasificar

```python
# Procesar todos los tweets recolectados
resultados = analyzer.pipeline_completo(desde_raw=True)

# Ver resumen
from tweets_sentiments_test import mostrar_resumen_rapido
mostrar_resumen_rapido(resultados['analisis'])
```

Esto:
1. Carga y limpia los tweets
2. Clasifica emociones usando IA
3. Agrega datos por día
4. Genera análisis anual

### Paso 5: Generar Visualizaciones

```python
from visualizador_emociones import crear_visualizaciones

crear_visualizaciones(resultados['diario'])
```

Genera 7 visualizaciones:
- Serie temporal de emociones
- Calendario de emociones (heatmap)
- Distribución anual (barras + pie)
- Box plots de intensidad
- Top días más intensos
- Evolución mensual
- Dashboard completo

## 📊 Estructura de Datos

### Tweets Clasificados (`tweets_clasificados_XXXXXX.csv`)

| Columna | Descripción |
|---------|-------------|
| `date` | Fecha y hora del tweet (UTC) |
| `content` | Texto del tweet |
| `fecha` | Fecha local (America/Mazatlan) |
| `hora` | Hora del día |
| `emocion` | Emoción clasificada |
| `username` | Usuario (si disponible) |

### Resumen Diario (`resumen_diario_XXXXXX.csv`)

| Columna | Descripción |
|---------|-------------|
| `fecha` | Fecha |
| `alegria` | Número de tweets con alegría |
| `tristeza` | Número de tweets con tristeza |
| `ira` | Número de tweets con ira |
| `miedo` | Número de tweets con miedo |
| `sorpresa` | Número de tweets con sorpresa |
| `neutral` | Número de tweets neutrales |
| `n_total` | Total de tweets del día |
| `pct_alegria` | Porcentaje de alegría |
| `pct_tristeza` | Porcentaje de tristeza |
| `pct_ira` | Porcentaje de ira |
| `pct_miedo` | Porcentaje de miedo |
| `pct_sorpresa` | Porcentaje de sorpresa |
| `pct_neutral` | Porcentaje de neutral |
| `ganador_del_dia` | Emoción dominante |
| `intensidad` | Porcentaje de la emoción ganadora |

### Análisis Anual (`analisis_anual_XXXXXX.json`)

Contiene:
- Período analizado
- Total de tweets
- Emoción anual (moda)
- Distribución de ganadores
- Promedios porcentuales
- Top días más emotivos
- Estadísticas por emoción

## 🎨 Personalización

### Cambiar Período de Análisis

En `config_tweets.py`:
```python
ANIO_INICIO = "2024-01-01"
ANIO_FIN = "2024-12-31"
```

### Agregar Palabras Clave

```python
PALABRAS_CLAVE = [
    "Culiacán",
    "Culiacan",
    "#Culiacán",
    "Dorados",
    "CUL",  # Aeropuerto
    # Agrega más...
]
```

### Ajustar Filtros

```python
EXCLUIR_RETWEETS = True      # Excluir RT
EXCLUIR_REPLIES = True       # Excluir respuestas
MAX_TWEETS_POR_USUARIO_DIA = 20  # Anti-bots
```

### Personalizar Análisis

```python
# Cambiar si neutral puede ser ganador
INCLUIR_NEUTRAL_COMO_GANADOR = False

# Cambiar mapeo de emociones
MAPEO_EMOCIONES = {
    "joy": "alegria",
    "sadness": "tristeza",
    # Personaliza según necesites
}
```

## 🔧 Solución de Problemas

### Error: "snscrape not found"

```powershell
pip uninstall snscrape
pip install git+https://github.com/JustAnotherArchivist/snscrape.git
```

### Error: "pysentimiento model download failed"

Primera vez descarga el modelo (~500MB):
```python
from pysentimiento import create_analyzer
analyzer = create_analyzer(task="emotion", lang="es")
# Espera la descarga...
```

### Tweets vacíos o pocos resultados

- Verifica las palabras clave
- Ajusta el rango de fechas
- Revisa filtros (quizá muy restrictivos)
- Twitter/X limita scraping; espaciar requests

### Memoria insuficiente

Para datasets grandes (>1M tweets):
```python
# Procesar por lotes
analyzer.clasificar_tweets(df, batch_size=16)  # Reducir batch
```

## 📈 Integración con Modelo de Predicción

Para usar las emociones como features en tu modelo de homicidios:

```python
import pandas as pd

# 1. Cargar resumen diario
df_emociones = pd.read_csv('data_tweets_culiacan/resultados/resumen_diario.csv')

# 2. Cargar datos de homicidios
df_homicidios = pd.read_csv('datos/homicidios.csv')
df_homicidios['fecha'] = pd.to_datetime(df_homicidios['fecha'])

# 3. Merge por fecha
df_merged = df_homicidios.merge(
    df_emociones[['fecha', 'pct_alegria', 'pct_tristeza', 'pct_ira', 
                  'pct_miedo', 'pct_sorpresa', 'ganador_del_dia']],
    on='fecha',
    how='left'
)

# 4. Codificar emoción del día
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df_merged['emocion_codigo'] = le.fit_transform(df_merged['ganador_del_dia'].fillna('neutral'))

# 5. Usar en tu modelo
features = ['pct_alegria', 'pct_tristeza', 'pct_ira', 'pct_miedo', 
            'pct_sorpresa', 'emocion_codigo']
```

## 📚 Referencias

- **pysentimiento**: https://github.com/pysentimiento/pysentimiento
- **snscrape**: https://github.com/JustAnotherArchivist/snscrape
- **Modelo de emociones**: Basado en BERT multilingüe fine-tuned para español

## ⚖️ Consideraciones Éticas

- ✅ Solo agregar datos, NO publicar tweets individuales
- ✅ Respetar términos de servicio de Twitter/X
- ✅ No hacer conclusiones causales directas
- ✅ Reconocer sesgo de muestra (usuarios de Twitter ≠ población general)
- ✅ Usar solo para investigación/análisis académico

## 🤝 Contribuir

Para mejorar el sistema:

1. Optimizar filtros de spam
2. Agregar más fuentes (Facebook, noticias)
3. Mejorar mapeo de emociones
4. Validar contra eventos conocidos

## 📞 Soporte

Para problemas o preguntas:
1. Revisa esta documentación
2. Ejecuta `ejemplo_uso_completo.py` (opción 2) para diagnóstico
3. Verifica logs en `tweets_emotion_analysis.log`

---

**Versión**: 1.0
**Última actualización**: 2025-10-04
**Autor**: Carlos
