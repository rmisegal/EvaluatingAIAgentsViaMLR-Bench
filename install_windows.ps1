# MLR-Bench Installation Script for Windows PowerShell
# Educational implementation by Dr. Yoram Segal
# All rights reserved - Educational use only

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackupDir = Join-Path $ScriptDir ".backup"
$EnvBackup = Join-Path $BackupDir "environment_backup.txt"
$InstallLog = Join-Path $BackupDir "install.log"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "MLR-Bench Installation (Windows)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Create backup directory
New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null

# Backup current environment
Write-Host "📦 Backing up current environment..." -ForegroundColor Yellow

$backupContent = @"
# MLR-Bench Environment Backup
# Date: $(Get-Date)
# User: $env:USERNAME
# Path: $ScriptDir

## PATH
PATH=$env:PATH

## Python
$(try { python --version 2>&1 } catch { "python: not found" })

## Node.js
$(try { node --version 2>&1 } catch { "node: not found" })

## Environment Variables
GOOGLE_API_KEY=$env:GOOGLE_API_KEY
BRAVE_API_KEY=$env:BRAVE_API_KEY
PYTHONPATH=$env:PYTHONPATH
"@

$backupContent | Out-File -FilePath $EnvBackup -Encoding UTF8
Write-Host "✅ Environment backed up to: $EnvBackup" -ForegroundColor Green
"" | Out-File -Append -FilePath $InstallLog

# Function to check Python version
function Get-PythonVersion {
    param($pythonCmd)
    try {
        $versionOutput = & $pythonCmd --version 2>&1
        if ($versionOutput -match "Python (\d+)\.(\d+)\.(\d+)") {
            return @{
                Command = $pythonCmd
                Major = [int]$Matches[1]
                Minor = [int]$Matches[2]
                Patch = [int]$Matches[3]
                Version = "$($Matches[1]).$($Matches[2]).$($Matches[3])"
            }
        }
    } catch {
        return $null
    }
    return $null
}

# Find all available Python versions
Write-Host "" 
Write-Host "🔍 Searching for Python installations..." -ForegroundColor Yellow

$pythonCommands = @("python", "python3", "python3.11", "python3.12", "python3.13", "py")
$foundPythons = @()

foreach ($cmd in $pythonCommands) {
    $pyInfo = Get-PythonVersion $cmd
    if ($pyInfo -and $pyInfo.Major -ge 3) {
        # Check if not already in list (avoid duplicates)
        $exists = $foundPythons | Where-Object { $_.Version -eq $pyInfo.Version }
        if (-not $exists) {
            $foundPythons += $pyInfo
            Write-Host "   Found: $($pyInfo.Command) -> Python $($pyInfo.Version)" -ForegroundColor Cyan
        }
    }
}

if ($foundPythons.Count -eq 0) {
    Write-Host "❌ No Python installation found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.11 or higher:" -ForegroundColor Yellow
    Write-Host "   1. Download from: https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host "   2. During installation, check 'Add Python to PATH'" -ForegroundColor Cyan
    Write-Host "   3. Restart PowerShell and run this script again" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

# Find best Python version (3.11+)
$bestPython = $foundPythons | Where-Object { $_.Major -eq 3 -and $_.Minor -ge 11 } | Sort-Object -Property Minor -Descending | Select-Object -First 1

if (-not $bestPython) {
    # No Python 3.11+, find highest available
    $bestPython = $foundPythons | Sort-Object -Property Major, Minor -Descending | Select-Object -First 1
    
    Write-Host ""
    Write-Host "⚠️  WARNING: Python 3.11+ required, but found Python $($bestPython.Version)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "MLR-Bench requires Python 3.11 or higher." -ForegroundColor Yellow
    Write-Host "Your current version ($($bestPython.Version)) may not work correctly." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Cyan
    Write-Host "   1. Install Python 3.11+ from: https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host "   2. Continue anyway (not recommended)" -ForegroundColor Cyan
    Write-Host ""
    
    $continue = Read-Host "Continue with Python $($bestPython.Version)? (y/N)"
    if ($continue -ne 'y' -and $continue -ne 'Y') {
        Write-Host "Installation cancelled. Please install Python 3.11+" -ForegroundColor Red
        exit 1
    }
}

$PYTHON_CMD = $bestPython.Command
Write-Host ""
Write-Host "✅ Using: $PYTHON_CMD (Python $($bestPython.Version))" -ForegroundColor Green
"Using: $PYTHON_CMD (Python $($bestPython.Version))" | Out-File -Append -FilePath $InstallLog

# Check Node.js (optional)
Write-Host ""
Write-Host "🔍 Checking Node.js (optional)..." -ForegroundColor Yellow

try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Found Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Node.js not found (optional)" -ForegroundColor Yellow
}

# Create virtual environment
Write-Host ""
Write-Host "🐍 Creating virtual environment..." -ForegroundColor Yellow

$venvPath = Join-Path $ScriptDir ".venv"
if (Test-Path $venvPath) {
    Write-Host "⚠️  Virtual environment already exists, removing..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $venvPath
}

& $PYTHON_CMD -m venv .venv
Write-Host "✅ Virtual environment created" -ForegroundColor Green

# Activate virtual environment
Write-Host ""
Write-Host "🔌 Activating virtual environment..." -ForegroundColor Yellow

$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
& $activateScript

# Upgrade pip
Write-Host ""
Write-Host "⬆️  Upgrading pip..." -ForegroundColor Yellow
& $PYTHON_CMD -m pip install --upgrade pip *>> $InstallLog
Write-Host "✅ pip upgraded" -ForegroundColor Green

# Install package
Write-Host ""
Write-Host "📦 Installing MLR-Bench..." -ForegroundColor Yellow
pip install -e . *>> $InstallLog
Write-Host "✅ MLR-Bench installed" -ForegroundColor Green

# Install Google ADK
Write-Host ""
Write-Host "📦 Installing Google ADK..." -ForegroundColor Yellow
pip install google-adk *>> $InstallLog
Write-Host "✅ Google ADK installed" -ForegroundColor Green

# Install Flask and SocketIO
Write-Host ""
Write-Host "📦 Installing Flask + SocketIO..." -ForegroundColor Yellow
pip install flask flask-socketio aiohttp *>> $InstallLog
Write-Host "✅ Flask + SocketIO installed" -ForegroundColor Green

# Configure API Keys
Write-Host ""
Write-Host "🔑 Configuring API Keys..." -ForegroundColor Yellow

$envFile = Join-Path $ScriptDir ".env"
if (-not (Test-Path $envFile)) {
    Write-Host "📝 Creating .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
}

# Ask for Google API Key
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Google AI API Key Configuration" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "MLR-Bench requires a Google AI API Key to function."
Write-Host "Get your free API key from: https://aistudio.google.com/"
Write-Host ""
Write-Host "🔒 SECURITY & PRIVACY:" -ForegroundColor Green
Write-Host "   • Your API key will be stored ONLY in the local .env file"
Write-Host "   • The .env file is in .gitignore and will NOT be uploaded to GitHub"
Write-Host "   • Your API key will NOT leave your local machine"
Write-Host "   • You can delete it anytime by running the uninstall script"
Write-Host ""
Write-Host "Press Enter to skip (you can configure it later in .env file)"
Write-Host ""

$googleKey = Read-Host "Enter your Google AI API Key"

if ($googleKey) {
    # Update .env file
    $envContent = Get-Content $envFile
    $keyExists = $false
    
    $newContent = $envContent | ForEach-Object {
        if ($_ -match "^GOOGLE_API_KEY=") {
            $keyExists = $true
            "GOOGLE_API_KEY=$googleKey"
        } else {
            $_
        }
    }
    
    if (-not $keyExists) {
        $newContent += "GOOGLE_API_KEY=$googleKey"
    }
    
    $newContent | Out-File -FilePath $envFile -Encoding UTF8
    
    # Set for current session
    $env:GOOGLE_API_KEY = $googleKey
    
    # Set user environment variable (persistent)
    [Environment]::SetEnvironmentVariable("GOOGLE_API_KEY", $googleKey, "User")
    
    Write-Host "✅ Google API Key configured and saved to .env" -ForegroundColor Green
    Write-Host "   (stored locally only, not uploaded to GitHub)" -ForegroundColor Cyan
} else {
    Write-Host "⚠️  Google API Key not configured" -ForegroundColor Yellow
    Write-Host "   You must edit .env file before running MLR-Bench" -ForegroundColor Yellow
}

# Ask for Brave API Key (optional)
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Brave Search API Key (Optional)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Brave Search API is optional for enhanced web search."
Write-Host "Get your free API key from: https://brave.com/search/api/"
Write-Host ""
Write-Host "🔒 This key will also be stored locally only in .env file" -ForegroundColor Green
Write-Host ""
Write-Host "Press Enter to skip"
Write-Host ""

$braveKey = Read-Host "Enter your Brave API Key (optional)"

if ($braveKey) {
    $envContent = Get-Content $envFile
    $keyExists = $false
    
    $newContent = $envContent | ForEach-Object {
        if ($_ -match "^BRAVE_API_KEY=") {
            $keyExists = $true
            "BRAVE_API_KEY=$braveKey"
        } else {
            $_
        }
    }
    
    if (-not $keyExists) {
        $newContent += "BRAVE_API_KEY=$braveKey"
    }
    
    $newContent | Out-File -FilePath $envFile -Encoding UTF8
    
    $env:BRAVE_API_KEY = $braveKey
    [Environment]::SetEnvironmentVariable("BRAVE_API_KEY", $braveKey, "User")
    
    Write-Host "✅ Brave API Key configured" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Brave API Key not configured (optional)" -ForegroundColor Cyan
}

# Add to PATH
Write-Host ""
Write-Host "🔧 Configuring PATH..." -ForegroundColor Yellow

$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -notlike "*$ScriptDir*") {
    $newPath = "$currentPath;$ScriptDir"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "✅ Added to PATH" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Already in PATH" -ForegroundColor Cyan
}

# Set PYTHONPATH
$pythonPath = [Environment]::GetEnvironmentVariable("PYTHONPATH", "User")
if ($pythonPath -notlike "*$ScriptDir*") {
    $newPythonPath = if ($pythonPath) { "$pythonPath;$ScriptDir" } else { $ScriptDir }
    [Environment]::SetEnvironmentVariable("PYTHONPATH", $newPythonPath, "User")
    Write-Host "✅ PYTHONPATH configured" -ForegroundColor Green
}

# Create directories
Write-Host ""
Write-Host "📁 Creating directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "results" | Out-Null
New-Item -ItemType Directory -Force -Path "workspaces" | Out-Null
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
Write-Host "✅ Directories created" -ForegroundColor Green

# Run environment check
Write-Host ""
Write-Host "🧪 Running environment check..." -ForegroundColor Yellow
& $PYTHON_CMD test_environment.py

# Save installation info
$installInfo = @"
# MLR-Bench Installation Info
Date: $(Get-Date)
Script: $ScriptDir
Python: $PYTHON_CMD (Python $($bestPython.Version))
Virtual Environment: $venvPath
"@

$installInfo | Out-File -FilePath (Join-Path $BackupDir "install_info.txt") -Encoding UTF8

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✅ Installation Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Restart PowerShell (to load new PATH)"
Write-Host ""
Write-Host "2. Activate virtual environment:"
Write-Host "   .\.venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. If you skipped API key configuration, edit .env file:"
Write-Host "   notepad .env" -ForegroundColor Cyan
Write-Host "   Add: GOOGLE_API_KEY=your_key_here"
Write-Host "   Get your key from: https://aistudio.google.com/"
Write-Host ""
Write-Host "4. Start visualization server (Terminal 1):"
Write-Host "   python -m mlr_bench.cli.ui_server" -ForegroundColor Cyan
Write-Host ""
Write-Host "5. Run MLR-Bench (Terminal 2):"
Write-Host "   mlr-bench --task-id iclr2025_bi_align" -ForegroundColor Cyan
Write-Host ""
Write-Host "6. Open browser:"
Write-Host "   http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Installation log: $InstallLog" -ForegroundColor Yellow
Write-Host "📦 Environment backup: $EnvBackup" -ForegroundColor Yellow
Write-Host ""
Write-Host "🔒 Security Note:" -ForegroundColor Green
Write-Host "   Your API keys are stored locally in .env file only"
Write-Host "   They will NOT be uploaded to GitHub (protected by .gitignore)"
Write-Host ""
Write-Host "To uninstall, run: .\uninstall_windows.ps1" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan
