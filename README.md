# ENTREGABLES FINALES - ANÁLISIS DE HOMICIDIOS EN CULIACÁN

## 📋 DESCRIPCIÓN DEL PROYECTO
Análisis completo de homicidios en Culiacán con datos corregidos (sin fechas futuras).
Proyecto de ciencia de datos que incluye limpieza, análisis estadístico, modelado y visualizaciones.

## 📅 INFORMACIÓN DEL ANÁLISIS
- **Fecha de análisis**: 09/07/2025
- **Período de datos**: 01/01/2025 - 08/07/2025 (solo datos históricos)
- **Total de registros**: 303 días
- **Total de homicidios**: 1,685 casos

## 📁 ESTRUCTURA DE ARCHIVOS

### 📊 `/datos`
- **culiacan_calendar_cleaned.csv**: Dataset principal limpio sin fechas futuras
- **feature_importance_corrected.csv**: Importancia de variables del modelo
- **homicidios.csv**: Datos originales de homicidios extraídos
- **robos.csv**: Datos originales de robos de vehículos

### 📋 `/reportes`
- **resumen_ejecutivo.txt**: Resumen ejecutivo para tomadores de decisiones
- **reporte_final_consolidado.txt**: Reporte técnico completo del proyecto
- **analisis_corregido_final.txt**: Análisis estadístico detallado

### 📊 `/visualizaciones`
- **analisis_corregido_final.png**: Gráficos principales del análisis
- **estadisticas_finales_corregidas.png**: Estadísticas visuales y tendencias

### 🔧 `/scripts`
- **get_homicides.py**: Script de web scraping para obtener datos de Flourish
- **precio_dolar.py**: Script para obtener precios del dólar desde Yahoo Finance
- **corrected_analysis.py**: Script principal de análisis sin fechas futuras
- **update_all_data.py**: Script para actualizar variables del dataset
- **create_final_summary.py**: Script para generar resúmenes ejecutivos
- **final_corrected_viz.py**: Script para crear visualizaciones corregidas

### 📓 **NOTEBOOK DE AUTOMATIZACIÓN**
- **automatizacion_datos_completa.ipynb**: Notebook completo que agrupa todos los scripts de obtención y actualización de datos

## 🎯 CARACTERÍSTICAS TÉCNICAS
- ✅ **Datos validados**: Sin fechas futuras, solo información histórica
- ✅ **Variables incluidas**: Climáticas, económicas, temporales y booleanas
- ✅ **Modelado**: Regresión lineal con análisis de importancia de features
- ✅ **Calidad**: Datos limpios, consistentes y documentados

## 🚀 CÓMO USAR ESTOS ARCHIVOS

### Para Obtener Datos Actualizados:
1. **Usar el Notebook**: Abrir `automatizacion_datos_completa.ipynb` y ejecutar todas las celdas
2. **Scripts individuales**: 
   - Ejecutar `get_homicides.py` para datos de homicidios y robos
   - Ejecutar `precio_dolar.py` para precios del dólar
   - Ejecutar `update_all_data.py` para integrar todo

### Para Análisis:
1. Cargar `culiacan_calendar_cleaned.csv` como dataset principal
2. Revisar `feature_importance_corrected.csv` para variables importantes
3. Ejecutar `corrected_analysis.py` para reproducir el análisis

### Para Reportes:
1. Consultar `resumen_ejecutivo.txt` para insights principales
2. Revisar `reporte_final_consolidado.txt` para detalles técnicos
3. Ver visualizaciones en la carpeta correspondiente

### Para Actualización de Datos:
1. **RECOMENDADO**: Usar `automatizacion_datos_completa.ipynb` (contiene todo el proceso)
2. **Alternativo**: Usar scripts individuales en este orden:
   - `get_homicides.py` → `precio_dolar.py` → `update_all_data.py`
3. Ejecutar `corrected_analysis.py` para re-analizar
4. Generar nuevos reportes con `create_final_summary.py`

## ⚠️ NOTAS IMPORTANTES
- Los datos están filtrados hasta el 08/07/2025 para evitar fechas futuras
- El modelo actual tiene limitaciones (R² negativo) y requiere mejoras
- Se recomienda actualizar datos semanalmente
- Validar nuevos datos antes de incorporar al análisis

## 📧 CONTACTO
Sistema de Análisis de Homicidios v1.0
Desarrollado para: Análisis de Seguridad Pública - Culiacán

---
**Generado automáticamente el**: 13 archivos organizados
**Fecha**: 09/07/2025
