@echo off
setlocal
powershell -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "%~dp0Setup Windows Launcher.ps1"
if errorlevel 1 (echo OmniView shortcut setup failed. The camera can still be opened below.)
where py >nul 2>nul
if %errorlevel% equ 0 (py -3 "%~dp0host.py" %*) else (python "%~dp0host.py" %*)
if errorlevel 1 pause
