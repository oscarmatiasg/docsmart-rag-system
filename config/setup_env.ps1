# ============================================================================
# Setup AWS Environment Variables from .env file
# Uso: . .\setup_env.ps1    (nota el punto inicial para cargar en sesión actual)
# ============================================================================

$envFile = Join-Path $PSScriptRoot ".env"

if (-not (Test-Path $envFile)) {
    Write-Host "❌ ERROR: Archivo .env no encontrado" -ForegroundColor Red
    Write-Host ""
    Write-Host "Ejecuta primero:" -ForegroundColor Yellow
    Write-Host "  python quick_credentials.py" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

Write-Host "🔧 Cargando credenciales desde .env..." -ForegroundColor Cyan

# Leer y parsear el .env
Get-Content $envFile | ForEach-Object {
    $line = $_.Trim()
    
    # Saltar líneas vacías y comentarios
    if ($line -eq "" -or $line.StartsWith("#")) {
        return
    }
    
    # Parsear línea KEY=VALUE
    if ($line -match "^([^=]+)=(.*)$") {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        
        # Solo exportar variables AWS
        if ($key -like "AWS_*") {
            Set-Item -Path "env:$key" -Value $value
            Write-Host "  ✓ $key" -ForegroundColor Green
        }
    }
}

# Verificar que las credenciales estén cargadas
if (-not $env:AWS_ACCESS_KEY_ID) {
    Write-Host "❌ ERROR: AWS_ACCESS_KEY_ID no encontrado en .env" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Variables de entorno AWS configuradas para esta sesión" -ForegroundColor Green
Write-Host ""
Write-Host "Región actual: $env:AWS_REGION" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ahora puedes ejecutar:" -ForegroundColor Yellow
Write-Host "  terraform plan" -ForegroundColor White
Write-Host "  terraform apply" -ForegroundColor White
Write-Host "  aws s3 ls" -ForegroundColor White
Write-Host ""
