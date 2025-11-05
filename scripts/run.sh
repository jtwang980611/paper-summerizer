#!/bin/bash

# 切换到项目根目录
cd "$(dirname "$0")/.."

echo "========================================"
echo "   PDF论文总结工具启动脚本"
echo "========================================"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python3，请先安装Python 3.8+"
    exit 1
fi

# 检查虚拟环境
if [ -f "venv/bin/activate" ]; then
    echo "[检测到虚拟环境] 正在激活..."
    source venv/bin/activate
else
    echo "[提示] 未检测到虚拟环境"
    echo "建议创建虚拟环境以避免依赖冲突："
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo ""
    read -p "是否现在创建虚拟环境? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "[创建虚拟环境中...]"
        python3 -m venv venv
        if [ $? -ne 0 ]; then
            echo "[警告] 虚拟环境创建失败，将在全局环境中安装"
        else
            source venv/bin/activate
            echo "[虚拟环境已创建并激活]"
        fi
    fi
fi

echo "[1/3] 检查依赖..."
if ! python3 -c "import gradio" &> /dev/null; then
    echo "[2/3] 安装依赖包..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[错误] 依赖安装失败"
        exit 1
    fi
else
    echo "[2/3] 依赖已安装"
fi

echo "[3/3] 启动应用..."
echo ""
echo "========================================"
echo " 应用将在浏览器中打开"
echo " 访问地址: http://localhost:7860"
echo " 按 Ctrl+C 停止应用"
echo "========================================"
echo ""
echo "[启动应用 - 支持 OpenAI / Gemini / Claude 等多种API]"
echo ""

python3 app.py
