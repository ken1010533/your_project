
@echo off
net session >nul 2>&1
if %errorLevel% == 0 (
    goto run
) else (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:run
pip install pandas openpyxl requests
pause
