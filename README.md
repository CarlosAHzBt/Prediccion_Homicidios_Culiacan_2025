# Predicción de Homicidios Diarios en Culiacán

## 📋 Descripción del Proyecto

Proyecto de ciencia de datos para analizar y predecir homicidios diarios en Culiacán, Sinaloa. Incluye recopilación de datos, ingeniería de características, experimentación con modelos de machine learning y visualizaciones.

**Estado del proyecto**: En desarrollo activo. Es un proyecto secundario personal que se avanza lentamente, por lo que puede tener algunos bugs y áreas por mejorar.

## ⚠️ Notas Importantes sobre el Desarrollo

- **Fuente de datos de homicidios**: Los datos de homicidios se obtienen a partir de los reportes publicados por "El Noroeste", un portal de noticias de Culiacán que publica diariamente el número de homicidios.
- **Proyecto en desarrollo**: No es una solución final o producción-ready. Se trata de un análisis exploratorio que evoluciona con el tiempo.
- **Variables utilizadas**: Las características incluidas no son necesariamente las óptimas. Gran parte del código fue "vibe-coded" (desarrollado con intuición y experimentación rápida), lo que significa que algunas decisiones técnicas podrían no seguir las mejores prácticas.
- **Fortalezas**: La selección de características, las visualizaciones y las predicciones son aspectos sólidos y útiles del proyecto.
- **Limitaciones**: Puede contener bugs menores, especialmente en la automatización y manejo de errores. Se recomienda revisar los resultados y validar antes de usar en contextos críticos.

## 📁 Estructura del Proyecto

### 🔧 Archivos Principales

- **`main.py`**: Script principal que ejecuta el pipeline completo para actualizar los datos. Recopila y procesa información de homicidios, robos, clima, dólar y calendario.
- **`tests/experimentacion_modelos.ipynb`**: Notebook principal para análisis exploratorio, ingeniería de características, experimentación con modelos de ML y visualizaciones.

### 📊 Datos

- **`Dataset_homicidios_Actualizado.csv`**: Dataset principal con todas las variables fusionadas (homicidios, clima, dólar, fechas, etc.).
- **`datos/`**: Carpeta con datasets intermedios procesados:
  - `homicidios.csv`: Datos de homicidios.
  - `robos.csv`: Datos de robos de vehículos.
  - `clima.csv`: Datos climáticos.
  - `dolar.csv`: Precios del dólar.
  - `calendario.csv`: Información de calendario y días especiales.
  - `culiacan_calendar_cleaned.csv`: Calendario limpio.
  - `feature_importance_corrected.csv`: Importancia de características del modelo.

### 🔧 Utilidades

- **`utils/`**: Scripts modulares para recopilar datos:
  - `get_homicidios.py`: Obtiene datos de homicidios.
  - `get_robos.py`: Obtiene datos de robos.
  - `get_clima.py`: Obtiene datos climáticos.
  - `get_dolar.py`: Obtiene precios del dólar.
  - `get_dias_pago.py`: Genera calendario con días de pago y festivos.
  - `merge_data.py`: Fusiona todos los datasets en el principal.

### 🤖 Modelos

- **`modelos/`**: Modelos entrenados y guardados:
  - `homicidios_predictor_*.joblib`: Modelos de predicción.
  - `scaler_*.joblib`: Escaladores para normalización.
  - `model_info_*.json`: Metadatos de los modelos.

### 📦 Otros

- **`requirements.txt`**: Dependencias de Python necesarias.
- **`.venv/`**: Entorno virtual (no incluir en control de versiones).

## 🚀 Cómo Usar el Proyecto

### Flujo de Trabajo Típico

Cada vez que quieres ejecutar el código:

1. **Actualizar datos**: Ejecuta `main.py` para recopilar y procesar los datos más recientes. Esto actualiza los CSVs en `datos/` y genera `Dataset_homicidios_Actualizado.csv`.

   ```bash
   python main.py
   ```
2. **Análisis y modelado**: Abre `tests/experimentacion_modelos.ipynb` y ejecuta todas las celdas. Esto incluye:

   - Carga de datos.
   - Exploración y visualizaciones.
   - Ingeniería de características.
   - Entrenamiento y evaluación de modelos.
   - Predicciones.

### Requisitos Previos

- Python 3.8+
- Instalar dependencias: `pip install -r requirements.txt`
- Navegador Chrome (para scraping con Selenium en algunos scripts).

### Actualización de Datos

- Ejecuta `main.py` regularmente para mantener los datos al día.
- Los scripts en `utils/` pueden ejecutarse individualmente si necesitas actualizar solo una fuente de datos.

## 🎯 Características Técnicas

- **Fuentes de datos**: Homicidios, robos, clima, precios del dólar, calendario.
- **Modelos probados**: Regresión lineal, Random Forest, XGBoost, LightGBM, etc.
- **Métricas**: MAE, RMSE, R², MAPE.
- **Visualizaciones**: Gráficos de tendencias, importancia de features, predicciones.

## 📧 Contacto y Contribuciones

Proyecto personal para análisis de datos. Si encuentras bugs o tienes sugerencias, siéntete libre de contribuir o reportar issues.

---

**Última actualización**: Septiembre 2025
**Versión**: En desarrollo
