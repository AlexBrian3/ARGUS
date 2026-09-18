@echo off
title ARGUS Windows Auto-Start Setup
echo ======================================================================
echo    ARGUS: Installing Auto-Start on Windows Boot / Restart
echo ======================================================================
echo.

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SOURCE_FILE=%~dp0argus_background.vbs"

echo Creating shortcut in: %STARTUP_FOLDER%
copy /Y "%SOURCE_FILE%" "%STARTUP_FOLDER%\argus_background.vbs" >nul

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] ARGUS is now installed in your Windows Startup!
    echo Whenever your PC boots up or restarts, ARGUS will automatically
    echo run silently in the background and deliver hourly updates.
    echo.
) else (
    echo.
    echo [ERROR] Could not copy to startup folder. Please run as Administrator.
    echo.
)

pause
