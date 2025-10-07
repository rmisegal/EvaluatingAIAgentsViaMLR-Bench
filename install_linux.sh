#!/bin/bash

# MLR-Bench Installation Script for Linux/WSL
# Educational implementation by Dr. Yoram Segal
# All rights reserved - Educational use only

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="$SCRIPT_DIR/.backup"
ENV_BACKUP="$BACKUP_DIR/environment_backup.txt"
INSTALL_LOG="$BACKUP_DIR/install.log"

echo "=========================================="
echo "MLR-Bench Installation (Linux/WSL)"
echo "=========================================="
echo ""

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup current environment
echo "📦 Backing up current environment..."
{
    echo "# MLR-Bench Environment Backup"
    echo "# Date: $(date)"
    echo "# User: $USER"
    echo "# Path: $SCRIPT_DIR"
    echo ""
    echo "## PATH"
    echo "PATH=$PATH"
    echo ""
    echo "## Python"
    which python3 || echo "python3: not found"
    python3 --version 2>&1 || echo "python3: not working"
    echo ""
    echo "## Node.js"
    which node || echo "node: not found"
    node --version 2>&1 || echo "node: not working"
    echo ""
    echo "## Environment Variables"
    env | grep -E "(GOOGLE_API_KEY|BRAVE_API_KEY|PYTHONPATH)" || echo "No MLR-related env vars"
} > "$ENV_BACKUP"

echo "✅ Environment backed up to: $ENV_BACKUP"
echo "" | tee -a "$INSTALL_LOG"

# Function to check Python version
check_python_version() {
    local cmd=$1
    if command -v "$cmd" &> /dev/null; then
        local version=$($cmd --version 2>&1 | grep -oP 'Python \K[0-9]+\.[0-9]+\.[0-9]+' || echo "")
        if [ -n "$version" ]; then
            local major=$(echo "$version" | cut -d. -f1)
            local minor=$(echo "$version" | cut -d. -f2)
            echo "$cmd|$version|$major|$minor"
        fi
    fi
}

# Find all available Python versions
echo "🔍 Searching for Python installations..." | tee -a "$INSTALL_LOG"

PYTHON_VERSIONS=()
for cmd in python3.13 python3.12 python3.11 python3.10 python3.9 python3 python; do
    result=$(check_python_version "$cmd")
    if [ -n "$result" ]; then
        # Check if version not already in list
        version=$(echo "$result" | cut -d'|' -f2)
        if ! printf '%s\n' "${PYTHON_VERSIONS[@]}" | grep -q "|$version|"; then
            PYTHON_VERSIONS+=("$result")
            echo "   Found: $cmd -> Python $version" | tee -a "$INSTALL_LOG"
        fi
    fi
done

if [ ${#PYTHON_VERSIONS[@]} -eq 0 ]; then
    echo "❌ No Python installation found!" | tee -a "$INSTALL_LOG"
    echo "" | tee -a "$INSTALL_LOG"
    echo "Please install Python 3.11 or higher:" | tee -a "$INSTALL_LOG"
    echo "   Ubuntu/Debian: sudo apt install python3.11 python3.11-venv" | tee -a "$INSTALL_LOG"
    echo "   Fedora/RHEL: sudo dnf install python3.11" | tee -a "$INSTALL_LOG"
    echo "   Or download from: https://www.python.org/downloads/" | tee -a "$INSTALL_LOG"
    echo "" | tee -a "$INSTALL_LOG"
    exit 1
fi

# Find best Python version (3.11+)
BEST_PYTHON=""
BEST_VERSION=""
BEST_MAJOR=0
BEST_MINOR=0

for py_info in "${PYTHON_VERSIONS[@]}"; do
    IFS='|' read -r cmd version major minor <<< "$py_info"
    if [ "$major" -eq 3 ] && [ "$minor" -ge 11 ]; then
        if [ "$minor" -gt "$BEST_MINOR" ]; then
            BEST_PYTHON="$cmd"
            BEST_VERSION="$version"
            BEST_MAJOR="$major"
            BEST_MINOR="$minor"
        fi
    fi
done

# If no 3.11+, use highest available
if [ -z "$BEST_PYTHON" ]; then
    for py_info in "${PYTHON_VERSIONS[@]}"; do
        IFS='|' read -r cmd version major minor <<< "$py_info"
        if [ "$major" -gt "$BEST_MAJOR" ] || ([ "$major" -eq "$BEST_MAJOR" ] && [ "$minor" -gt "$BEST_MINOR" ]); then
            BEST_PYTHON="$cmd"
            BEST_VERSION="$version"
            BEST_MAJOR="$major"
            BEST_MINOR="$minor"
        fi
    done
    
    echo "" | tee -a "$INSTALL_LOG"
    echo "⚠️  WARNING: Python 3.11+ required, but found Python $BEST_VERSION" | tee -a "$INSTALL_LOG"
    echo "" | tee -a "$INSTALL_LOG"
    echo "MLR-Bench requires Python 3.11 or higher." | tee -a "$INSTALL_LOG"
    echo "Your current version ($BEST_VERSION) may not work correctly." | tee -a "$INSTALL_LOG"
    echo "" | tee -a "$INSTALL_LOG"
    echo "Options:" | tee -a "$INSTALL_LOG"
    echo "   1. Install Python 3.11+:" | tee -a "$INSTALL_LOG"
    echo "      Ubuntu/Debian: sudo apt install python3.11 python3.11-venv" | tee -a "$INSTALL_LOG"
    echo "      Fedora/RHEL: sudo dnf install python3.11" | tee -a "$INSTALL_LOG"
    echo "   2. Continue anyway (not recommended)" | tee -a "$INSTALL_LOG"
    echo "" | tee -a "$INSTALL_LOG"
    
    read -p "Continue with Python $BEST_VERSION? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled. Please install Python 3.11+" | tee -a "$INSTALL_LOG"
        exit 1
    fi
fi

echo "" | tee -a "$INSTALL_LOG"
echo "✅ Using: $BEST_PYTHON (Python $BEST_VERSION)" | tee -a "$INSTALL_LOG"

# Check Node.js (optional)
echo "" | tee -a "$INSTALL_LOG"
echo "🔍 Checking Node.js (optional)..." | tee -a "$INSTALL_LOG"
if command -v node &> /dev/null; then
    node_version=$(node --version)
    echo "✅ Found Node.js $node_version" | tee -a "$INSTALL_LOG"
else
    echo "⚠️  Node.js not found (optional)" | tee -a "$INSTALL_LOG"
fi

# Create virtual environment
echo "" | tee -a "$INSTALL_LOG"
echo "🐍 Creating virtual environment..." | tee -a "$INSTALL_LOG"
if [ -d ".venv" ]; then
    echo "⚠️  Virtual environment already exists, removing..." | tee -a "$INSTALL_LOG"
    rm -rf .venv
fi

$BEST_PYTHON -m venv .venv
echo "✅ Virtual environment created" | tee -a "$INSTALL_LOG"

# Activate virtual environment
echo "" | tee -a "$INSTALL_LOG"
echo "🔌 Activating virtual environment..." | tee -a "$INSTALL_LOG"
source .venv/bin/activate

# Upgrade pip
echo "" | tee -a "$INSTALL_LOG"
echo "⬆️  Upgrading pip..." | tee -a "$INSTALL_LOG"
pip install --upgrade pip >> "$INSTALL_LOG" 2>&1
echo "✅ pip upgraded" | tee -a "$INSTALL_LOG"

# Install package
echo "" | tee -a "$INSTALL_LOG"
echo "📦 Installing MLR-Bench..." | tee -a "$INSTALL_LOG"
pip install -e . >> "$INSTALL_LOG" 2>&1
echo "✅ MLR-Bench installed" | tee -a "$INSTALL_LOG"

# Install required packages explicitly
echo "" | tee -a "$INSTALL_LOG"
echo "📦 Installing required packages..." | tee -a "$INSTALL_LOG"
pip install loguru google-adk flask flask-socketio aiohttp pydantic python-dotenv >> "$INSTALL_LOG" 2>&1
echo "✅ Required packages installed" | tee -a "$INSTALL_LOG"

# Configure API Keys
echo "" | tee -a "$INSTALL_LOG"
echo "🔑 Configuring API Keys..." | tee -a "$INSTALL_LOG"

if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..." | tee -a "$INSTALL_LOG"
    cp .env.example .env
fi

# Ask for Google API Key
echo ""
echo "=========================================="
echo "Google AI API Key Configuration"
echo "=========================================="
echo ""
echo "MLR-Bench requires a Google AI API Key to function."
echo "Get your free API key from: https://aistudio.google.com/"
echo ""
echo "🔒 SECURITY & PRIVACY:"
echo "   • Your API key will be stored ONLY in the local .env file"
echo "   • The .env file is in .gitignore and will NOT be uploaded to GitHub"
echo "   • Your API key will NOT leave your local machine"
echo "   • You can delete it anytime by running the uninstall script"
echo ""
echo "Press Enter to skip (you can configure it later in .env file)"
echo ""
read -p "Enter your Google AI API Key: " GOOGLE_KEY

if [ -n "$GOOGLE_KEY" ]; then
    # Update .env file
    if grep -q "^GOOGLE_API_KEY=" .env; then
        # Replace existing key
        sed -i "s/^GOOGLE_API_KEY=.*/GOOGLE_API_KEY=$GOOGLE_KEY/" .env
    else
        # Add new key
        echo "GOOGLE_API_KEY=$GOOGLE_KEY" >> .env
    fi
    
    # Also export for current session
    export GOOGLE_API_KEY="$GOOGLE_KEY"
    
    echo "✅ Google API Key configured and saved to .env" | tee -a "$INSTALL_LOG"
    echo "   (stored locally only, not uploaded to GitHub)" | tee -a "$INSTALL_LOG"
else
    echo "⚠️  Google API Key not configured" | tee -a "$INSTALL_LOG"
    echo "   You must edit .env file before running MLR-Bench" | tee -a "$INSTALL_LOG"
fi

# Ask for Brave API Key (optional)
echo ""
echo "=========================================="
echo "Brave Search API Key (Optional)"
echo "=========================================="
echo ""
echo "Brave Search API is optional for enhanced web search."
echo "Get your free API key from: https://brave.com/search/api/"
echo ""
echo "🔒 This key will also be stored locally only in .env file"
echo ""
echo "Press Enter to skip"
echo ""
read -p "Enter your Brave API Key (optional): " BRAVE_KEY

if [ -n "$BRAVE_KEY" ]; then
    if grep -q "^BRAVE_API_KEY=" .env; then
        sed -i "s/^BRAVE_API_KEY=.*/BRAVE_API_KEY=$BRAVE_KEY/" .env
    else
        echo "BRAVE_API_KEY=$BRAVE_KEY" >> .env
    fi
    
    export BRAVE_API_KEY="$BRAVE_KEY"
    echo "✅ Brave API Key configured" | tee -a "$INSTALL_LOG"
else
    echo "ℹ️  Brave API Key not configured (optional)" | tee -a "$INSTALL_LOG"
fi

echo "" | tee -a "$INSTALL_LOG"

# Add to PATH (optional)
echo "" | tee -a "$INSTALL_LOG"
echo "🔧 Configuring PATH..." | tee -a "$INSTALL_LOG"

SHELL_RC=""
if [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
elif [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
fi

if [ -n "$SHELL_RC" ]; then
    if ! grep -q "MLR-Bench" "$SHELL_RC"; then
        echo "" >> "$SHELL_RC"
        echo "# MLR-Bench" >> "$SHELL_RC"
        echo "export PYTHONPATH=\"$SCRIPT_DIR:\$PYTHONPATH\"" >> "$SHELL_RC"
        echo "alias mlr-bench-activate='source $SCRIPT_DIR/.venv/bin/activate'" >> "$SHELL_RC"
        echo "✅ Added to $SHELL_RC" | tee -a "$INSTALL_LOG"
        echo "   Run: source $SHELL_RC" | tee -a "$INSTALL_LOG"
    else
        echo "ℹ️  Already configured in $SHELL_RC" | tee -a "$INSTALL_LOG"
    fi
fi

# Create results and workspaces directories
echo "" | tee -a "$INSTALL_LOG"
echo "📁 Creating directories..." | tee -a "$INSTALL_LOG"
mkdir -p results workspaces logs
echo "✅ Directories created" | tee -a "$INSTALL_LOG"

# Run environment check
echo "" | tee -a "$INSTALL_LOG"
echo "🧪 Running environment check..." | tee -a "$INSTALL_LOG"
python test_environment.py

# Save installation info
{
    echo "# MLR-Bench Installation Info"
    echo "Date: $(date)"
    echo "Script: $SCRIPT_DIR"
    echo "Python: $BEST_PYTHON (Python $BEST_VERSION)"
    echo "Virtual Environment: $SCRIPT_DIR/.venv"
} > "$BACKUP_DIR/install_info.txt"

echo "" | tee -a "$INSTALL_LOG"
echo "=========================================="
echo "✅ Installation Complete!"
echo "=========================================="
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Activate virtual environment:"
echo "   source .venv/bin/activate"
echo ""
echo "2. If you skipped API key configuration, edit .env file:"
echo "   nano .env"
echo "   Add: GOOGLE_API_KEY=your_key_here"
echo "   Get your key from: https://aistudio.google.com/"
echo ""
echo "3. Start visualization server (Terminal 1):"
echo "   python -m mlr_bench.cli.ui_server"
echo ""
echo "4. Run MLR-Bench (Terminal 2):"
echo "   mlr-bench --task-id iclr2025_bi_align"
echo ""
echo "5. Open browser:"
echo "   http://localhost:5000"
echo ""
echo "📝 Installation log: $INSTALL_LOG"
echo "📦 Environment backup: $ENV_BACKUP"
echo ""
echo "🔒 Security Note:"
echo "   Your API keys are stored locally in .env file only"
echo "   They will NOT be uploaded to GitHub (protected by .gitignore)"
echo ""
echo "To uninstall, run: ./uninstall_linux.sh"
echo "=========================================="
