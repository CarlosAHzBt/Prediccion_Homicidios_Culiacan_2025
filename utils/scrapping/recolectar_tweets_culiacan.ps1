# Script de recolección de tweets sobre Culiacán
# Generado: 2025-10-04 16:30:00
# Período: 2024-09-01 a 2025-09-30 (395 días)
# Palabras clave: Culiacan, Culiacán, Culiacan Sinaloa
# Incluye: Tweets base + respuestas
# Excluye: Retweets

Write-Host 'Iniciando recolección de tweets sobre Culiacán...' -ForegroundColor Green
Write-Host ''
Write-Host '========================================' -ForegroundColor Cyan
Write-Host 'CONFIGURACIÓN:' -ForegroundColor Cyan
Write-Host '========================================' -ForegroundColor Cyan
Write-Host 'Período: 2024-09-01 a 2025-09-30' -ForegroundColor Yellow
Write-Host 'Días totales: 395' -ForegroundColor Yellow
Write-Host 'Palabras clave: Culiacan, Culiacán, Culiacan Sinaloa' -ForegroundColor Yellow
Write-Host 'Incluye respuestas: Sí' -ForegroundColor Yellow
Write-Host 'Excluye retweets: Sí' -ForegroundColor Yellow
Write-Host 'Idioma: es (español)' -ForegroundColor Yellow
Write-Host '========================================' -ForegroundColor Cyan
Write-Host ''
Write-Host '⏱️  Tiempo estimado: 6-7 horas' -ForegroundColor Magenta
Write-Host '💡 Puedes pausar con Ctrl+C y reanudar después' -ForegroundColor Magenta
Write-Host ''
Start-Sleep -Seconds 3

# Verificar que existe el directorio de salida
$outDir = "data_tweets_culiacan\raw"
if (-not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir -Force | Out-Null
    Write-Host "✅ Directorio creado: $outDir" -ForegroundColor Green
}

# Contador de progreso
$totalDias = 395
$diaActual = 0

# SEPTIEMBRE 2024 (30 días)
Write-Host "`n📅 SEPTIEMBRE 2024 (30 días)" -ForegroundColor Cyan

# Día 1: 2024-09-01
$diaActual++
Write-Host "[$diaActual/$totalDias] Recolectando 2024-09-01..." -ForegroundColor Yellow
snscrape --jsonl twitter-search "Culiacan OR Culiacán OR `"Culiacan Sinaloa`" lang:es since:2024-09-01 until:2024-09-02 -filter:retweets" > data_tweets_culiacan\raw\tweets_2024-09-01.jsonl

# Día 2: 2024-09-02
$diaActual++
Write-Host "[$diaActual/$totalDias] Recolectando 2024-09-02..." -ForegroundColor Yellow
snscrape --jsonl twitter-search "Culiacan OR Culiacán OR `"Culiacan Sinaloa`" lang:es since:2024-09-02 until:2024-09-03 -filter:retweets" > data_tweets_culiacan\raw\tweets_2024-09-02.jsonl

# Día 3: 2024-09-03
$diaActual++
Write-Host "[$diaActual/$totalDias] Recolectando 2024-09-03..." -ForegroundColor Yellow
snscrape --jsonl twitter-search "Culiacan OR Culiacán OR `"Culiacan Sinaloa`" lang:es since:2024-09-03 until:2024-09-04 -filter:retweets" > data_tweets_culiacan\raw\tweets_2024-09-03.jsonl

# Continuar con el resto de septiembre 2024...
# (Aquí iría cada día del 4 al 30 de septiembre)
$fechas_sept_2024 = @(
    "2024-09-04", "2024-09-05", "2024-09-06", "2024-09-07", "2024-09-08", "2024-09-09", "2024-09-10",
    "2024-09-11", "2024-09-12", "2024-09-13", "2024-09-14", "2024-09-15", "2024-09-16", "2024-09-17",
    "2024-09-18", "2024-09-19", "2024-09-20", "2024-09-21", "2024-09-22", "2024-09-23", "2024-09-24",
    "2024-09-25", "2024-09-26", "2024-09-27", "2024-09-28", "2024-09-29", "2024-09-30"
)

foreach ($fecha in $fechas_sept_2024) {
    $diaActual++
    $fechaSiguiente = (Get-Date $fecha).AddDays(1).ToString("yyyy-MM-dd")
    Write-Host "[$diaActual/$totalDias] Recolectando $fecha..." -ForegroundColor Yellow
    snscrape --jsonl twitter-search "Culiacan OR Culiacán OR `"Culiacan Sinaloa`" lang:es since:$fecha until:$fechaSiguiente -filter:retweets" > "data_tweets_culiacan\raw\tweets_$fecha.jsonl"
}

# OCTUBRE 2024 (31 días)
Write-Host "`n📅 OCTUBRE 2024 (31 días)" -ForegroundColor Cyan
$fechas_oct_2024 = @(
    "2024-10-01", "2024-10-02", "2024-10-03", "2024-10-04", "2024-10-05", "2024-10-06", "2024-10-07",
    "2024-10-08", "2024-10-09", "2024-10-10", "2024-10-11", "2024-10-12", "2024-10-13", "2024-10-14",
    "2024-10-15", "2024-10-16", "2024-10-17", "2024-10-18", "2024-10-19", "2024-10-20", "2024-10-21",
    "2024-10-22", "2024-10-23", "2024-10-24", "2024-10-25", "2024-10-26", "2024-10-27", "2024-10-28",
    "2024-10-29", "2024-10-30", "2024-10-31"
)

foreach ($fecha in $fechas_oct_2024) {
    $diaActual++
    $fechaSiguiente = (Get-Date $fecha).AddDays(1).ToString("yyyy-MM-dd")
    Write-Host "[$diaActual/$totalDias] Recolectando $fecha..." -ForegroundColor Yellow
    snscrape --jsonl twitter-search "Culiacan OR Culiacán OR `"Culiacan Sinaloa`" lang:es since:$fecha until:$fechaSiguiente -filter:retweets" > "data_tweets_culiacan\raw\tweets_$fecha.jsonl"
}

# NOVIEMBRE 2024 (30 días)
Write-Host "`n📅 NOVIEMBRE 2024 (30 días)" -ForegroundColor Cyan
$fechas_nov_2024 = @(
    "2024-11-01", "2024-11-02", "2024-11-03", "2024-11-04", "2024-11-05", "2024-11-06", "2024-11-07",
    "2024-11-08", "2024-11-09", "2024-11-10", "2024-11-11", "2024-11-12", "2024-11-13", "2024-11-14",
    "2024-11-15", "2024-11-16", "2024-11-17", "2024-11-18", "2024-11-19", "2024-11-20", "2024-11-21",
    "2024-11-22", "2024-11-23", "2024-11-24", "2024-11-25", "2024-11-26", "2024-11-27", "2024-11-28",
    "2024-11-29", "2024-11-30"
)

foreach ($fecha in $fechas_nov_2024) {
    $diaActual++
    $fechaSiguiente = (Get-Date $fecha).AddDays(1).ToString("yyyy-MM-dd")
    Write-Host "[$diaActual/$totalDias] Recolectando $fecha..." -ForegroundColor Yellow
    snscrape --jsonl twitter-search "Culiacan OR Culiacán OR `"Culiacan Sinaloa`" lang:es since:$fecha until:$fechaSiguiente -filter:retweets" > "data_tweets_culiacan\raw\tweets_$fecha.jsonl"
}

# DICIEMBRE 2024 (31 días)
Write-Host "`n📅 DICIEMBRE 2024 (31 días)" -ForegroundColor Cyan
$fechas_dic_2024 = @(
    "2024-12-01", "2024-12-02", "2024-12-03", "2024-12-04", "2024-12-05", "2024-12-06", "2024-12-07",
    "2024-12-08", "2024-12-09", "2024-12-10", "2024-12-11", "2024-12-12", "2024-12-13", "2024-12-14",
    "2024-12-15", "2024-12-16", "2024-12-17", "2024-12-18", "2024-12-19", "2024-12-20", "2024-12-21",
    "2024-12-22", "2024-12-23", "2024-12-24", "2024-12-25", "2024-12-26", "2024-12-27", "2024-12-28",
    "2024-12-29", "2024-12-30", "2024-12-31"
)

foreach ($fecha in $fechas_dic_2024) {
    $diaActual++
    $fechaSiguiente = (Get-Date $fecha).AddDays(1).ToString("yyyy-MM-dd")
    Write-Host "[$diaActual/$totalDias] Recolectando $fecha..." -ForegroundColor Yellow
    snscrape --jsonl twitter-search "Culiacan OR Culiacán OR `"Culiacan Sinaloa`" lang:es since:$fecha until:$fechaSiguiente -filter:retweets" > "data_tweets_culiacan\raw\tweets_$fecha.jsonl"
}

# ENERO 2025 (31 días)
Write-Host "`n📅 ENERO 2025 (31 días)" -ForegroundColor Cyan
$fechas_ene_2025 = @(
    "2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05", "2025-01-06", "2025-01-07",
    "2025-01-08", "2025-01-09", "2025-01-10", "2025-01-11", "2025-01-12", "2025-01-13", "2025-01-14",
    "2025-01-15", "2025-01-16", "2025-01-17", "2025-01-18", "2025-01-19", "2025-01-20", "2025-01-21",
    "2025-01-22", "2025-01-23", "2025-01-24", "2025-01-25", "2025-01-26", "2025-01-27", "2025-01-28",
    "2025-01-29", "2025-01-30", "2025-01-31"
)

foreach ($fecha in $fechas_ene_2025) {
    $diaActual++
    $fechaSiguiente = (Get-Date $fecha).AddDays(1).ToString("yyyy-MM-dd")
    Write-Host "[$diaActual/$totalDias] Recolectando $fecha..." -ForegroundColor Yellow
    snscrape --jsonl twitter-search "Culiacan OR Culiacán OR `"Culiacan Sinaloa`" lang:es since:$fecha until:$fechaSiguiente -filter:retweets" > "data_tweets_culiacan\raw\tweets_$fecha.jsonl"
}

# FEBRERO 2025 (28 días)
Write-Host "`n📅 FEBRERO 2025 (28 días)" -ForegroundColor Cyan
$fechas_feb_2025 = @(
    "2025-02-01", "2025-02-02", "2025-02-03", "2025-02-04", "2025-02-05", "2025-02-06", "2025-02-07",
    "2025-02-08", "2025-02-09", "2025-02-10", "2025-02-11", "2025-02-12", "2025-02-13", "2025-02-14",
    "2025-02-15", "2025-02-16", "2025-02-17", "2025-02-18", "2025-02-19", "2025-02-20", "2025-02-21",
    "2025-02-22", "2025-02-23", "2025-02-24", "2025-02-25", "2025-02-26", "2025-02-27", "2025-02-28"
)

foreach ($fecha in $fechas_feb_2025) {
    $diaActual++
    $fechaSiguiente = (Get-Date $fecha).AddDays(1).ToString("yyyy-MM-dd")
    Write-Host "[$diaActual/$totalDias] Recolectando $fecha..." -ForegroundColor Yellow
    snscrape --jsonl twitter-search "Culiacan OR Culiacán OR `"Culiacan Sinaloa`" lang:es since:$fecha until:$fechaSiguiente -filter:retweets" > "data_tweets_culiacan\raw\tweets_$fecha.jsonl"
}

# MARZO 2025 (31 días)
Write-Host "`n📅 MARZO 2025 (31 días)" -ForegroundColor Cyan
$fechas_mar_2025 = @(
    "2025-03-01", "2025-03-02", "2025-03-03", "2025-03-04", "2025-03-05", "2025-03-06", "2025-03-07",
    "2025-03-08", "2025-03-09", "2025-03-10", "2025-03-11", "2025-03-12", "2025-03-13", "2025-03-14",
    "2025-03-15", "2025-03-16", "2025-03-17", "2025-03-18", "2025-03-19", "2025-03-20", "2025-03-21",
    "2025-03-22", "2025-03-23", "2025-03-24", "2025-03-25", "2025-03-26", "2025-03-27", "2025-03-28",
    "2025-03-29", "2025-03-30", "2025-03-31"
)

foreach ($fecha in $fechas_mar_2025) {
    $diaActual++
    $fechaSiguiente = (Get-Date $fecha).AddDays(1).ToString("yyyy-MM-dd")
    Write-Host "[$diaActual/$totalDias] Recolectando $fecha..." -ForegroundColor Yellow
    snscrape --jsonl twitter-search "Culiacan OR Culiacán OR `"Culiacan Sinaloa`" lang:es since:$fecha until:$fechaSiguiente -filter:retweets" > "data_tweets_culiacan\raw\tweets_$fecha.jsonl"
}

# ABRIL 2025 (30 días)
Write-Host "`n📅 ABRIL 2025 (30 días)" -ForegroundColor Cyan
$fechas_abr_2025 = @(
    "2025-04-01", "2025-04-02", "2025-04-03", "2025-04-04", "2025-04-05", "2025-04-06", "2025-04-07",
    "2025-04-08", "2025-04-09", "2025-04-10", "2025-04-11", "2025-04-12", "2025-04-13", "2025-04-14",
    "2025-04-15", "2025-04-16", "2025-04-17", "2025-04-18", "2025-04-19", "2025-04-20", "2025-04-21",
    "2025-04-22", "2025-04-23", "2025-04-24", "2025-04-25", "2025-04-26", "2025-04-27", "2025-04-28",
    "2025-04-29", "2025-04-30"
)

foreach ($fecha in $fechas_abr_2025) {
    $diaActual++
    $fechaSiguiente = (Get-Date $fecha).AddDays(1).ToString("yyyy-MM-dd")
    Write-Host "[$diaActual/$totalDias] Recolectando $fecha..." -ForegroundColor Yellow
    snscrape --jsonl twitter-search "Culiacan OR Culiacán OR `"Culiacan Sinaloa`" lang:es since:$fecha until:$fechaSiguiente -filter:retweets" > "data_tweets_culiacan\raw\tweets_$fecha.jsonl"
}

# MAYO 2025 (31 días)
Write-Host "`n📅 MAYO 2025 (31 días)" -ForegroundColor Cyan
$fechas_may_2025 = @(
    "2025-05-01", "2025-05-02", "2025-05-03", "2025-05-04", "2025-05-05", "2025-05-06", "2025-05-07",
    "2025-05-08", "2025-05-09", "2025-05-10", "2025-05-11", "2025-05-12", "2025-05-13", "2025-05-14",
    "2025-05-15", "2025-05-16", "2025-05-17", "2025-05-18", "2025-05-19", "2025-05-20", "2025-05-21",
    "2025-05-22", "2025-05-23", "2025-05-24", "2025-05-25", "2025-05-26", "2025-05-27", "2025-05-28",
    "2025-05-29", "2025-05-30", "2025-05-31"
)

foreach ($fecha in $fechas_may_2025) {
    $diaActual++
    $fechaSiguiente = (Get-Date $fecha).AddDays(1).ToString("yyyy-MM-dd")
    Write-Host "[$diaActual/$totalDias] Recolectando $fecha..." -ForegroundColor Yellow
    snscrape --jsonl twitter-search "Culiacan OR Culiacán OR `"Culiacan Sinaloa`" lang:es since:$fecha until:$fechaSiguiente -filter:retweets" > "data_tweets_culiacan\raw\tweets_$fecha.jsonl"
}

# JUNIO 2025 (30 días)
Write-Host "`n📅 JUNIO 2025 (30 días)" -ForegroundColor Cyan
$fechas_jun_2025 = @(
    "2025-06-01", "2025-06-02", "2025-06-03", "2025-06-04", "2025-06-05", "2025-06-06", "2025-06-07",
    "2025-06-08", "2025-06-09", "2025-06-10", "2025-06-11", "2025-06-12", "2025-06-13", "2025-06-14",
    "2025-06-15", "2025-06-16", "2025-06-17", "2025-06-18", "2025-06-19", "2025-06-20", "2025-06-21",
    "2025-06-22", "2025-06-23", "2025-06-24", "2025-06-25", "2025-06-26", "2025-06-27", "2025-06-28",
    "2025-06-29", "2025-06-30"
)

foreach ($fecha in $fechas_jun_2025) {
    $diaActual++
    $fechaSiguiente = (Get-Date $fecha).AddDays(1).ToString("yyyy-MM-dd")
    Write-Host "[$diaActual/$totalDias] Recolectando $fecha..." -ForegroundColor Yellow
    snscrape --jsonl twitter-search "Culiacan OR Culiacán OR `"Culiacan Sinaloa`" lang:es since:$fecha until:$fechaSiguiente -filter:retweets" > "data_tweets_culiacan\raw\tweets_$fecha.jsonl"
}

# JULIO 2025 (31 días)
Write-Host "`n📅 JULIO 2025 (31 días)" -ForegroundColor Cyan
$fechas_jul_2025 = @(
    "2025-07-01", "2025-07-02", "2025-07-03", "2025-07-04", "2025-07-05", "2025-07-06", "2025-07-07",
    "2025-07-08", "2025-07-09", "2025-07-10", "2025-07-11", "2025-07-12", "2025-07-13", "2025-07-14",
    "2025-07-15", "2025-07-16", "2025-07-17", "2025-07-18", "2025-07-19", "2025-07-20", "2025-07-21",
    "2025-07-22", "2025-07-23", "2025-07-24", "2025-07-25", "2025-07-26", "2025-07-27", "2025-07-28",
    "2025-07-29", "2025-07-30", "2025-07-31"
)

foreach ($fecha in $fechas_jul_2025) {
    $diaActual++
    $fechaSiguiente = (Get-Date $fecha).AddDays(1).ToString("yyyy-MM-dd")
    Write-Host "[$diaActual/$totalDias] Recolectando $fecha..." -ForegroundColor Yellow
    snscrape --jsonl twitter-search "Culiacan OR Culiacán OR `"Culiacan Sinaloa`" lang:es since:$fecha until:$fechaSiguiente -filter:retweets" > "data_tweets_culiacan\raw\tweets_$fecha.jsonl"
}

# AGOSTO 2025 (31 días)
Write-Host "`n📅 AGOSTO 2025 (31 días)" -ForegroundColor Cyan
$fechas_ago_2025 = @(
    "2025-08-01", "2025-08-02", "2025-08-03", "2025-08-04", "2025-08-05", "2025-08-06", "2025-08-07",
    "2025-08-08", "2025-08-09", "2025-08-10", "2025-08-11", "2025-08-12", "2025-08-13", "2025-08-14",
    "2025-08-15", "2025-08-16", "2025-08-17", "2025-08-18", "2025-08-19", "2025-08-20", "2025-08-21",
    "2025-08-22", "2025-08-23", "2025-08-24", "2025-08-25", "2025-08-26", "2025-08-27", "2025-08-28",
    "2025-08-29", "2025-08-30", "2025-08-31"
)

foreach ($fecha in $fechas_ago_2025) {
    $diaActual++
    $fechaSiguiente = (Get-Date $fecha).AddDays(1).ToString("yyyy-MM-dd")
    Write-Host "[$diaActual/$totalDias] Recolectando $fecha..." -ForegroundColor Yellow
    snscrape --jsonl twitter-search "Culiacan OR Culiacán OR `"Culiacan Sinaloa`" lang:es since:$fecha until:$fechaSiguiente -filter:retweets" > "data_tweets_culiacan\raw\tweets_$fecha.jsonl"
}

# SEPTIEMBRE 2025 (30 días)
Write-Host "`n📅 SEPTIEMBRE 2025 (30 días)" -ForegroundColor Cyan
$fechas_sep_2025 = @(
    "2025-09-01", "2025-09-02", "2025-09-03", "2025-09-04", "2025-09-05", "2025-09-06", "2025-09-07",
    "2025-09-08", "2025-09-09", "2025-09-10", "2025-09-11", "2025-09-12", "2025-09-13", "2025-09-14",
    "2025-09-15", "2025-09-16", "2025-09-17", "2025-09-18", "2025-09-19", "2025-09-20", "2025-09-21",
    "2025-09-22", "2025-09-23", "2025-09-24", "2025-09-25", "2025-09-26", "2025-09-27", "2025-09-28",
    "2025-09-29", "2025-09-30"
)

foreach ($fecha in $fechas_sep_2025) {
    $diaActual++
    $fechaSiguiente = (Get-Date $fecha).AddDays(1).ToString("yyyy-MM-dd")
    Write-Host "[$diaActual/$totalDias] Recolectando $fecha..." -ForegroundColor Yellow
    snscrape --jsonl twitter-search "Culiacan OR Culiacán OR `"Culiacan Sinaloa`" lang:es since:$fecha until:$fechaSiguiente -filter:retweets" > "data_tweets_culiacan\raw\tweets_$fecha.jsonl"
}

# Resumen final
Write-Host ''
Write-Host '========================================' -ForegroundColor Green
Write-Host 'RECOLECCIÓN COMPLETADA' -ForegroundColor Green
Write-Host '========================================' -ForegroundColor Green
Write-Host "✅ Total de días procesados: $diaActual" -ForegroundColor Yellow
Write-Host "📁 Archivos guardados en: data_tweets_culiacan\raw\" -ForegroundColor Yellow
Write-Host ''
Write-Host '📋 SIGUIENTES PASOS:' -ForegroundColor Cyan
Write-Host '   1. Procesar los tweets: python utils\scrapping\ejemplo_uso_completo.py' -ForegroundColor White
Write-Host '   2. Seleccionar opción 3 (Procesar tweets recolectados)' -ForegroundColor White
Write-Host '   3. Seleccionar opción 4 (Generar visualizaciones)' -ForegroundColor White
Write-Host ''
