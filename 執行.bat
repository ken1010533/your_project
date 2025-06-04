
chcp 65001
@echo off
:: 檢查管理員權限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 需要管理員權限，正在請求提升權限...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: 確認 main.py 存在
if not exist "main.py" (
    echo 找不到 main.py，請確認當前目錄是否正確！
    pause
    exit /b
)

:: 執行 Python 程式
echo 正在執行 Python 程式...
python main.py
if errorlevel 1 (
    echo Python 程式執行失敗，請檢查錯誤訊息。
) else (
    echo Python 程式執行完成。
)

pause
