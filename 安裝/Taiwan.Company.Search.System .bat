chcp 65001
@echo off
:: --- 檢查是否有管理員權限 ---
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 需要管理員權限，正在請求提升權限...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: --- 輸入自訂資料夾名稱 ---
set /p FOLDER_NAME=請輸入要下載的資料夾名稱（預設為 your_project）：
if "%FOLDER_NAME%"=="" (
    set "FOLDER_NAME=your_project"
)

:: --- 安裝 Python ---
python --version >nul 2>&1
if errorlevel 1 (
    echo Python 未安裝，開始下載並安裝 Python...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe' -OutFile \"$env:TEMP\python-installer.exe\"; Start-Process \"$env:TEMP\python-installer.exe\" -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait; Remove-Item \"$env:TEMP\python-installer.exe\" -Force"
) else (
    echo ✅ 已偵測到 Python，版本為：
    python --version
)

:: --- 安裝 Git ---
git --version >nul 2>&1
if errorlevel 1 (
    echo Git 未安裝，正在透過 winget 安裝 Git...
    winget install --id Git.Git -e --source winget
    setx PATH "%PATH%;C:\Program Files\Git\cmd" /M
) else (
    echo ✅ 已偵測到 Git，版本為：
    git --version
)

:: --- 安裝 Python 套件 ---
echo 🔄 正在安裝 Python 套件：pandas、openpyxl、requests...
python -m pip install --upgrade pip
python -m pip install pandas openpyxl requests

:: --- 設定下載路徑為目前資料夾 + 使用者自訂名稱 ---
set "TARGET_DIR=%~dp0%FOLDER_NAME%"

if exist "%TARGET_DIR%" (
    echo 📂 資料夾 %FOLDER_NAME% 已存在，略過 git clone。
) else (
    echo ⬇️ 正在下載專案至：%TARGET_DIR% ...
    git clone https://github.com/ken1010533/your_project.git "%TARGET_DIR%"
    if errorlevel 1 (
        echo ❌ Git clone 失敗，請手動執行：
        echo git clone https://github.com/ken1010533/your_project.git "%TARGET_DIR%"
    )
)

:: --- 加入 Git 安全資料夾白名單 ---
git config --global --add safe.directory "%TARGET_DIR%"
echo ✅ 已將 %TARGET_DIR% 加入 Git 安全白名單

echo 🟢 全部安裝與設定完成！可以開始使用你的專案囉 🎉

