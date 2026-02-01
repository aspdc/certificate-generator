@echo off
REM Certificate Generator - Setup Script for Windows
REM This script helps you set up the certificate generator for the first time

echo.
echo ASPDC Certificate Generator - Setup Script
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3 is not installed. Please install Python 3.11 or higher.
    pause
    exit /b 1
)

echo [OK] Python is installed

REM Check if uv is installed
uv --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo uv is not installed. Please install it manually:
    echo    powershell -c "irm https://astral.sh/uv/install.ps1 ^| iex"
    echo.
    echo After installing uv, run this script again.
    pause
    exit /b 1
)

echo [OK] uv is already installed

REM Create virtual environment
echo.
echo Creating virtual environment...
if not exist ".venv" (
    uv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Install dependencies
echo.
echo Installing dependencies...
call .venv\Scripts\activate.bat
uv pip install -r deps.txt
echo [OK] Dependencies installed

REM Create config.py if it doesn't exist
echo.
if not exist "config.py" (
    echo Creating config.py from template...
    copy config.example.py config.py
    echo [OK] config.py created
    echo.
    echo IMPORTANT: Please edit config.py to match your setup:
    echo    - Verify template paths ^(c1.pdf, p1.pdf^)
    echo    - Adjust name and QR code positions
    echo    - Check font path
) else (
    echo [OK] config.py already exists
)

REM Create necessary directories
echo.
echo Creating output directories...
if not exist "qr_codes" mkdir qr_codes
if not exist "runner-up" mkdir runner-up
if not exist "participants-odoo" mkdir participants-odoo
if not exist "winners" mkdir winners
echo [OK] Directories created

REM Check for required files
echo.
echo Checking for required files...

set MISSING=0

if not exist "c1.pdf" (
    echo    - c1.pdf ^(certificate template with QR^)
    set MISSING=1
)

if not exist "p1.pdf" (
    echo    - p1.pdf ^(certificate template without QR^)
    set MISSING=1
)

if not exist "Monotype Corsiva\Monotype-Corsiva-Regular.ttf" (
    echo    - Monotype Corsiva\Monotype-Corsiva-Regular.ttf ^(font file^)
    set MISSING=1
)

if %MISSING%==1 (
    echo.
    echo WARNING: Please add the missing files before generating certificates.
) else (
    echo [OK] All required files present
)

REM Create sample input files if they don't exist
echo.
if not exist "names.txt" (
    echo Creating sample names.txt...
    (
        echo Sample Name 1
        echo Sample Name 2
        echo Sample Name 3
    ) > names.txt
    echo [OK] Sample names.txt created ^(edit before generating certificates^)
)

if not exist "certi.json" (
    echo Creating sample certi.json...
    (
        echo [
        echo   {
        echo     "name": "Sample Name 1",
        echo     "link": "https://aspdc.vercel.app/verify/sample-name-1"
        echo   },
        echo   {
        echo     "name": "Sample Name 2",
        echo     "link": "https://aspdc.vercel.app/verify/sample-name-2"
        echo   }
        echo ]
    ) > certi.json
    echo [OK] Sample certi.json created ^(edit before generating QR codes^)
)

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Edit config.py to match your setup
echo 2. Add your certificate PDF templates ^(c1.pdf, p1.pdf^)
echo 3. Ensure font file is in place
echo 4. Update names.txt with actual participant names
echo 5. Update certi.json with actual verification links ^(if using QR codes^)
echo.
echo To generate certificates:
echo   .venv\Scripts\activate.bat
echo   python qr.py       # Generate QR codes ^(if needed^)
echo   python generate.py # Select 1 ^(with QR^) or 2 ^(without QR^)
echo.
echo See README.md for detailed documentation.
echo.
pause
