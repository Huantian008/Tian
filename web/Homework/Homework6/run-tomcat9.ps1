$ErrorActionPreference = 'Stop'

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$maven = 'E:\idea\IntelliJ IDEA 2025.3.3\plugins\maven\lib\maven3\bin\mvn.cmd'
$tomcat = Join-Path $projectDir 'tools\apache-tomcat-9.0.117'
$javaHome = 'C:\Program Files\Eclipse Adoptium\jdk-21.0.10.7-hotspot'
$war = Join-Path $projectDir 'target\Homework6.war'
$deployedWar = Join-Path $tomcat 'webapps\Homework6.war'
$expandedApp = Join-Path $tomcat 'webapps\Homework6'

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
        throw "Maven package failed."
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
        -RedirectStandardOutput (Join-Path $tomcat 'logs\idea-stdout.log') `
        -RedirectStandardError (Join-Path $tomcat 'logs\idea-stderr.log') `
        -WindowStyle Hidden `
        -PassThru

    for ($i = 0; $i -lt 45; $i++) {
        Start-Sleep -Seconds 1
        try {
            $response = Invoke-WebRequest -Uri 'http://localhost:8080/Homework6/students' -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                Write-Host 'Homework6 started successfully.'
                Write-Host 'URL: http://localhost:8080/Homework6/students'
                Write-Host "Tomcat PID: $($process.Id)"
                exit 0
            }
        } catch {
        }
    }

    Get-Content -Tail 120 -LiteralPath (Join-Path $tomcat 'logs\idea-stderr.log'), (Join-Path $tomcat 'logs\idea-stdout.log') -ErrorAction SilentlyContinue
    throw 'Tomcat started, but Homework6 did not become ready.'
} finally {
    Pop-Location
}
