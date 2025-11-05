#!/bin/bash
# 服务器端一键更新脚本

echo "🔄 开始更新 Paper Summarizer..."

# 进入项目目录（根据实际情况修改）
cd "$(dirname "$0")/.." || exit 1

echo "📥 拉取最新镜像..."
docker compose pull

echo "🔄 重启容器..."
docker compose down
docker compose up -d

echo "✅ 更新完成！"
echo "📊 查看运行状态："
docker compose ps

echo ""
echo "📝 查看日志："
echo "docker compose logs -f"
