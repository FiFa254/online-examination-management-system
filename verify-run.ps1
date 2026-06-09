$ErrorActionPreference = 'Continue'

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$LogDir = Join-Path $ProjectRoot 'test-logs'
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

$Timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$SummaryPath = Join-Path $LogDir "verify-$Timestamp.txt"

function Test-App {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ExeName
    )

    $ExePath = Join-Path $ProjectRoot $ExeName
    $OutPath = Join-Path $LogDir "$($ExeName)-$Timestamp.out.txt"
    $ErrPath = Join-Path $LogDir "$($ExeName)-$Timestamp.err.txt"

    Add-Content -LiteralPath $SummaryPath -Value "[$(Get-Date -Format s)] Testing $ExeName"

    if (-not (Test-Path -LiteralPath $ExePath)) {
        Add-Content -LiteralPath $SummaryPath -Value "MISSING: $ExePath"
        return
    }

    try {
        $process = Start-Process -FilePath $ExePath -WorkingDirectory $ProjectRoot -PassThru -RedirectStandardOutput $OutPath -RedirectStandardError $ErrPath -WindowStyle Hidden
        Start-Sleep -Seconds 12

        if ($process.HasExited) {
            Add-Content -LiteralPath $SummaryPath -Value "EXITED: $ExeName exit code $($process.ExitCode)"
        }
        else {
            Add-Content -LiteralPath $SummaryPath -Value "RUNNING: $ExeName stayed alive for 12 seconds; stopping test process."
            Stop-Process -Id $process.Id -Force
        }

        if (Test-Path -LiteralPath $ErrPath) {
            $err = Get-Content -LiteralPath $ErrPath -Raw
            if ($err.Trim().Length -gt 0) {
                Add-Content -LiteralPath $SummaryPath -Value "STDERR:"
                Add-Content -LiteralPath $SummaryPath -Value $err
            }
        }
    }
    catch {
        Add-Content -LiteralPath $SummaryPath -Value "FAILED: $($_.Exception.Message)"
    }

    Add-Content -LiteralPath $SummaryPath -Value ''
}

Test-App -ExeName 'Student.exe'
Test-App -ExeName 'Teacher.exe'

Get-Content -LiteralPath $SummaryPath
