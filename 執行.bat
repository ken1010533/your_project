@echo off
:: 檢查是否有管理員權限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 需要管理員權限，正在請求提升權限...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

python main.py 