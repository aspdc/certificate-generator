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
    echo "IMPORTANT: Please edit config.py to match your setup:"
    echo "   - Verify template paths (c1.pdf, p1.pdf)"
    echo "   - Adjust name and QR code positions"
    echo "   - Check font path"
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

MISSING_FILES=()

if [ ! -f "c1.pdf" ]; then
    MISSING_FILES+=("c1.pdf (certificate template with QR)")
fi

if [ ! -f "p1.pdf" ]; then
    MISSING_FILES+=("p1.pdf (certificate template without QR)")
fi

if [ ! -f "Monotype Corsiva/Monotype-Corsiva-Regular.ttf" ]; then
    MISSING_FILES+=("Monotype Corsiva/Monotype-Corsiva-Regular.ttf (font file)")
fi

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo ""
    echo "WARNING: Missing required files:"
    for file in "${MISSING_FILES[@]}"; do
        echo "   - $file"
    done
    echo ""
    echo "Please add these files before generating certificates."
else
    echo "[OK] All required files present"
fi

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
echo "1. Edit config.py to match your setup"
echo "2. Add your certificate PDF templates (c1.pdf, p1.pdf)"
echo "3. Ensure font file is in place"
echo "4. Update names.txt with actual participant names"
echo "5. Update certi.json with actual verification links (if using QR codes)"
echo ""
echo "To generate certificates:"
echo "  source .venv/bin/activate"
echo "  python qr.py       # Generate QR codes (if needed)"
echo "  python generate.py # Select 1 (with QR) or 2 (without QR)"
echo ""
echo "See README.md for detailed documentation."
