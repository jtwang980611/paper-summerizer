# PowerShell启动脚本
# 设置UTF-8编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 切换到项目根目录
Set-Location (Split-Path -Parent $PSScriptRoot)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   PDF论文总结工具启动脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Python是否安装
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[检测] Python版本: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[错误] 未检测到Python，请先安装Python 3.8+" -ForegroundColor Red
    pause
    exit 1
}

# 检查虚拟环境
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "[检测到虚拟环境] 正在激活..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
} else {
    Write-Host "[提示] 未检测到虚拟环境" -ForegroundColor Yellow
    Write-Host "建议创建虚拟环境以避免依赖冲突" -ForegroundColor Yellow
    Write-Host ""

    $response = Read-Host "是否现在创建虚拟环境? (y/n)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        Write-Host "[创建虚拟环境中...]" -ForegroundColor Cyan
        python -m venv venv

        if ($LASTEXITCODE -eq 0) {
            Write-Host "[虚拟环境已创建]" -ForegroundColor Green
            & "venv\Scripts\Activate.ps1"
            Write-Host "[虚拟环境已激活]" -ForegroundColor Green
        } else {
            Write-Host "[警告] 虚拟环境创建失败，将在当前环境中安装" -ForegroundColor Yellow
        }
    }
}

# 检查依赖
Write-Host ""
Write-Host "[1/3] 检查依赖..." -ForegroundColor Cyan

try {
    python -c "import gradio" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Gradio未安装"
    }
    Write-Host "[2/3] 依赖已安装" -ForegroundColor Green
} catch {
    Write-Host "[2/3] 安装依赖包..." -ForegroundColor Cyan
    pip install -r requirements.txt

    if ($LASTEXITCODE -ne 0) {
        Write-Host "[错误] 依赖安装失败" -ForegroundColor Red
        pause
        exit 1
    }
    Write-Host "[依赖安装完成]" -ForegroundColor Green
}

# 启动应用
Write-Host "[3/3] 启动应用..." -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " 应用将在浏览器中打开" -ForegroundColor Green
Write-Host " 访问地址: http://localhost:7860" -ForegroundColor Green
Write-Host " 按 Ctrl+C 停止应用" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "[启动应用 - 支持 OpenAI / Gemini / Claude 等多种API]" -ForegroundColor Green
Write-Host ""

python app.py
