#!/bin/bash

# MLR-Bench Uninstallation Script for Linux/WSL
# Educational implementation by Dr. Yoram Segal

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="$SCRIPT_DIR/.backup"
ENV_BACKUP="$BACKUP_DIR/environment_backup.txt"

echo "=========================================="
echo "MLR-Bench Uninstallation (Linux/WSL)"
echo "=========================================="
echo ""

# Check if backup exists
if [ ! -f "$ENV_BACKUP" ]; then
    echo "⚠️  No backup found at: $ENV_BACKUP"
    echo "   Proceeding with standard uninstallation..."
    echo ""
fi

# Confirm uninstallation
read -p "Are you sure you want to uninstall MLR-Bench? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Uninstallation cancelled"
    exit 0
fi

echo ""
echo "🗑️  Starting uninstallation..."
echo ""

# Remove virtual environment
if [ -d ".venv" ]; then
    echo "🗑️  Removing virtual environment..."
    rm -rf .venv
    echo "✅ Virtual environment removed"
else
    echo "ℹ️  No virtual environment found"
fi

# Remove from shell RC files
echo ""
echo "🔧 Cleaning shell configuration..."

for RC_FILE in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [ -f "$RC_FILE" ]; then
        if grep -q "MLR-Bench" "$RC_FILE"; then
            # Create backup
            cp "$RC_FILE" "$RC_FILE.mlr-backup"
            
            # Remove MLR-Bench lines
            sed -i '/# MLR-Bench/,+2d' "$RC_FILE" 2>/dev/null || \
            sed -i.bak '/# MLR-Bench/,+2d' "$RC_FILE"
            
            echo "✅ Cleaned $RC_FILE (backup: $RC_FILE.mlr-backup)"
        fi
    fi
done

# Ask about data removal
echo ""
read -p "Remove results and workspaces? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Removing data directories..."
    rm -rf results workspaces logs
    echo "✅ Data directories removed"
else
    echo "ℹ️  Keeping data directories"
fi

# Ask about .env removal
echo ""
read -p "Remove .env file (contains API keys)? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f ".env" ]; then
        # Backup .env
        cp .env "$BACKUP_DIR/env_backup_$(date +%Y%m%d_%H%M%S).txt"
        rm .env
        echo "✅ .env removed (backup in $BACKUP_DIR)"
    fi
else
    echo "ℹ️  Keeping .env file"
fi

# Show environment restoration info
echo ""
echo "=========================================="
echo "📋 Environment Restoration"
echo "=========================================="
echo ""

if [ -f "$ENV_BACKUP" ]; then
    echo "Your original environment was backed up to:"
    echo "  $ENV_BACKUP"
    echo ""
    echo "To restore PATH manually, check the backup file."
    echo ""
    
    # Show original PATH
    if grep -q "^PATH=" "$ENV_BACKUP"; then
        echo "Original PATH:"
        grep "^PATH=" "$ENV_BACKUP" | cut -d'=' -f2-
    fi
else
    echo "No environment backup found."
fi

echo ""
echo "=========================================="
echo "✅ Uninstallation Complete!"
echo "=========================================="
echo ""
echo "📝 Notes:"
echo "- Virtual environment removed"
echo "- Shell configuration cleaned"
echo "- Backup files preserved in: $BACKUP_DIR"
echo ""
echo "To reinstall, run: ./install_linux.sh"
echo "=========================================="
