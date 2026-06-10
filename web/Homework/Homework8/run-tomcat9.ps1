$ErrorActionPreference = 'Stop'

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$mavenCandidates = @(
    'C:\Program Files\JetBrains\IntelliJ IDEA 2026.1.1\plugins\maven\lib\maven3\bin\mvn.cmd',
    'E:\idea\IntelliJ IDEA 2025.3.3\plugins\maven\lib\maven3\bin\mvn.cmd'
)
$maven = $mavenCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
$tomcat = 'E:\code\web\Homework\Homework6\tools\apache-tomcat-9.0.117'
$javaHome = 'C:\Program Files\Eclipse Adoptium\jdk-21.0.10.7-hotspot'
$war = Join-Path $projectDir 'target\Homework8.war'
$deployedWar = Join-Path $tomcat 'webapps\Homework8.war'
$expandedApp = Join-Path $tomcat 'webapps\Homework8'

if (-not $maven) {
    throw 'Maven not found. Please check IntelliJ Maven installation.'
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
    Copy-Item -LiteralPath $war -Destination $deployedWar -Force

    $env:JAVA_HOME = $javaHome
    $env:JRE_HOME = ''
    $env:CATALINA_HOME = $tomcat
    $env:CATALINA_BASE = $tomcat

    $process = Start-Process -FilePath (Join-Path $tomcat 'bin\catalina.bat') `
        -ArgumentList 'run' `
        -WorkingDirectory $tomcat `
        -RedirectStandardOutput (Join-Path $tomcat 'logs\homework8-stdout.log') `
        -RedirectStandardError (Join-Path $tomcat 'logs\homework8-stderr.log') `
        -WindowStyle Hidden `
        -PassThru

    for ($i = 0; $i -lt 45; $i++) {
        Start-Sleep -Seconds 1
        try {
            $response = Invoke-WebRequest -Uri 'http://localhost:8080/Homework8/' -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                Write-Host 'Homework8 started successfully.'
                Write-Host 'URL: http://localhost:8080/Homework8/'
                Write-Host "Tomcat PID: $($process.Id)"
                exit 0
            }
        } catch {
        }
    }

    Get-Content -Tail 120 -LiteralPath (Join-Path $tomcat 'logs\homework8-stderr.log'), (Join-Path $tomcat 'logs\homework8-stdout.log') -ErrorAction SilentlyContinue
    throw 'Tomcat started, but Homework8 did not become ready.'
} finally {
    Pop-Location
}
