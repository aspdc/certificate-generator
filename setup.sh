#!/bin/bash

# Certificate Generator - Setup Script
# This script helps you set up the certificate generator for the first time

set -e

echo "ASPDC Certificate Generator - Setup Script"
echo "==========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "[OK] Found Python $PYTHON_VERSION"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo ""
    echo "uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "[OK] uv installed successfully"
else
    echo "[OK] uv is already installed"
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d ".venv" ]; then
    uv venv
    echo "[OK] Virtual environment created"
else
    echo "[OK] Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo ""
echo "Installing dependencies..."
source .venv/bin/activate
uv pip install -r deps.txt
echo "[OK] Dependencies installed"

# Create config.py if it doesn't exist
echo ""
if [ ! -f "config.py" ]; then
    echo "Creating config.py from template..."
    cp config.example.py config.py
    echo "[OK] config.py created"
    echo ""
    echo "IMPORTANT: Please edit config.py to configure:"
    echo "   - Template PDF paths"
    echo "   - Font file path"
    echo "   - Name and QR code positions"
    echo "   - Input file paths"
else
    echo "[OK] config.py already exists"
fi

# Create necessary directories
echo ""
echo "Creating output directories..."
mkdir -p "qr_codes" "runner-up" "participants-odoo" "winners"
echo "[OK] Directories created"

# Check for required files
echo ""
echo "Checking for required files..."
echo "Note: File paths are configurable in config.py"
echo "[OK] Setup will create sample input files"

# Create sample input files if they don't exist
echo ""
if [ ! -f "names.txt" ]; then
    echo "Creating sample names.txt..."
    cat > names.txt << 'EOF'
Sample Name 1
Sample Name 2
Sample Name 3
EOF
    echo "[OK] Sample names.txt created (edit before generating certificates)"
fi

if [ ! -f "certi.json" ]; then
    echo "Creating sample certi.json..."
    cat > certi.json << 'EOF'
[
  {
    "name": "Sample Name 1",
    "link": "https://aspdc.vercel.app/verify/sample-name-1"
  },
  {
    "name": "Sample Name 2",
    "link": "https://aspdc.vercel.app/verify/sample-name-2"
  }
]
EOF
    echo "[OK] Sample certi.json created (edit before generating QR codes)"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit config.py to set your template paths, font, and positions"
echo "2. Add your certificate PDF templates at the paths specified in config.py"
echo "3. Add your font file at the path specified in config.py"
echo "4. Update your input file (default: names.txt) with participant names"
echo "5. Update your JSON file (default: certi.json) with verification links (if using QR)"
echo ""
echo "To generate certificates:"
echo "  source .venv/bin/activate"
echo "  python qr.py       # Generate QR codes (if needed)"
echo "  python generate.py # Select 1 (with QR) or 2 (without QR)"
echo ""
echo "See README.md for detailed documentation."
