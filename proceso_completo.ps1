param (
    [string]$fecha
)

Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Definition)

for ($i = 1; $i -le 10; $i++) {
    $valor = $i * 100
    Write-Host "Simulacion de $valor usuarios"

    # 1️ Ejecutar script SQL
    Write-Host "Ejecutando borrar.sql en BarDB..."
    psql -h 192.168.100.15 -U postgres -d BarDB -f borrar.sql
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error ejecutando borrar.sql" -ForegroundColor Red
        exit $LASTEXITCODE
    }

    # 2️ Ejecutar prueba de estrés con Locust en segundo plano...
    Write-Host "Ejecutando prueba de estrés con Locust en segundo plano..."
    $locustJob = Start-Job -ScriptBlock {
        param($fechaParam, $valParam)

        Set-Location 'E:\Tesis\Codigos_Tesis'

        $csvPath = "Resultados\$fechaParam\$valParam-Usuarios\Locust\data"
        $htmlPath = "Resultados\$fechaParam\$valParam-Usuarios\Locust\pagina.html"
        $runtime = 720 + ${valParam}/10
        Write-Host "Corriendo por $runtime segundos" -ForegroundColor Yellow
        locust -f pruebaEstres.py -H http://192.168.100.15/ --headless -u $valParam -r 10 `
            --csv $csvPath `
            --html $htmlPath `
            --run-time "${runtime}s"
    } -ArgumentList $fecha, $valor

    $dormir = $valor/10
    Write-Host "Durmiendo $dormir segundos mientras spawnean usuarios..."
    Start-Sleep -Seconds $dormir

    # 3️ Ejecutar script remoto por SSH
    Write-Host "Ejecutando script remoto por SSH..."
    & "C:\Windows\System32\OpenSSH\ssh.exe" -i 'C:\Users\patri\.ssh\id_ed25519' pscida@192.168.100.15 `
        "pruebas-perfomance/benchmarks/BUCLE.sh 'pruebas-perfomance/Resultados/$valor-Usuarios' 10"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error ejecutando script remoto" -ForegroundColor Red
        exit $LASTEXITCODE
    }

    # Esperar a que termine locust antes de seguir
    Write-Host "Esperando a que termine la prueba de estrés..."
    Wait-Job $locustJob
    Receive-Job $locustJob | ForEach-Object { Write-Host $_ }

    # 4 Copiar resultados con SCP
    Write-Host "Copiando resultados con SCP..."
    $destino = "E:\Tesis\Codigos_Tesis\Resultados\$fecha\$valor-Usuarios\Datos_CSV"
    if (-not (Test-Path $destino)) {
        Write-Host "Creando carpeta destino: $destino"
        New-Item -ItemType Directory -Path $destino -Force | Out-Null
    }

    & "C:\Windows\System32\OpenSSH\scp.exe" -r "pscida@192.168.100.15:~/pruebas-perfomance/Resultados/$valor-Usuarios/*" $destino

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error copiando resultados con SCP" -ForegroundColor Red
        exit $LASTEXITCODE
    }

    # 5 Cerrar conexiones con la DB
    Write-Host "Ejecutando cerrar_conexiones.sql"
    psql -h 192.168.100.15 -U postgres -d BarDB -f cerrar_conexiones.sql
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error ejecutando cerrar_conexiones.sql" -ForegroundColor Red
        exit $LASTEXITCODE
    }

    Write-Host "Simulacion $valor usuarios finalizada correctamente." -ForegroundColor Green
    Write-Host "Durmiendo 5 segundos para esperar al servidor..."
    Start-Sleep -Seconds 5
}

Write-Host "Todo el proceso finalizó para las 10 iteraciones." -ForegroundColor Green
