#!/bin/bash
# Startup script for XLIFF Localization Translator

echo "🌍 XLIFF Localization Translator"
echo "=================================="
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Check if dependencies are installed
echo ""
echo "Checking dependencies..."

if python3 -c "import deep_translator" 2>/dev/null; then
    echo "✓ deep-translator installed"
else
    echo "⚠ deep-translator not found. Installing..."
    pip3 install -r requirements.txt
fi

if python3 -c "import lxml" 2>/dev/null; then
    echo "✓ lxml installed"
else
    echo "⚠ lxml not found. Installing..."
    pip3 install -r requirements.txt
fi

echo ""
echo "Starting GUI application..."
echo ""

# Launch the GUI
python3 localization_app.py
