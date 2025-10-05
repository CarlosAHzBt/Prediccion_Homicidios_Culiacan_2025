# 🚀 Guía de Inicio Rápido - Sistema de Análisis de Emociones en Tweets

## 📖 ¿Qué es esto?

Un sistema completo para analizar emociones en tweets sobre Culiacán. Clasifica cada tweet en **5 categorías emocionales** (alegría, tristeza, ira, miedo, sorpresa) y determina el "sentimiento del día" para análisis temporal.

## ⚡ Instalación Rápida (5 minutos)

### Opción A: Script Automático (Windows)

```powershell
cd utils\scrapping
.\setup_sistema_tweets.ps1
```

### Opción B: Manual

```powershell
# 1. Instalar dependencias
pip install -r utils/scrapping/requirements_tweets.txt

# 2. Descargar modelo de IA
python -c "from pysentimiento import create_analyzer; create_analyzer(task='emotion', lang='es')"

# 3. Crear directorios
mkdir data_tweets_culiacan\raw
mkdir data_tweets_culiacan\resultados
mkdir data_tweets_culiacan\visualizaciones
```

## 📊 Flujo de Trabajo Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                     FLUJO DE TRABAJO                            │
└─────────────────────────────────────────────────────────────────┘

1️⃣  CONFIGURAR
    │
    ├─► Editar config_tweets.py (opcional)
    │   • Ajustar fechas (ANIO_INICIO, ANIO_FIN)
    │   • Modificar palabras clave
    │   • Personalizar filtros
    │
    └─► python ejemplo_uso_completo.py
        Seleccionar opción 1: "Generar script de recolección"
        → Crea: recolectar_tweets_culiacan.ps1

2️⃣  RECOLECTAR TWEETS
    │
    └─► .\recolectar_tweets_culiacan.ps1
        • Descarga tweets día por día
        • Guarda en: data_tweets_culiacan/raw/
        • Tiempo: ~4-6 horas para 1 año
        • Puedes pausar y reanudar

3️⃣  PROCESAR Y CLASIFICAR
    │
    └─► python ejemplo_uso_completo.py
        Seleccionar opción 3: "Procesar tweets"
        │
        ├─► Limpia tweets (spam, duplicados, bots)
        ├─► Clasifica emociones con IA
        ├─► Agrega por día
        └─► Genera análisis anual
        
        Guarda en: data_tweets_culiacan/resultados/
        • tweets_clasificados_XXXXXX.csv
        • resumen_diario_XXXXXX.csv
        • analisis_anual_XXXXXX.json
        • reporte_XXXXXX.txt

4️⃣  VISUALIZAR
    │
    └─► python ejemplo_uso_completo.py
        Seleccionar opción 4: "Generar visualizaciones"
        
        Crea 7 gráficos:
        • serie_temporal_emociones.png
        • calendario_emociones.png
        • distribucion_anual.png
        • intensidad_emociones.png
        • dias_mas_intensos.png
        • evolucion_mensual.png
        • dashboard_completo.png

5️⃣  INTEGRAR CON TU MODELO
    │
    └─► Ver ejemplo en README_TWEETS.md
        Merge con dataset de homicidios
```

## 🎯 Casos de Uso Rápidos

### Caso 1: Probar con 1 semana de datos

```powershell
# Generar datos sintéticos de prueba
python -c "from utils.scrapping.test_sistema import generar_datos_prueba, guardar_datos_prueba; df = generar_datos_prueba(7, 50); guardar_datos_prueba(df)"

# Procesar
python utils\scrapping\ejemplo_uso_completo.py
# Opción 3 → procesar
# Opción 4 → visualizar
```

### Caso 2: Solo recolectar 1 mes

Edita `config_tweets.py`:
```python
ANIO_INICIO = "2025-01-01"
ANIO_FIN = "2025-01-31"
```

Luego ejecuta pasos 1-4 normales.

### Caso 3: Análisis de un día específico

```python
from tweets_sentiments_test import TweetsEmotionAnalyzer

analyzer = TweetsEmotionAnalyzer()
comando = analyzer.generar_comando_snscrape("2025-10-04")
print(comando)
# Ejecuta el comando en PowerShell
```

### Caso 4: Re-analizar datos existentes

```python
import pandas as pd
from visualizador_emociones import crear_visualizaciones

# Cargar resumen existente
df = pd.read_csv('data_tweets_culiacan/resultados/resumen_diario_20251004_123456.csv')

# Regenerar visualizaciones
crear_visualizaciones(df)
```

## 📁 Estructura de Archivos Generados

```
data_tweets_culiacan/
├── raw/                          # Tweets originales (JSONL)
│   ├── tweets_2024-10-01.jsonl
│   ├── tweets_2024-10-02.jsonl
│   └── ...
│
├── resultados/                   # Datos procesados
│   ├── tweets_clasificados_20251004_120000.csv
│   ├── resumen_diario_20251004_120000.csv
│   ├── analisis_anual_20251004_120000.json
│   └── reporte_20251004_120000.txt
│
└── visualizaciones/              # Gráficos
    ├── serie_temporal_emociones.png
    ├── calendario_emociones.png
    ├── distribucion_anual.png
    ├── intensidad_emociones.png
    ├── dias_mas_intensos.png
    ├── evolucion_mensual.png
    └── dashboard_completo.png
```

## 🔧 Comandos Útiles

### Ver resumen de resultados

```powershell
# Ver reporte en texto
cat data_tweets_culiacan\resultados\reporte_*.txt

# Ver JSON
cat data_tweets_culiacan\resultados\analisis_anual_*.json
```

### Ejecutar tests

```powershell
python utils\scrapping\test_sistema.py
# Opción 5: "Ejecutar todos los tests"
```

### Ver logs

```powershell
cat tweets_emotion_analysis.log
```

### Limpiar datos de prueba

```powershell
Remove-Item data_tweets_culiacan\test -Recurse -Force
```

## 🆘 Solución de Problemas

### Error: "snscrape not found"

```powershell
pip uninstall snscrape
pip install git+https://github.com/JustAnotherArchivist/snscrape.git
```

### Error: "pysentimiento model download failed"

```powershell
python -c "from pysentimiento import create_analyzer; create_analyzer(task='emotion', lang='es')"
# Espera la descarga (~500MB)
```

### Pocos resultados o tweets vacíos

1. Verifica palabras clave en `config_tweets.py`
2. Ajusta filtros (quizá muy restrictivos)
3. Twitter/X limita scraping - espaciar requests

### Memoria insuficiente (>1M tweets)

```python
# Reducir batch_size
analyzer.clasificar_tweets(df, batch_size=16)
```

## 📚 Ejemplos de Código

### Análisis Personalizado

```python
import pandas as pd

# Cargar datos
df = pd.read_csv('data_tweets_culiacan/resultados/resumen_diario_*.csv')
df['fecha'] = pd.to_datetime(df['fecha'])

# Emoción por día de la semana
df['dia_semana'] = df['fecha'].dt.day_name()
por_dia = df.groupby('dia_semana')['ganador_del_dia'].agg(lambda x: x.mode()[0])
print(por_dia)

# Racha más larga de una emoción
df_sorted = df.sort_values('fecha')
# ... (ver ejemplo_uso_completo.py, opción 5)
```

### Integrar con Modelo de Homicidios

```python
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Cargar ambos datasets
df_emociones = pd.read_csv('data_tweets_culiacan/resultados/resumen_diario_*.csv')
df_homicidios = pd.read_csv('datos/homicidios.csv')

# Merge
df_merged = df_homicidios.merge(
    df_emociones[['fecha', 'pct_alegria', 'pct_tristeza', 'pct_ira', 
                  'pct_miedo', 'pct_sorpresa', 'ganador_del_dia']],
    on='fecha',
    how='left'
)

# Codificar emoción
le = LabelEncoder()
df_merged['emocion_codigo'] = le.fit_transform(df_merged['ganador_del_dia'].fillna('neutral'))

# Usar en modelo
features = ['pct_alegria', 'pct_tristeza', 'pct_ira', 'pct_miedo', 
            'pct_sorpresa', 'emocion_codigo', ... otras features]
```

## 📊 Interpretación de Resultados

### Resumen Diario (CSV)

| Columna | Descripción | Rango |
|---------|-------------|-------|
| `fecha` | Fecha del análisis | - |
| `n_total` | Total de tweets del día | 0-∞ |
| `pct_alegria` | % de tweets alegres | 0-100 |
| `ganador_del_dia` | Emoción dominante | alegria/tristeza/ira/miedo/sorpresa |
| `intensidad` | % de la emoción ganadora | 0-100 |

### Análisis Anual (JSON)

```json
{
  "emocion_anual_moda": "ira",          // Emoción más frecuente
  "tweets_totales": 123456,             // Total de tweets
  "distribucion_ganadores": {           // Días ganados por emoción
    "ira": 150,
    "tristeza": 100,
    ...
  },
  "dias_mas_emotivos": {                // Top días por emoción
    "ira": [
      {
        "fecha": "2025-03-15",
        "intensidad": 75.5,
        "tweets": 1234
      },
      ...
    ]
  }
}
```

## ⚖️ Consideraciones Éticas

✅ **Solo publicar agregados**, NO tweets individuales
✅ **Respetar términos de servicio** de Twitter/X
✅ **No hacer conclusiones causales** directas
✅ **Reconocer sesgo**: usuarios de Twitter ≠ población general
✅ **Uso académico/investigación** únicamente

## 🎓 Referencias y Recursos

- **pysentimiento**: https://github.com/pysentimiento/pysentimiento
- **snscrape**: https://github.com/JustAnotherArchivist/snscrape
- **Documentación completa**: `README_TWEETS.md`
- **Paper del modelo**: RoBERTuito (BERT para español)

## 💡 Tips Pro

1. **Ejecuta primero con 1 semana** para familiarizarte
2. **Revisa logs** para detectar problemas temprano
3. **Guarda scripts personalizados** en `ejemplo_uso_completo.py`
4. **Haz backup** de `data_tweets_culiacan/` regularmente
5. **Valida resultados** contra eventos conocidos

---

**¿Dudas?** Lee [`README_TWEETS.md`](README_TWEETS.md) o ejecuta `test_sistema.py` para diagnóstico.

**Versión**: 1.0 | **Fecha**: 2025-10-04
