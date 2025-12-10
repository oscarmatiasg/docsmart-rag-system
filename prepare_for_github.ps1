# DocSmart RAG System - GitHub Preparation Script
# Run this before pushing to GitHub

Write-Host "🚀 DocSmart - GitHub Preparation Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the correct directory
if (-not (Test-Path ".\README.md")) {
    Write-Host "❌ Error: Please run this script from the docsmart-rag-system root directory" -ForegroundColor Red
    exit 1
}

Write-Host "✅ In correct directory" -ForegroundColor Green

# 1. Check for sensitive files
Write-Host "`n📝 Checking for sensitive files..." -ForegroundColor Yellow

$sensitiveFiles = @(
    ".env",
    "stack1\terraform.tfvars",
    "stack2\terraform.tfvars",
    "*.tfstate",
    "*.tfstate.backup"
)

$foundSensitive = $false
foreach ($pattern in $sensitiveFiles) {
    $files = Get-ChildItem -Path . -Filter $pattern -Recurse -ErrorAction SilentlyContinue
    if ($files) {
        Write-Host "   ⚠️  Found sensitive file(s): $pattern" -ForegroundColor Red
        $foundSensitive = $true
    }
}

if (-not $foundSensitive) {
    Write-Host "   ✅ No sensitive files found in git" -ForegroundColor Green
}

# 2. Verify .gitignore exists
Write-Host "`n📝 Checking .gitignore..." -ForegroundColor Yellow
if (Test-Path ".\.gitignore") {
    Write-Host "   ✅ .gitignore exists" -ForegroundColor Green
    
    # Check critical entries
    $gitignore = Get-Content .\.gitignore
    $criticalEntries = @(".env", "*.tfvars", "*.tfstate", "venv/")
    $missing = @()
    
    foreach ($entry in $criticalEntries) {
        if ($gitignore -notmatch [regex]::Escape($entry)) {
            $missing += $entry
        }
    }
    
    if ($missing.Count -eq 0) {
        Write-Host "   ✅ All critical entries present" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Missing entries: $($missing -join ', ')" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ❌ .gitignore not found!" -ForegroundColor Red
}

# 3. Check required files
Write-Host "`n📝 Checking required files..." -ForegroundColor Yellow

$requiredFiles = @(
    "README.md",
    "LICENSE",
    "requirements.txt",
    ".env.example",
    "app_demo.py",
    "bedrock_utils.py",
    "DEPLOYMENT_GUIDE.md",
    "stack1\terraform.tfvars.example",
    "stack2\terraform.tfvars.example"
)

$missingFiles = @()
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "   ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $file" -ForegroundColor Red
        $missingFiles += $file
    }
}

# 4. Check terraform formatting
Write-Host "`n📝 Formatting Terraform files..." -ForegroundColor Yellow
try {
    terraform -chdir=stack1 fmt
    terraform -chdir=stack2 fmt
    Write-Host "   ✅ Terraform files formatted" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Terraform not found or error formatting" -ForegroundColor Yellow
}

# 5. Check Python syntax
Write-Host "`n📝 Checking Python syntax..." -ForegroundColor Yellow
$pythonFiles = Get-ChildItem -Path . -Filter "*.py" -Recurse -Exclude "venv","__pycache__"
$pythonErrors = 0

foreach ($file in $pythonFiles) {
    try {
        python -m py_compile $file.FullName 2>$null
    } catch {
        Write-Host "   ❌ Syntax error in $($file.Name)" -ForegroundColor Red
        $pythonErrors++
    }
}

if ($pythonErrors -eq 0) {
    Write-Host "   ✅ All Python files have valid syntax" -ForegroundColor Green
} else {
    Write-Host "   ❌ Found $pythonErrors file(s) with syntax errors" -ForegroundColor Red
}

# 6. Check git status
Write-Host "`n📝 Checking git status..." -ForegroundColor Yellow
try {
    $gitStatus = git status --short
    if ($gitStatus) {
        Write-Host "   ⚠️  Uncommitted changes found:" -ForegroundColor Yellow
        Write-Host $gitStatus
    } else {
        Write-Host "   ✅ No uncommitted changes" -ForegroundColor Green
    }
} catch {
    Write-Host "   ⚠️  Not a git repository or git not found" -ForegroundColor Yellow
}

# 7. Count screenshots
Write-Host "`n📝 Counting screenshots..." -ForegroundColor Yellow
if (Test-Path ".\screenshots") {
    $screenshots = Get-ChildItem -Path ".\screenshots" -Filter "*.png"
    $count = $screenshots.Count
    Write-Host "   📸 Found $count screenshot(s)" -ForegroundColor $(if ($count -ge 30) { "Green" } else { "Yellow" })
    
    if ($count -lt 30) {
        Write-Host "   ⚠️  Expected 30 screenshots, found only $count" -ForegroundColor Yellow
    } else {
        Write-Host "   ✅ All screenshots present" -ForegroundColor Green
    }
} else {
    Write-Host "   ❌ Screenshots directory not found" -ForegroundColor Red
}

# Summary
Write-Host "`n" + ("=" * 50) -ForegroundColor Cyan
Write-Host "📊 SUMMARY" -ForegroundColor Cyan
Write-Host ("=" * 50) -ForegroundColor Cyan

if ($foundSensitive) {
    Write-Host "⚠️  CRITICAL: Sensitive files detected! Remove before pushing!" -ForegroundColor Red
}

if ($missingFiles.Count -gt 0) {
    Write-Host "⚠️  Missing $($missingFiles.Count) required file(s)" -ForegroundColor Yellow
}

if (-not $foundSensitive -and $missingFiles.Count -eq 0 -and $pythonErrors -eq 0) {
    Write-Host "✅ Repository is ready for GitHub!" -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    Write-Host "  1. Review changes: git status" -ForegroundColor White
    Write-Host "  2. Add files: git add -A" -ForegroundColor White
    Write-Host "  3. Commit: git commit -m 'Final submission - DocSmart RAG System'" -ForegroundColor White
    Write-Host "  4. Push: git push origin main" -ForegroundColor White
} else {
    Write-Host "⚠️  Please fix the issues above before pushing to GitHub" -ForegroundColor Yellow
}

Write-Host "`n✨ Preparation check complete!" -ForegroundColor Cyan
