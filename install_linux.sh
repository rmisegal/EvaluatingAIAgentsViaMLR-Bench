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

# Check Python version
echo "🔍 Checking Python version..." | tee -a "$INSTALL_LOG"
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.11+" | tee -a "$INSTALL_LOG"
    echo "   Download from: https://www.python.org/downloads/" | tee -a "$INSTALL_LOG"
    exit 1
fi

python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Found Python $python_version" | tee -a "$INSTALL_LOG"

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

python3 -m venv .venv
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

# Install Google ADK
echo "" | tee -a "$INSTALL_LOG"
echo "📦 Installing Google ADK..." | tee -a "$INSTALL_LOG"
pip install google-adk >> "$INSTALL_LOG" 2>&1
echo "✅ Google ADK installed" | tee -a "$INSTALL_LOG"

# Install Flask and SocketIO
echo "" | tee -a "$INSTALL_LOG"
echo "📦 Installing Flask + SocketIO..." | tee -a "$INSTALL_LOG"
pip install flask flask-socketio aiohttp >> "$INSTALL_LOG" 2>&1
echo "✅ Flask + SocketIO installed" | tee -a "$INSTALL_LOG"

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
python3 test_environment.py

# Save installation info
{
    echo "# MLR-Bench Installation Info"
    echo "Date: $(date)"
    echo "Script: $SCRIPT_DIR"
    echo "Python: $(python3 --version)"
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
