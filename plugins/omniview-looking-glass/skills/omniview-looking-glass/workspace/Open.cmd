@echo off
setlocal
where py >nul 2>nul
if %errorlevel% equ 0 (py -3 "%~dp0host.py") else (python "%~dp0host.py")
if errorlevel 1 pause
