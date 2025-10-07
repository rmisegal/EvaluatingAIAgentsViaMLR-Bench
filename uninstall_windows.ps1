# MLR-Bench Uninstallation Script for Windows PowerShell
# Educational implementation by Dr. Yoram Segal
# All rights reserved - Educational use only

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackupDir = Join-Path $ScriptDir ".backup"
$EnvBackup = Join-Path $BackupDir "environment_backup.txt"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "MLR-Bench Uninstallation (Windows)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if backup exists
if (-not (Test-Path $EnvBackup)) {
    Write-Host "⚠️  No backup found at: $EnvBackup" -ForegroundColor Yellow
    Write-Host "   Proceeding with standard uninstallation..." -ForegroundColor Yellow
    Write-Host ""
}

# Confirm uninstallation
$confirmation = Read-Host "Are you sure you want to uninstall MLR-Bench? (y/N)"
if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
    Write-Host "❌ Uninstallation cancelled" -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "🗑️  Starting uninstallation..." -ForegroundColor Yellow
Write-Host ""

# Remove virtual environment
$venvPath = Join-Path $ScriptDir ".venv"
if (Test-Path $venvPath) {
    Write-Host "🗑️  Removing virtual environment..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $venvPath
    Write-Host "✅ Virtual environment removed" -ForegroundColor Green
} else {
    Write-Host "ℹ️  No virtual environment found" -ForegroundColor Cyan
}

# Remove from PATH
Write-Host ""
Write-Host "🔧 Cleaning PATH..." -ForegroundColor Yellow

$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -like "*$ScriptDir*") {
    $newPath = $currentPath -replace [regex]::Escape(";$ScriptDir"), ""
    $newPath = $newPath -replace [regex]::Escape("$ScriptDir;"), ""
    $newPath = $newPath -replace [regex]::Escape("$ScriptDir"), ""
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "✅ Removed from PATH" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Not found in PATH" -ForegroundColor Cyan
}

# Remove PYTHONPATH
$pythonPath = [Environment]::GetEnvironmentVariable("PYTHONPATH", "User")
if ($pythonPath -like "*$ScriptDir*") {
    $newPythonPath = $pythonPath -replace [regex]::Escape(";$ScriptDir"), ""
    $newPythonPath = $newPythonPath -replace [regex]::Escape("$ScriptDir;"), ""
    $newPythonPath = $newPythonPath -replace [regex]::Escape("$ScriptDir"), ""
    if ($newPythonPath) {
        [Environment]::SetEnvironmentVariable("PYTHONPATH", $newPythonPath, "User")
    } else {
        [Environment]::SetEnvironmentVariable("PYTHONPATH", $null, "User")
    }
    Write-Host "✅ PYTHONPATH cleaned" -ForegroundColor Green
}

# Ask about data removal
Write-Host ""
$removeData = Read-Host "Remove results and workspaces? (y/N)"
if ($removeData -eq 'y' -or $removeData -eq 'Y') {
    Write-Host "🗑️  Removing data directories..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "results", "workspaces", "logs"
    Write-Host "✅ Data directories removed" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Keeping data directories" -ForegroundColor Cyan
}

# Ask about .env removal
Write-Host ""
$removeEnv = Read-Host "Remove .env file (contains API keys)? (y/N)"
if ($removeEnv -eq 'y' -or $removeEnv -eq 'Y') {
    $envFile = Join-Path $ScriptDir ".env"
    if (Test-Path $envFile) {
        # Backup .env
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        Copy-Item $envFile (Join-Path $BackupDir "env_backup_$timestamp.txt")
        Remove-Item $envFile
        Write-Host "✅ .env removed (backup in $BackupDir)" -ForegroundColor Green
    }
    
    # Remove environment variables
    [Environment]::SetEnvironmentVariable("GOOGLE_API_KEY", $null, "User")
    [Environment]::SetEnvironmentVariable("BRAVE_API_KEY", $null, "User")
    Write-Host "✅ API keys removed from environment variables" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Keeping .env file" -ForegroundColor Cyan
}

# Show environment restoration info
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "📋 Environment Restoration" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

if (Test-Path $EnvBackup) {
    Write-Host "Your original environment was backed up to:"
    Write-Host "  $EnvBackup" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To restore PATH manually, check the backup file."
    Write-Host ""
    
    # Show original PATH
    $backupContent = Get-Content $EnvBackup -Raw
    if ($backupContent -match "PATH=(.+)") {
        Write-Host "Original PATH:"
        Write-Host $Matches[1] -ForegroundColor Cyan
    }
} else {
    Write-Host "No environment backup found."
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✅ Uninstallation Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Notes:" -ForegroundColor Yellow
Write-Host "- Virtual environment removed"
Write-Host "- PATH and PYTHONPATH cleaned"
Write-Host "- Backup files preserved in: $BackupDir"
Write-Host ""
Write-Host "⚠️  Please restart PowerShell for changes to take effect" -ForegroundColor Yellow
Write-Host ""
Write-Host "To reinstall, run: .\install_windows.ps1" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
