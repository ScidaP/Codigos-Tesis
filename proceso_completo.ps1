param (
    [string]$fecha
)

# Script: ejecutar-pruebas.ps1
# Para permitir ejecutar scripts:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Definition)

# 1️ Ejecutar script SQL en PostgreSQL
Write-Host "Ejecutando borrar.sql en BarDB..."
psql -h 192.168.100.15 -U postgres -d BarDB -f borrar.sql
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error ejecutando borrar.sql" -ForegroundColor Red
    exit $LASTEXITCODE
}

# 2️ Ejecutar prueba de estrés con Locust en segundo plano...
Write-Host "Ejecutando prueba de estrés con Locust en segundo plano..."
$locustJob = Start-Job -ScriptBlock {
    param($fechaParam)

    Set-Location 'E:\Tesis\Codigos_Tesis'

    $csvPath = "Resultados\$fechaParam\100-Usuarios\Locust\data"
    $htmlPath = "Resultados\$fechaParam\100-Usuarios\Locust\pagina.html"

    Write-Host "Ejecutando locust con:"
    Write-Host "CSV path: $csvPath"
    Write-Host "HTML path: $htmlPath"

    # Ejecutar locust pasando las variables ya interpoladas como argumentos separados
    locust -f pruebaEstres.py -H http://192.168.100.15/ --headless -u 100 -r 10 `
        --csv $csvPath `
        --html $htmlPath `
        --run-time 4m
} -ArgumentList $fecha


Write-Host "Durmiendo 10 segundos mientras spawnean usuarios..."
Start-Sleep -Seconds 10 # Locust demora 10 segundos en spawnear los 100 usuarios

# 3️ Conectarse por SSH y ejecutar script remoto
Write-Host "Ejecutando script remoto por SSH..."
& "C:\Windows\System32\OpenSSH\ssh.exe" -i 'C:\Users\patri\.ssh\id_ed25519' pscida@192.168.100.15 `
    'pruebas-perfomance/benchmarks/BUCLE.sh "pruebas-perfomance/Resultados/100-Usuarios" 2'
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error ejecutando script remoto" -ForegroundColor Red
    exit $LASTEXITCODE
}

# Esperar que Locust termine antes de seguir con el SCP
Write-Host "Esperando a que termine la prueba de estrés..."
Wait-Job $locustJob
Receive-Job $locustJob | ForEach-Object { Write-Host $_ }

# 4 Copiar resultados desde el servidor con SCP
Write-Host "Copiando resultados con SCP..."
$destino = "E:\Tesis/Codigos_Tesis/Resultados/${fecha}/100-Usuarios/Datos_CSV"
if (-not (Test-Path $destino)) {
    Write-Host "Creando carpeta destino: $destino"
    New-Item -ItemType Directory -Path $destino -Force | Out-Null
}

& "C:\Windows\System32\OpenSSH\scp.exe" -r "pscida@192.168.100.15:~/pruebas-perfomance/Resultados/100-Usuarios/*" $destino

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error copiando resultados con SCP" -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "Todo el proceso finalizó correctamente." -ForegroundColor Green
