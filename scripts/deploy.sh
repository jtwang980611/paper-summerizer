#!/bin/bash
# 服务器快速部署脚本

set -e  # 遇到错误立即退出

echo "========================================"
echo "  PDF论文总结工具 - 服务器部署脚本"
echo "========================================"
echo ""

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: 未检测到 Docker"
    echo "请先安装 Docker: https://docs.docker.com/engine/install/"
    exit 1
fi

# 检查 Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ 错误: 未检测到 Docker Compose"
    echo "请先安装 Docker Compose"
    exit 1
fi

echo "✅ Docker 和 Docker Compose 已安装"
echo ""

# 切换到项目根目录
cd "$(dirname "$0")/.."

# 停止旧容器（如果存在）
echo "[1/4] 停止旧容器..."
docker-compose down 2>/dev/null || true

# 构建镜像
echo "[2/4] 构建 Docker 镜像..."
docker-compose build --no-cache

# 启动容器
echo "[3/4] 启动容器..."
docker-compose up -d

# 等待容器启动
echo "[4/4] 等待应用启动..."
sleep 5

# 检查容器状态
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "========================================"
    echo "✅ 部署成功！"
    echo "========================================"
    echo ""

    # 尝试获取服务器 IP
    SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || echo "服务器IP")

    echo "访问地址："
    echo "  - 本地: http://localhost:7860"
    echo "  - 外网: http://$SERVER_IP:7860"
    echo ""
    echo "查看日志: docker-compose logs -f"
    echo "停止服务: docker-compose down"
    echo "========================================"
else
    echo ""
    echo "❌ 部署失败，请查看日志："
    docker-compose logs
    exit 1
fi
