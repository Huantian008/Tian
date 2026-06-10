$ErrorActionPreference = 'Stop'

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$maven = 'C:\Program Files\JetBrains\IntelliJ IDEA 2026.1.1\plugins\maven\lib\maven3\bin\mvn.cmd'
$tomcat = 'E:\code\web\Homework\Homework6\tools\apache-tomcat-9.0.117'
$javaHome = 'C:\Program Files\Eclipse Adoptium\jdk-21.0.10.7-hotspot'
$war = Join-Path $projectDir 'target\Homework7.war'
$deployedWar = Join-Path $tomcat 'webapps\Homework7.war'
$expandedApp = Join-Path $tomcat 'webapps\Homework7'
$stdout = Join-Path $tomcat 'logs\homework7-stdout.log'
$stderr = Join-Path $tomcat 'logs\homework7-stderr.log'

if (-not (Test-Path -LiteralPath $maven)) {
    throw "Maven not found: $maven"
}
if (-not (Test-Path -LiteralPath $tomcat)) {
    throw "Tomcat9 not found: $tomcat"
}
if (-not (Test-Path -LiteralPath $javaHome)) {
    throw "JAVA_HOME not found: $javaHome"
}

Push-Location $projectDir
try {
    & $maven clean package
    if ($LASTEXITCODE -ne 0) {
        throw 'Maven package failed.'
    }

    $connections = Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue
    foreach ($connection in $connections) {
        $process = Get-Process -Id $connection.OwningProcess -ErrorAction SilentlyContinue
        if ($process -and $process.Path -like "$javaHome\bin\java.exe") {
            Stop-Process -Id $process.Id -Force
            Start-Sleep -Seconds 2
        }
    }

    if (Test-Path -LiteralPath $expandedApp) {
        Remove-Item -LiteralPath $expandedApp -Recurse -Force
    }
    if (Test-Path -LiteralPath $deployedWar) {
        Remove-Item -LiteralPath $deployedWar -Force
    }
    Copy-Item -LiteralPath $war -Destination $deployedWar -Force

    $env:JAVA_HOME = $javaHome
    $env:JRE_HOME = ''
    $env:CATALINA_HOME = $tomcat
    $env:CATALINA_BASE = $tomcat

    $process = Start-Process -FilePath (Join-Path $tomcat 'bin\catalina.bat') `
        -ArgumentList 'run' `
        -WorkingDirectory $tomcat `
        -RedirectStandardOutput $stdout `
        -RedirectStandardError $stderr `
        -WindowStyle Hidden `
        -PassThru

    for ($i = 0; $i -lt 45; $i++) {
        Start-Sleep -Seconds 1
        try {
            $response = Invoke-WebRequest -Uri 'http://localhost:8080/Homework7/user/query' -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                Write-Host 'Homework7 started successfully.'
                Write-Host 'URL: http://localhost:8080/Homework7/user/query'
                Write-Host "Tomcat PID: $($process.Id)"
                exit 0
            }
        } catch {
        }
    }

    Get-Content -Tail 120 -LiteralPath $stderr, $stdout -ErrorAction SilentlyContinue
    throw 'Tomcat started, but Homework7 did not become ready.'
} finally {
    Pop-Location
}
