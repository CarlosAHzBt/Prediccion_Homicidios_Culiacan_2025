# Script de instalación y configuración rápida del sistema de análisis de emociones
# Ejecutar como: .\setup_sistema_tweets.ps1

Write-Host @"

╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║     INSTALACIÓN DEL SISTEMA DE ANÁLISIS DE EMOCIONES             ║
║     Proyecto: Predicción de Homicidios en Culiacán              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

Write-Host "Iniciando instalación..." -ForegroundColor Green
Write-Host ""

# 1. Verificar Python
Write-Host "1️⃣  Verificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "   ❌ Python no encontrado. Por favor instala Python 3.8 o superior." -ForegroundColor Red
    exit 1
}

# 2. Verificar pip
Write-Host "`n2️⃣  Verificando pip..." -ForegroundColor Yellow
$pipVersion = pip --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ pip encontrado: $pipVersion" -ForegroundColor Green
} else {
    Write-Host "   ❌ pip no encontrado." -ForegroundColor Red
    exit 1
}

# 3. Actualizar pip
Write-Host "`n3️⃣  Actualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip
Write-Host "   ✅ pip actualizado" -ForegroundColor Green

# 4. Instalar dependencias
Write-Host "`n4️⃣  Instalando dependencias..." -ForegroundColor Yellow
Write-Host "   (Esto puede tomar varios minutos...)" -ForegroundColor Gray

$requirementsFile = "utils\scrapping\requirements_tweets.txt"

if (Test-Path $requirementsFile) {
    pip install -r $requirementsFile
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Dependencias instaladas" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Hubo algunos errores, pero continuando..." -ForegroundColor Yellow
    }
} else {
    Write-Host "   ⚠️  Archivo requirements_tweets.txt no encontrado." -ForegroundColor Yellow
    Write-Host "   Instalando paquetes manualmente..." -ForegroundColor Yellow
    
    $packages = @(
        "snscrape",
        "pysentimiento",
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "tqdm",
        "langdetect",
        "emoji"
    )
    
    foreach ($package in $packages) {
        Write-Host "   Instalando $package..." -ForegroundColor Gray
        pip install $package --quiet
    }
    Write-Host "   ✅ Paquetes instalados" -ForegroundColor Green
}

# 5. Crear estructura de directorios
Write-Host "`n5️⃣  Creando estructura de directorios..." -ForegroundColor Yellow

$dirs = @(
    "data_tweets_culiacan\raw",
    "data_tweets_culiacan\procesados",
    "data_tweets_culiacan\resultados",
    "data_tweets_culiacan\visualizaciones",
    "data_tweets_culiacan\test"
)

foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "   ✅ Creado: $dir" -ForegroundColor Green
    } else {
        Write-Host "   ℹ️  Ya existe: $dir" -ForegroundColor Gray
    }
}

# 6. Verificar instalación
Write-Host "`n6️⃣  Verificando instalación..." -ForegroundColor Yellow

$testScript = "utils\scrapping\test_sistema.py"

if (Test-Path $testScript) {
    Write-Host "   Ejecutando tests de verificación..." -ForegroundColor Gray
    python $testScript
} else {
    Write-Host "   ⚠️  Script de test no encontrado, saltando verificación." -ForegroundColor Yellow
}

# 7. Descargar modelos de pysentimiento
Write-Host "`n7️⃣  Descargando modelo de emociones..." -ForegroundColor Yellow
Write-Host "   (Primera vez: ~500MB, puede tomar varios minutos)" -ForegroundColor Gray

python -c @"
try:
    from pysentimiento import create_analyzer
    print('   Descargando modelo...')
    analyzer = create_analyzer(task='emotion', lang='es')
    print('   ✅ Modelo descargado correctamente')
except Exception as e:
    print(f'   ⚠️  Error descargando modelo: {e}')
    print('   El modelo se descargará en el primer uso.')
"@

# 8. Resumen final
Write-Host @"

╔══════════════════════════════════════════════════════════════════╗
║                   ✅ INSTALACIÓN COMPLETADA                      ║
╚══════════════════════════════════════════════════════════════════╝

📋 SIGUIENTES PASOS:

1️⃣  CONFIGURAR PARÁMETROS (opcional):
   Edita: utils\scrapping\config_tweets.py
   - Ajusta fechas (ANIO_INICIO, ANIO_FIN)
   - Modifica palabras clave
   - Personaliza filtros

2️⃣  INICIAR ANÁLISIS:
   
   Opción A - Menú interactivo (recomendado):
   python utils\scrapping\ejemplo_uso_completo.py
   
   Opción B - Código directo:
   python -c "from utils.scrapping.tweets_sentiments_test import TweetsEmotionAnalyzer; analyzer = TweetsEmotionAnalyzer(); analyzer.generar_script_recoleccion('recolectar.ps1')"

3️⃣  EJECUTAR TESTS (opcional):
   python utils\scrapping\test_sistema.py

📚 DOCUMENTACIÓN:
   Lee: utils\scrapping\README_TWEETS.md

💡 EJEMPLO RÁPIDO (7 días de prueba):
   python -c "from utils.scrapping.test_sistema import generar_datos_prueba, guardar_datos_prueba; df = generar_datos_prueba(7, 50); guardar_datos_prueba(df)"

"@ -ForegroundColor Cyan

Write-Host "🎉 ¡Listo para empezar!" -ForegroundColor Green
Write-Host ""
