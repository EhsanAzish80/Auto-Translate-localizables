#!/bin/bash
# Setup script for XLIFF Localization Translator

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     XLIFF Localization Translator - Setup                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     PLATFORM=Linux;;
    Darwin*)    PLATFORM=Mac;;
    CYGWIN*)    PLATFORM=Windows;;
    MINGW*)     PLATFORM=Windows;;
    *)          PLATFORM="UNKNOWN:${OS}"
esac

echo "Platform detected: $PLATFORM"
echo ""

# Check Python
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✓ Python 3 found: $PYTHON_VERSION"
    
    # Check version is 3.7+
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 7 ]; then
        echo "✓ Python version is compatible (3.7+)"
    else
        echo "✗ Python 3.7 or higher is required"
        echo "  Current version: $PYTHON_VERSION"
        exit 1
    fi
else
    echo "✗ Python 3 not found!"
    echo "  Please install Python 3.7 or higher from https://www.python.org/"
    exit 1
fi

echo ""

# Check pip
echo "Checking pip..."
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version 2>&1 | awk '{print $2}')
    echo "✓ pip found: $PIP_VERSION"
else
    echo "✗ pip3 not found!"
    echo "  Installing pip..."
    python3 -m ensurepip --upgrade
fi

echo ""

# Install dependencies
echo "Installing dependencies..."
echo "─────────────────────────────────────────────────────────────"

if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    echo ""
    echo "✓ Dependencies installed successfully"
else
    echo "✗ requirements.txt not found!"
    exit 1
fi

echo ""

# Verify installations
echo "Verifying installations..."
echo "─────────────────────────────────────────────────────────────"

if python3 -c "import deep_translator" 2>/dev/null; then
    echo "✓ deep-translator"
else
    echo "✗ deep-translator failed to install"
    exit 1
fi

if python3 -c "import lxml" 2>/dev/null; then
    echo "✓ lxml"
else
    echo "⚠ lxml not available (will use standard xml library)"
fi

# Check Tkinter for GUI
if python3 -c "import tkinter" 2>/dev/null; then
    echo "✓ tkinter (GUI support)"
else
    echo "⚠ tkinter not available (GUI mode will not work)"
    if [ "$PLATFORM" = "Linux" ]; then
        echo "  Install with: sudo apt-get install python3-tk"
    fi
fi

echo ""

# Make scripts executable
if [ "$PLATFORM" != "Windows" ]; then
    echo "Setting script permissions..."
    chmod +x run.sh 2>/dev/null || true
    chmod +x localization_app.py 2>/dev/null || true
    chmod +x translate_xliff.py 2>/dev/null || true
    echo "✓ Scripts are now executable"
    echo ""
fi

# Success message
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              Setup Complete! ✓                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "You can now run the application:"
echo ""
if [ "$PLATFORM" != "Windows" ]; then
    echo "  GUI Mode:     ./run.sh"
    echo "              or  python3 localization_app.py"
else
    echo "  GUI Mode:     python localization_app.py"
fi
echo ""
echo "  CLI Mode:     python3 translate_xliff.py --help"
echo ""
echo "Quick Start:  cat QUICKSTART.md"
echo "Full Guide:   cat README.md"
echo ""
echo "Happy translating! 🌍"
