# 🐳 Docker 部署指南

本文档介绍如何使用 Docker 运行 PDF 论文总结工具。

> 💡 **服务器部署**：如果需要在远程服务器上部署，请查看 [服务器部署指南](SERVER_DEPLOYMENT.md)

## 📋 前置要求

- Docker 20.10+
- Docker Compose 2.0+（可选，推荐）

## 🚀 快速启动

### 方式一：使用 Docker Compose（推荐）

1. **启动容器**
```bash
docker-compose up -d
```

2. **查看日志**
```bash
docker-compose logs -f
```

3. **访问应用**
打开浏览器访问 `http://localhost:7860`

4. **停止容器**
```bash
docker-compose down
```

### 方式二：使用 Docker 命令

1. **构建镜像**
```bash
docker build -t paper-summarizer .
```

2. **运行容器**
```bash
docker run -d \
  --name paper-summarizer \
  -p 7860:7860 \
  -v $(pwd)/config.json:/app/config.json \
  -v $(pwd)/summaries:/app/summaries \
  paper-summarizer
```

3. **查看日志**
```bash
docker logs -f paper-summarizer
```

4. **停止容器**
```bash
docker stop paper-summarizer
docker rm paper-summarizer
```

## ⚙️ 配置说明

### 环境变量

可以通过环境变量配置 API 密钥（可选）：

**修改 `docker-compose.yml`：**
```yaml
environment:
  - OPENAI_API_KEY=your-api-key-here
```

或创建 `.env` 文件：
```env
OPENAI_API_KEY=your-api-key-here
```

### 数据持久化

Docker Compose 配置了两个数据卷：

1. **配置持久化**
   - 主机路径：`./config.json`
   - 容器路径：`/app/config.json`
   - 作用：保存 API 配置和 Prompt 模板

2. **输出持久化**
   - 主机路径：`./summaries`
   - 容器路径：`/app/summaries`
   - 作用：保存生成的论文摘要文件

### 端口映射

- 默认端口：`7860:7860`
- 修改主机端口：编辑 `docker-compose.yml` 中的 `ports` 配置

```yaml
ports:
  - "8080:7860"  # 将主机 8080 端口映射到容器 7860 端口
```

## 🔧 常用命令

### 查看运行状态
```bash
docker-compose ps
```

### 重启容器
```bash
docker-compose restart
```

### 查看容器日志
```bash
# 实时查看
docker-compose logs -f

# 查看最近 100 行
docker-compose logs --tail=100
```

### 进入容器
```bash
docker-compose exec paper-summarizer bash
```

### 更新容器
```bash
# 停止并删除旧容器
docker-compose down

# 重新构建镜像
docker-compose build --no-cache

# 启动新容器
docker-compose up -d
```

### 清理 Docker 资源
```bash
# 删除停止的容器
docker-compose down

# 删除镜像
docker rmi paper-summarizer

# 清理未使用的资源
docker system prune -a
```

## 🌐 网络访问

### 本地访问
```
http://localhost:7860
```

### 局域网访问
```
http://<你的IP地址>:7860
```

查看本机 IP：
```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
```

## 🔒 安全建议

1. **不要在 Docker 镜像中硬编码 API 密钥**
   - 使用环境变量或挂载配置文件

2. **生产环境部署**
   - 使用反向代理（Nginx）
   - 配置 HTTPS
   - 限制访问 IP

3. **配置文件权限**
```bash
chmod 600 config.json
```

## 📊 资源限制

如需限制容器资源使用，修改 `docker-compose.yml`：

```yaml
services:
  paper-summarizer:
    # ... 其他配置
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          memory: 512M
```

## 🐛 故障排查

### 容器无法启动
```bash
# 查看详细日志
docker-compose logs

# 检查端口占用
netstat -an | grep 7860  # Linux/Mac
netstat -ano | findstr 7860  # Windows
```

### 无法访问 Web 界面
1. 检查容器是否运行：`docker-compose ps`
2. 检查端口映射：`docker-compose port paper-summarizer 7860`
3. 检查防火墙设置

### 配置不保存
确保挂载了 `config.json`：
```bash
docker-compose exec paper-summarizer ls -la /app/config.json
```

## 📝 示例：完整工作流

```bash
# 1. 克隆项目
git clone <repository-url>
cd paper-summerizer

# 2. 启动容器
docker-compose up -d

# 3. 查看日志确认启动成功
docker-compose logs -f

# 4. 在浏览器中访问
# http://localhost:7860

# 5. 使用完毕后停止
docker-compose down
```

## 🔄 更新镜像

当代码更新后：

```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker-compose up -d --build
```

## 💡 提示

- ✅ 首次启动需要下载基础镜像，可能需要几分钟
- ✅ 配置文件保存在主机，不会因容器删除而丢失
- ✅ 生成的摘要文件保存在 `./summaries` 目录
- ✅ 容器默认自动重启（`restart: unless-stopped`）

## 📮 需要帮助？

查看主文档：[README.md](../README.md)
