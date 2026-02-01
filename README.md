# Certificate Generator

Generate personalized certificates with optional QR codes for ASPDC events. Supports batch processing, custom fonts, and parallel generation.

## Quick Start

```bash
# Setup
git clone https://github.com/aspdc/certificate-generator.git
cd certificate-generator
./setup.sh  # or setup.bat on Windows

# Configure
cp config.example.py config.py
# Edit config.py with your settings

# Generate
source .venv/bin/activate
python qr.py              # Generate QR codes (if needed)
python certificate.py      # Certificates with QR
python certificates-no-qr.py  # Certificates without QR
python merge_pdfs.py      # Merge all PDFs (optional)
```

## Installation

### Requirements

- Python 3.11+
- uv package manager

### Setup

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# or: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows

# Install dependencies
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e .
```

## Configuration

Copy `config.example.py` to `config.py` and customize:

### Required Settings

```python
# Template PDFs (must exist)
TEMPLATE_PATH_WITH_QR = "./c1.pdf"
TEMPLATE_PATH_NO_QR = "./p1.pdf"

# Font (must exist)
FONT_PATH = "./Monotype Corsiva/Monotype-Corsiva-Regular.ttf"
FONT_NAME = "Monotype Corsiva"

# Name position - adjust to match your template
NAME_POSITION_WITH_QR = (410, 280)  # (x, y) from bottom-left
NAME_POSITION_NO_QR = (410, 280)

# QR position and size
QR_POSITION_X = 228
QR_POSITION_Y = 87
QR_WIDTH = 75
QR_HEIGHT = 75
```

### Optional Settings (with defaults)

```python
# Font styling
FONT_SIZE = 23  # Auto-scales down for long names
FONT_COLOR = (17/255, 74/255, 156/255)  # RGB 0-1 range
MAX_NAME_WIDTH = 500  # Max width before auto-scaling

# Output folders
OUTPUT_FOLDER_WITH_QR = "runner-up"
OUTPUT_FOLDER_NO_QR = "participants-odoo"
QR_FOLDER = "./qr_codes"

# Input files
NAMES_FILE = "./names.txt"
PARTICIPANTS_JSON = "./certi.json"

# QR code settings
OUTPUT_DPI = 300
QR_SIZE_PX = 313
QR_ERROR_CORRECTION = "M"  # L, M, Q, or H
QR_BOX_SIZE = 10
QR_BORDER = 2

# Processing
ENABLE_PARALLEL_PROCESSING = True  # Faster generation
AUTO_TITLE_CASE = True  # Convert names to Title Case

# PDF merging
MERGE_SOURCE_FOLDER = "./participants-odoo"
MERGE_OUTPUT_FILE = "merged_participants_odoo.pdf"
```

## Input Files

**names.txt** - One name per line:

```
John Doe
Jane Smith
```

**certi.json** - For QR codes:

```json
[
  { "name": "John Doe", "link": "https://aspdc.vercel.app/verify/john-doe" },
  { "name": "Jane Smith", "link": "https://aspdc.vercel.app/verify/jane-smith" }
]
```

## Scripts

- `qr.py` - Generate QR codes from certi.json
- `certificate.py` - Generate certificates WITH QR codes
- `certificates-no-qr.py` - Generate certificates WITHOUT QR codes
- `merge_pdfs.py` - Merge all PDFs into one file

## Positioning Guide

PDF coordinates start from **bottom-left** (0,0):

- Open template in PDF editor
- Measure from bottom-left in points (1pt = 1/72 inch)
- Update NAME_POSITION and QR_POSITION in config.py
- Test with one certificate and adjust

## Troubleshooting

| Issue                 | Solution                                      |
| --------------------- | --------------------------------------------- |
| "config.py not found" | `cp config.example.py config.py`              |
| QR codes missing      | Run `python qr.py` first                      |
| Wrong position        | Adjust coordinates in config.py               |
| Font error            | Check FONT_PATH exists                        |
| Names too long        | Increase MAX_NAME_WIDTH or decrease FONT_SIZE |
| Slow generation       | Set ENABLE_PARALLEL_PROCESSING = True         |

---

**Repository**: https://github.com/aspdc/certificate-generator  
**Maintained by**: ASPDC Team
