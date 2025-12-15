param (
    [string]$fecha
)

Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Definition)

# Definir IPs de las 3 sucursales
$sucursales = @(
    @{IP = "192.168.100.229"; Nombre = "Sucursal_229"},
    @{IP = "192.168.100.242"; Nombre = "Sucursal_242"},
    @{IP = "192.168.100.243"; Nombre = "Sucursal_243"}
)

for ($i = 1; $i -le 10; $i++) {
    $valor = $i * 100
    Write-Host "Simulacion de $valor usuarios (3 sucursales simultaneas)"

    # 1️ Ejecutar script SQL
    Write-Host "Ejecutando borrar.sql en BarDB..."
    psql -h 192.168.100.230 -U postgres -d BarDB -f borrar.sql
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error ejecutando borrar.sql" -ForegroundColor Red
        exit $LASTEXITCODE
    }

    # 2️ Ejecutar pruebas de estrés con Locust en segundo plano para las 3 sucursales...
    Write-Host "Ejecutando pruebas de estrés con Locust en segundo plano para 3 sucursales..."
    $locustJobs = @()
    
    foreach ($sucursal in $sucursales) {
        $ip = $sucursal.IP
        $nombreSucursal = $sucursal.Nombre
        Write-Host "Iniciando Locust para $nombreSucursal ($ip)..." -ForegroundColor Cyan
        
        $locustJob = Start-Job -ScriptBlock {
            param($fechaParam, $valParam, $ipParam, $nombreSucursalParam)

            Set-Location 'E:\Tesis\Codigos_Tesis'

            $csvPath = "Resultados\Proxmox_Triple_Sucursal\$fechaParam\$valParam-Usuarios\Locust\$nombreSucursalParam\data"
            $htmlPath = "Resultados\Proxmox_Triple_Sucursal\$fechaParam\$valParam-Usuarios\Locust\$nombreSucursalParam\pagina.html"
            $runtime = 720 + ${valParam}/10
            Write-Host "[$nombreSucursalParam] Corriendo por $runtime segundos" -ForegroundColor Yellow
            locust -f pruebaEstres.py -H http://${ipParam}:5000 --headless -u $valParam -r 10 `
                --csv $csvPath `
                --html $htmlPath `
                --run-time "${runtime}s"
        } -ArgumentList $fecha, $valor, $ip, $nombreSucursal
        
        $locustJobs += $locustJob
    }

    $dormir = $valor/10
    Write-Host "Durmiendo $dormir segundos mientras spawnean usuarios en las 3 sucursales..."
    Start-Sleep -Seconds $dormir

    # 3️ Ejecutar script remoto por SSH
    Write-Host "Ejecutando script remoto por SSH..."
    & "C:\Windows\System32\OpenSSH\ssh.exe" -i 'C:\Users\patri\.ssh\id_ed25519' pscida@192.168.100.229 `
        "pruebas-perfomance/benchmarks/BUCLE.sh 'pruebas-perfomance/Resultados_Triple_Sucursal/$fecha/$valor-Usuarios' 10"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error ejecutando script remoto" -ForegroundColor Red
        exit $LASTEXITCODE
    }

    # Esperar a que terminen todos los trabajos Locust antes de seguir
    Write-Host "Esperando a que terminen las pruebas de estrés de las 3 sucursales..."
    Wait-Job $locustJobs | Out-Null
    
    foreach ($job in $locustJobs) {
        Write-Host "Resultados de trabajo Locust:" -ForegroundColor Green
        Receive-Job $job | ForEach-Object { Write-Host $_ }
        Remove-Job $job
    }

    # 4 Copiar resultados con SCP
    Write-Host "Copiando resultados con SCP..."
    $destino = "E:\Tesis\Codigos_Tesis\Resultados\Proxmox_Triple_Sucursal\$fecha\$valor-Usuarios\Datos_CSV"
    if (-not (Test-Path $destino)) {
        Write-Host "Creando carpeta destino: $destino"
        New-Item -ItemType Directory -Path $destino -Force | Out-Null
    }

    & "C:\Windows\System32\OpenSSH\scp.exe" -r "pscida@192.168.100.229:~/pruebas-perfomance/Resultados_Triple_Sucursal/$fecha/$valor-Usuarios/*" $destino

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error copiando resultados con SCP" -ForegroundColor Red
        exit $LASTEXITCODE
    }

    # 5 Cerrar conexiones con la DB
    Write-Host "Ejecutando cerrar_conexiones.sql"
    psql -h 192.168.100.230 -U postgres -d BarDB -f cerrar_conexiones.sql
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error ejecutando cerrar_conexiones.sql" -ForegroundColor Red
        exit $LASTEXITCODE
    }

    Write-Host "Simulacion $valor usuarios finalizada correctamente." -ForegroundColor Green
    Write-Host "Durmiendo 5 segundos para esperar al servidor..."
    Start-Sleep -Seconds 5
}

Write-Host "Todo el proceso finalizó para las 10 iteraciones." -ForegroundColor Green
