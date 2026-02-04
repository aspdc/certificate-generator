"""
Configuration file for ASPDC Certificate Generator
Copy this file to config.py and update values as needed.
"""

# ============================================================================
# REQUIRED SETTINGS - Must configure these
# ============================================================================

# PDF Templates (must exist)
TEMPLATE_PATH_WITH_QR = "./c1.pdf"  # Template for certificates with QR codes
TEMPLATE_PATH_NO_QR = "./p1.pdf"    # Template for certificates without QR codes

# Font Configuration (font file must exist)
FONT_PATH = "./Monotype Corsiva/Monotype-Corsiva-Regular.ttf"
FONT_NAME = "Monotype Corsiva"

# Name Position - Adjust to match your template layout
# Coordinates are (x, y) from bottom-left corner in points
NAME_POSITION_WITH_QR = (410, 280)
NAME_POSITION_NO_QR = (410, 280)

# QR Code Position and Size (only for certificates with QR)
QR_POSITION_X = 228
QR_POSITION_Y = 87
QR_WIDTH = 75
QR_HEIGHT = 75

# Serial Number Position (optional - set to None to disable)
SERIAL_NUMBER_POSITION_WITH_QR = (370, 35)  # Default: (370, 35) - set to None to disable
SERIAL_NUMBER_POSITION_NO_QR = (370, 35)  # Default: (370, 35) - set to None to disable
SERIAL_NUMBER_FONT_SIZE = 10  # Default: 10


# ============================================================================
# OPTIONAL SETTINGS - Defaults provided
# ============================================================================

# Font Styling (optional - defaults shown)
FONT_SIZE = 23  # Default: 23 - auto-scales down for long names
FONT_COLOR = (17/255, 74/255, 156/255)  # Default: blue (17, 74, 156) in 0-1 range
MAX_NAME_WIDTH = 500  # Default: 500 points - max width before auto-scaling

# Output Folders (optional - defaults shown)
OUTPUT_FOLDER_WITH_QR = "runner-up"  # Default: "runner-up"
OUTPUT_FOLDER_NO_QR = "participants-odoo"  # Default: "participants-odoo"
QR_FOLDER = "./qr_codes"  # Default: "./qr_codes"

# Input Files (optional - defaults shown)
NAMES_FILE = "./names.txt"  # Default: "./names.txt"
PARTICIPANTS_JSON = "./certi.json"  # Default: "./certi.json"
SERIAL_NUMBERS_FILE = "./sr-no.txt"  # Default: "./sr-no.txt" - one serial number per line

# QR Code Generation (optional - defaults shown)
OUTPUT_DPI = 300  # Default: 300 DPI for print quality
QR_SIZE_PX = 313  # Default: 313 pixels (calculated from QR_WIDTH at 300 DPI)
QR_ERROR_CORRECTION = "M"  # Default: "M" - Options: "L", "M", "Q", "H"
QR_BOX_SIZE = 10  # Default: 10 - size of each QR box
QR_BORDER = 2  # Default: 2 - border size (minimum 4 for spec compliance)

# Processing Options (optional - defaults shown)
ENABLE_PARALLEL_PROCESSING = True  # Default: True - faster generation
AUTO_TITLE_CASE = True  # Default: True - convert names to Title Case

# PDF Merging (optional - defaults shown)
MERGE_SOURCE_FOLDER = "./participants-odoo"  # Default: "./participants-odoo"
MERGE_OUTPUT_FILE = "merged_participants_odoo.pdf"  # Default: "merged_participants_odoo.pdf"

