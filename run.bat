@echo off
cd /d "%~dp0"
py -3 -c "import sys; sys.exit(sys.version_info < (3, 11))" >nul 2>&1
if errorlevel 1 (
  echo Python 3.11 or newer is required. Install it from https://www.python.org/downloads/
  echo Tick "Add python.exe to PATH" in the installer, then double-click run.bat again.
  pause
  exit /b 1
)
py -3 -m pip install -q --no-warn-script-location -r requirements.txt
if errorlevel 1 (
  echo Dependency install failed.
  pause
  exit /b 1
)
if "%GEMINI_API_KEY%"=="" (
  echo Get a free key at https://aistudio.google.com/apikey
  set /p GEMINI_API_KEY=Paste your Gemini API key:
  setx GEMINI_API_KEY "%GEMINI_API_KEY%" >nul
)
echo SnipAI running. Ctrl+Alt+A full screen, Ctrl+Alt+S snip, Ctrl+Alt+H hide, Ctrl+Alt+Q quit.
py -3 snipai.py
pause
