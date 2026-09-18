@echo off
title ARGUS: The Hundred-Eyed Builder Intelligence Engine
cd /d "%~dp0"
echo ======================================================================
echo    ARGUS: The Hundred-Eyed Builder Intelligence Engine
echo ======================================================================
echo  Starting continuous hourly intelligence scanner...
echo  Updates will be sent directly to your Telegram bot every hour.
echo  Press Ctrl+C to stop.
echo ======================================================================
echo.

python -m brain.daemon --continuous
pause
