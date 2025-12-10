# ==============================================================================
# Wrapper de Terraform con credenciales AWS automáticas
# Uso: .\terraform.ps1 plan
#      .\terraform.ps1 apply
#      .\terraform.ps1 destroy
# ==============================================================================

param(
    [Parameter(Position=0, Mandatory=$true)]
    [string]$Command,
    
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$RemainingArgs
)

# Colores
$ErrorColor = "Red"
$SuccessColor = "Green"
$InfoColor = "Cyan"
$WarningColor = "Yellow"

Write-Host ""
Write-Host "🔧 Terraform Wrapper - DocSmart RAG System" -ForegroundColor $InfoColor
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

# Verificar que existe .env
$envFile = Join-Path $PSScriptRoot ".env"
if (-not (Test-Path $envFile)) {
    Write-Host "❌ ERROR: Archivo .env no encontrado" -ForegroundColor $ErrorColor
    Write-Host ""
    Write-Host "Ejecuta primero:" -ForegroundColor $WarningColor
    Write-Host "  python quick_credentials.py" -ForegroundColor White
    Write-Host ""
    exit 1
}

# Cargar credenciales desde .env
Write-Host "📥 Cargando credenciales desde .env..." -ForegroundColor $InfoColor
Write-Host "   Archivo: $envFile" -ForegroundColor Gray

$envVars = @{}
$awsKeysFound = 0

Get-Content $envFile -Encoding UTF8 | ForEach-Object {
    $line = $_.Trim()
    if ($line -and -not $line.StartsWith("#") -and $line.Contains("=")) {
        $parts = $line.Split("=", 2)
        if ($parts.Count -eq 2) {
            $key = $parts[0].Trim()
            $value = $parts[1].Trim()
            
            # Solo AWS variables
            if ($key.StartsWith("AWS_")) {
                $envVars[$key] = $value
                [Environment]::SetEnvironmentVariable($key, $value, "Process")
                
                # Mostrar KEY truncada para seguridad
                $displayValue = if ($value.Length -gt 20) { 
                    $value.Substring(0, 20) + "..." 
                } else { 
                    $value 
                }
                Write-Host "  ✓ $key = $displayValue" -ForegroundColor $SuccessColor
                $awsKeysFound++
            }
        }
    }
}

if ($awsKeysFound -eq 0) {
    Write-Host ""
    Write-Host "❌ ERROR: No se encontraron credenciales AWS en .env" -ForegroundColor $ErrorColor
    Write-Host ""
    Write-Host "El archivo .env debe contener:" -ForegroundColor $WarningColor
    Write-Host "  AWS_ACCESS_KEY_ID=..." -ForegroundColor White
    Write-Host "  AWS_SECRET_ACCESS_KEY=..." -ForegroundColor White
    Write-Host "  AWS_SESSION_TOKEN=..." -ForegroundColor White
    Write-Host "  AWS_REGION=..." -ForegroundColor White
    Write-Host ""
    Write-Host "Ejecuta: python quick_credentials.py" -ForegroundColor $InfoColor
    Write-Host ""
    exit 1
}

# Verificar credenciales cargadas
if (-not $env:AWS_ACCESS_KEY_ID) {
    Write-Host ""
    Write-Host "❌ ERROR: No se pudieron cargar las credenciales AWS" -ForegroundColor $ErrorColor
    Write-Host ""
    Write-Host "Verifica que el archivo .env contiene:" -ForegroundColor $WarningColor
    Write-Host "  - AWS_ACCESS_KEY_ID" -ForegroundColor White
    Write-Host "  - AWS_SECRET_ACCESS_KEY" -ForegroundColor White
    Write-Host "  - AWS_SESSION_TOKEN" -ForegroundColor White
    Write-Host "  - AWS_REGION" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "✅ Credenciales AWS cargadas correctamente" -ForegroundColor $SuccessColor
Write-Host "   Región: $env:AWS_REGION" -ForegroundColor $InfoColor
Write-Host ""

# Cambiar a directorio stack1 si existe
$stack1Path = Join-Path $PSScriptRoot "stack1"
if (Test-Path $stack1Path) {
    Write-Host "📂 Cambiando a directorio: stack1" -ForegroundColor $InfoColor
    Set-Location $stack1Path
    Write-Host ""
}

# Construir comando terraform
$terraformCmd = "terraform $Command"
if ($RemainingArgs) {
    $terraformCmd += " " + ($RemainingArgs -join " ")
}

Write-Host "🚀 Ejecutando: $terraformCmd" -ForegroundColor $InfoColor
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

# Ejecutar terraform
try {
    Invoke-Expression $terraformCmd
    $exitCode = $LASTEXITCODE
    
    Write-Host ""
    Write-Host "=" * 70 -ForegroundColor Gray
    
    if ($exitCode -eq 0) {
        Write-Host "✅ Comando completado exitosamente" -ForegroundColor $SuccessColor
    } else {
        Write-Host "⚠️  Comando terminó con código de salida: $exitCode" -ForegroundColor $WarningColor
    }
    
    Write-Host ""
    exit $exitCode
    
} catch {
    Write-Host ""
    Write-Host "=" * 70 -ForegroundColor Gray
    Write-Host "❌ ERROR: $_" -ForegroundColor $ErrorColor
    Write-Host ""
    exit 1
}
