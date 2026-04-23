Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Invoke-Step {
    param(
        [Parameter(Mandatory)]
        [string]$WorkDir,
        [Parameter(Mandatory)]
        [scriptblock]$Command,
        [string]$Description = ''
    )

    if (-not (Test-Path -LiteralPath $WorkDir)) {
        throw "WorkDir '$WorkDir' not found."
    }

    Push-Location -LiteralPath $WorkDir
    try {
        if ($Description) {
            Write-Host "[$WorkDir] $Description"
        } else {
            Write-Host "[$WorkDir] $($Command.ToString().Trim())"
        }

        & $Command

        if ($LASTEXITCODE -ne 0) {
            throw "Command failed with exit code $LASTEXITCODE in '$WorkDir'."
        }
    }
    finally {
        Pop-Location
    }
}

# javawork
Invoke-Step -WorkDir 'javawork' -Description 'Compile' -Command {
    Remove-Item -Force -Recurse out -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Name out | Out-Null
    javac -d out (Get-ChildItem -Recurse -Filter *.java | ForEach-Object { $_.FullName })
}

# migrated legacy demos
Invoke-Step -WorkDir 'javawork' -Description 'Run legacy.basics.Mankind' -Command { java -cp out legacy.basics.Mankind }
Invoke-Step -WorkDir 'javawork' -Description 'Run legacy.basics.work4' -Command { java -cp out legacy.basics.work4 }
Invoke-Step -WorkDir 'javawork' -Description 'Run legacy.basics.test.Employee' -Command { "10`n5`n+`n" | java -cp out legacy.basics.test.Employee }
Invoke-Step -WorkDir 'javawork' -Description 'Run legacy.basics.test.ArraySearchExample' -Command { "2`n4`n*`n" | java -cp out legacy.basics.test.ArraySearchExample }
Invoke-Step -WorkDir 'javawork' -Description 'Run legacy.basics.test.FactorialSum' -Command { java -cp out legacy.basics.test.FactorialSum }
Invoke-Step -WorkDir 'javawork' -Description 'Run legacy.basics.test.HuanTian' -Command { java -cp out legacy.basics.test.HuanTian }
Invoke-Step -WorkDir 'javawork' -Description 'Run legacy.basics.test.RunnoobTest' -Command { java -cp out legacy.basics.test.RunnoobTest }
Invoke-Step -WorkDir 'javawork' -Description 'Run legacy.basics.test.test2' -Command { java -cp out legacy.basics.test.test2 }
Invoke-Step -WorkDir 'javawork' -Description 'Run legacy.basics.test2.work4' -Command { java -cp out legacy.basics.test2.work4 }
Invoke-Step -WorkDir 'javawork' -Description 'Run legacy.hello.Main' -Command { java -cp out legacy.hello.Main }
Invoke-Step -WorkDir 'javawork' -Description 'Run legacy.oop.test.test1' -Command { java -cp out legacy.oop.test.test1 }

# javawork demos
Invoke-Step -WorkDir 'javawork' -Description 'Run javawork.E' -Command { java -cp out javawork.E }
Invoke-Step -WorkDir 'javawork' -Description 'Run javawork.Plant' -Command { java -cp out javawork.Plant }
Invoke-Step -WorkDir 'javawork' -Description 'Run javawork.work1' -Command { java -cp out javawork.work1 }
Invoke-Step -WorkDir 'javawork' -Description 'Run javawork.work2' -Command { java -cp out javawork.work2 }
Invoke-Step -WorkDir 'javawork' -Description 'Run javawork.work3' -Command { "4`n" | java -cp out javawork.work3 }
Invoke-Step -WorkDir 'javawork' -Description 'Run javawork.work4' -Command { java -cp out javawork.work4 }
Invoke-Step -WorkDir 'javawork' -Description 'Run javawork.StudentID' -Command { "20230001`n20230002`n20230003`n20230004`n20230005`n" | java -cp out javawork.StudentID }
Invoke-Step -WorkDir 'javawork' -Description 'Run javawork2.People' -Command { java -cp out javawork2.People }
Invoke-Step -WorkDir 'javawork' -Description 'Run javatest.E' -Command { java -cp out javatest.E }
Invoke-Step -WorkDir 'javawork' -Description 'Run pack3.c' -Command { java -cp out pack3.c }
Invoke-Step -WorkDir 'javawork' -Description 'Run javawork3.E' -Command { java -cp out javawork3.E }
Invoke-Step -WorkDir 'javawork' -Description 'Run javawork4.Vegetable' -Command { java -cp out javawork4.Vegetable }

Write-Host 'Javawork (including migrated legacy demos) compiled and executed successfully.'
