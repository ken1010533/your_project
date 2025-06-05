chcp 65001

@echo off
:: 檢查是否有管理員權限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 需要管理員權限，正在請求提升權限...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: --- 安裝 Python ---
python --version >nul 2>&1
if errorlevel 1 (
    echo Python 未安裝，開始下載安裝 Python...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe' -OutFile \"$env:TEMP\python-installer.exe\"; Start-Process \"$env:TEMP\python-installer.exe\" -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait; Remove-Item \"$env:TEMP\python-installer.exe\" -Force"
) else (
    echo 已偵測到 Python，版本：
    python --version
)

:: --- 安裝 Git ---
git --version >nul 2>&1
if errorlevel 1 (
    echo Git 未安裝，正在使用 winget 安裝 Git...
    winget install --id Git.Git -e --source winget
    :: 添加 Git 到系統路徑
    setx PATH "%PATH%;C:\Program Files\Git\cmd" /M
    :: 刷新當前會話的環境變量
    for /f "tokens=2,*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path ^| findstr /i "Path"') do set "systempath=%%b"
    set "PATH=%systempath%"
) else (
    echo 已偵測到 Git，版本：
    git --version
)

:: --- 安裝 Python 套件 ---
echo 正在安裝 pandas openpyxl requests 套件...
python -m pip install --upgrade pip
python -m pip install pandas openpyxl requests

:: --- 下載你的專案 ---
set TARGET_DIR=%USERPROFILE%\Desktop\your_project

if exist "%TARGET_DIR%" (
    echo 目標資料夾已存在，跳過 git clone。
) else (
    echo 正在下載你的專案到 %TARGET_DIR% ...
    git clone https://github.com/ken1010533/your_project.git "%TARGET_DIR%"
    if errorlevel 1 (
        echo 下載失敗，請手動執行以下命令：
        echo git clone https://github.com/ken1010533/your_project.git "%TARGET_DIR%"
    )
)

echo 全部安裝與下載完成！
pause