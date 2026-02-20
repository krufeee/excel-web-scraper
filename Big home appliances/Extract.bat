@echo off
cd /d "%~dp0"

REM create logs and output folders if missing
if not exist logs mkdir logs

REM timestamp for log
for /f %%i in ('powershell -command "Get-Date -format yyyy-MM-dd_HH-mm-ss"') do set datetime=%%i

echo ============================
echo Made by Dolniya Kolio
echo Running scraper...
echo Working Directory: %cd%
echo ============================
echo.

REM 👇 Run Python with output shown in console AND saved to log file
powershell -Command "& { py -u \"%~dp0scraper.py\" 2>&1 | Tee-Object -FilePath 'logs\scraper_%datetime%.log' -Append }"

REM Check if the script failed
if errorlevel 1 (
    echo.
    echo ============================
    echo ERROR: Scraper failed!
    echo Check logs\scraper_%datetime%.log for details
    echo ============================
    pause
    exit /b 1
)

echo.
echo ============================
echo Scraper finished.
echo Log saved in logs\scraper_%datetime%.log
echo ============================
pause