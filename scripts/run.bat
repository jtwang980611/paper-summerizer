@echo off
chcp 65001 >nul
echo ========================================
echo    PDF论文总结工具启动脚本
echo ========================================
echo.

REM 切换到项目根目录
cd /d "%~dp0.."

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查虚拟环境
if exist "venv\Scripts\activate.bat" (
    echo [检测到虚拟环境] 正在激活...
    call venv\Scripts\activate.bat
) else (
    echo [提示] 未检测到虚拟环境
    echo 建议创建虚拟环境以避免依赖冲突：
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo.
    choice /C YN /M "是否现在创建虚拟环境"
    if errorlevel 2 goto :skip_venv
    if errorlevel 1 (
        echo [创建虚拟环境中...]
        python -m venv venv
        if %errorlevel% neq 0 (
            echo [警告] 虚拟环境创建失败，将在全局环境中安装
            goto :skip_venv
        )
        call venv\Scripts\activate.bat
        echo [虚拟环境已创建并激活]
    )
)

:skip_venv
echo [1/3] 检查依赖...
pip show gradio >nul 2>&1
if %errorlevel% neq 0 (
    echo [2/3] 安装依赖包...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
) else (
    echo [2/3] 依赖已安装
)

echo [3/3] 启动应用...
echo.
echo ========================================
echo  应用将在浏览器中打开
echo  访问地址: http://localhost:7860
echo  按 Ctrl+C 停止应用
echo ========================================
echo.
echo [启动应用 - 支持 OpenAI / Gemini / Claude 等多种API]
echo.

python app.py

pause
