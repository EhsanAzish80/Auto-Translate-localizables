#!/bin/bash
# Installation and setup script for auto-translate-localizables

set -e

echo "🚀 Setting up auto-translate-localizables..."
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python $PYTHON_VERSION found"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is required"
    exit 1
fi

echo "✓ pip found"

# Install package in editable mode
echo ""
echo "📦 Installing package in development mode..."
pip3 install -e .

echo ""
echo "✅ Installation complete!"
echo ""
echo "Try it out:"
echo "  auto-translate-xcloc --version"
echo "  auto-translate-xcloc --list-languages"
echo ""
echo "For help:"
echo "  auto-translate-xcloc --help"
echo ""
