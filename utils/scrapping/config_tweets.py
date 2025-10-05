"""
Configuración para análisis de emociones en tweets sobre Culiacán
"""
from datetime import datetime

# === CONFIGURACIÓN TEMPORAL ===
ANIO_INICIO = "2024-09-01"  # Fecha inicio (inclusive)
ANIO_FIN = "2025-09-30"      # Fecha fin (inclusive)
ZONA_HORARIA = "America/Mazatlan"

# === CONFIGURACIÓN DE BÚSQUEDA ===
PALABRAS_CLAVE = [
    "Culiacan",
    "Culiacán",
    "Culiacan Sinaloa"
]

# Cuentas locales importantes (opcional, para filtrado adicional)
CUENTAS_LOCALES = [
    "@RioDoce_mx",
    "@noroeste",
    "@linea_directa",
    # Agrega más según necesites
]

# === CONFIGURACIÓN DE SCRAPING ===
EXCLUIR_RETWEETS = True
EXCLUIR_REPLIES = False  # False para incluir respuestas
SOLO_VERIFICADOS = False  # True si solo quieres cuentas verificadas
IDIOMA = "es"

# === CONFIGURACIÓN DE EMOCIONES ===
# Si True, incluye "neutral" como ganador posible del día
# Si False, neutral se cuenta pero el ganador siempre es una de las 5 emociones
INCLUIR_NEUTRAL_COMO_GANADOR = False

# Emociones principales (5 categorías)
EMOCIONES_PRINCIPALES = ["alegria", "tristeza", "ira", "miedo", "sorpresa"]

# Mapeo de etiquetas del modelo a nuestras 5 categorías
MAPEO_EMOCIONES = {
    "joy": "alegria",
    "alegría": "alegria",
    "alegria": "alegria",
    "happiness": "alegria",
    "sadness": "tristeza",
    "tristeza": "tristeza",
    "anger": "ira",
    "enojo": "ira",
    "ira": "ira",
    "disgust": "ira",  # Agrupamos asco con ira
    "asco": "ira",
    "fear": "miedo",
    "miedo": "miedo",
    "surprise": "sorpresa",
    "sorpresa": "sorpresa",
    "others": "neutral",
    "neutral": "neutral",
    "other": "neutral"
}

# === CONFIGURACIÓN DE ARCHIVOS ===
DIR_DATOS_RAW = "data_tweets_culiacan/raw"
DIR_DATOS_PROCESADOS = "data_tweets_culiacan/procesados"
DIR_RESULTADOS = "data_tweets_culiacan/resultados"
DIR_VISUALIZACIONES = "data_tweets_culiacan/visualizaciones"

# === CONFIGURACIÓN DE FILTROS ===
# Palabras que indican contenido no útil
PALABRAS_SPAM = ["sorteo", "concurso", "gana", "premio", "sigueme"]

# Mínimo de caracteres para considerar un tweet válido
MIN_CARACTERES = 10

# Máximo de tweets por usuario por día (para filtrar bots)
MAX_TWEETS_POR_USUARIO_DIA = 20

# === CONFIGURACIÓN DEL MODELO ===
MODELO_EMOCION = "emotion"  # Para pysentimiento
MODELO_LANG = "es"
BATCH_SIZE = 32  # Para procesamiento por lotes

# === CONFIGURACIÓN DE LOGGING ===
LOG_LEVEL = "INFO"
LOG_FILE = "tweets_emotion_analysis.log"
