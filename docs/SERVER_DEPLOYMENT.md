# 🚀 服务器部署指南

本文档介绍如何在 Linux 服务器上部署 PDF 论文总结工具。

## 📋 前置要求

- Linux 服务器（Ubuntu 20.04+、CentOS 7+、Debian 10+ 等）
- SSH 访问权限
- 至少 2GB 内存
- 至少 5GB 磁盘空间

## 🔧 第一步：安装 Docker

### Ubuntu/Debian

```bash
# 更新软件包索引
sudo apt update

# 安装必要的依赖
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# 添加 Docker 官方 GPG 密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 添加 Docker APT 源
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 更新软件包索引
sudo apt update

# 安装 Docker
sudo apt install -y docker-ce docker-ce-cli containerd.io

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker --version
docker-compose --version
```

### CentOS/RHEL

```bash
# 安装必要的依赖
sudo yum install -y yum-utils

# 添加 Docker 仓库
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 安装 Docker
sudo yum install -y docker-ce docker-ce-cli containerd.io

# 启动 Docker
sudo systemctl start docker
sudo systemctl enable docker

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker --version
docker-compose --version
```

### 配置 Docker 权限（可选）

```bash
# 将当前用户添加到 docker 组，避免每次使用 sudo
sudo usermod -aG docker $USER

# 重新登录以使更改生效
# 或执行
newgrp docker
```

## 📦 第二步：上传项目到服务器

### 方法一：使用 Git（推荐）

```bash
# 在服务器上克隆项目
cd ~
git clone <your-repository-url>
cd paper-summerizer
```

### 方法二：使用 SCP 上传

**在本地电脑上执行：**

```bash
# 打包项目（排除不必要的文件）
tar -czf paper-summerizer.tar.gz \
  --exclude='venv' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='.git' \
  paper-summerizer/

# 上传到服务器
scp paper-summerizer.tar.gz user@your-server-ip:~/

# SSH 到服务器
ssh user@your-server-ip

# 解压
cd ~
tar -xzf paper-summerizer.tar.gz
cd paper-summerizer
```

### 方法三：使用 SFTP/FTP 工具

使用 FileZilla、WinSCP 等工具上传整个项目文件夹。

## 🚀 第三步：启动 Docker 容器

### 基本启动

```bash
# 进入项目目录
cd ~/paper-summerizer

# 使用 Docker Compose 启动
docker-compose up -d

# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 查看启动状态

```bash
# 检查容器是否运行
docker ps

# 应该看到类似输出：
# CONTAINER ID   IMAGE               STATUS          PORTS
# abc123...      paper-summarizer   Up 2 minutes   0.0.0.0:7860->7860/tcp
```

## 🔐 第四步：配置防火墙

### Ubuntu/Debian (UFW)

```bash
# 允许 7860 端口
sudo ufw allow 7860/tcp

# 查看防火墙状态
sudo ufw status
```

### CentOS/RHEL (firewalld)

```bash
# 允许 7860 端口
sudo firewall-cmd --permanent --add-port=7860/tcp
sudo firewall-cmd --reload

# 查看开放的端口
sudo firewall-cmd --list-ports
```

### 云服务器安全组

如果使用阿里云、腾讯云、AWS 等云服务器，还需要在**控制台**的**安全组规则**中开放 7860 端口。

## 🌐 第五步：访问应用

### 通过 IP 访问

```
http://你的服务器IP:7860
```

例如：`http://123.45.67.89:7860`

### 查看服务器 IP

```bash
# 查看公网 IP
curl ifconfig.me

# 或
curl ipinfo.io/ip
```

## ⚙️ 第六步：配置 API（首次使用）

1. 在浏览器中打开 `http://服务器IP:7860`
2. 在 Web 界面中配置：
   - 选择 API 提供商（OpenAI / Gemini / Claude）
   - 输入 API 密钥
   - 配置 Base URL（如果使用 new_api）
   - 勾选"保存配置"
3. 上传 PDF 测试

配置会自动保存到 `config.json`，下次启动自动加载。

## 🔒 生产环境配置（可选但推荐）

### 配置 Nginx 反向代理

**1. 安装 Nginx**

```bash
# Ubuntu/Debian
sudo apt install -y nginx

# CentOS/RHEL
sudo yum install -y nginx
```

**2. 配置反向代理**

创建配置文件：

```bash
sudo nano /etc/nginx/sites-available/paper-summarizer
```

添加以下内容：

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名或 IP

    location / {
        proxy_pass http://127.0.0.1:7860;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 支持大文件上传
        client_max_body_size 100M;
    }
}
```

**3. 启用配置**

```bash
# Ubuntu/Debian
sudo ln -s /etc/nginx/sites-available/paper-summarizer /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx
```

现在可以通过 `http://your-domain.com` 访问（无需 :7860 端口）。

### 配置 HTTPS（强烈推荐）

**使用 Let's Encrypt 免费证书：**

```bash
# 安装 Certbot
sudo apt install -y certbot python3-certbot-nginx  # Ubuntu/Debian
# 或
sudo yum install -y certbot python3-certbot-nginx  # CentOS/RHEL

# 获取证书并自动配置 Nginx
sudo certbot --nginx -d your-domain.com

# 测试自动续期
sudo certbot renew --dry-run
```

现在可以通过 `https://your-domain.com` 安全访问。

## 🔄 常用运维命令

### 查看容器状态

```bash
# 查看运行中的容器
docker ps

# 查看所有容器
docker ps -a

# 查看容器日志
docker-compose logs -f

# 查看最近 100 行日志
docker-compose logs --tail=100
```

### 重启容器

```bash
# 重启
docker-compose restart

# 停止
docker-compose stop

# 启动
docker-compose start

# 停止并删除
docker-compose down
```

### 更新应用

```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker-compose up -d --build

# 或者分步骤
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 备份数据

```bash
# 备份配置文件
cp config.json config.json.backup

# 备份摘要文件
tar -czf summaries_backup_$(date +%Y%m%d).tar.gz summaries/
```

### 查看资源使用

```bash
# 查看容器资源使用
docker stats

# 查看磁盘使用
docker system df

# 清理未使用的资源
docker system prune -a
```

## 🐛 故障排查

### 容器无法启动

```bash
# 查看详细日志
docker-compose logs

# 检查端口是否被占用
sudo netstat -tulnp | grep 7860
# 或
sudo lsof -i :7860
```

### 无法访问 Web 界面

1. **检查容器状态**
   ```bash
   docker ps
   ```

2. **检查防火墙**
   ```bash
   # Ubuntu/Debian
   sudo ufw status

   # CentOS/RHEL
   sudo firewall-cmd --list-all
   ```

3. **检查云服务器安全组**
   - 登录云服务商控制台
   - 检查安全组规则是否开放 7860 端口

4. **测试端口连通性**
   ```bash
   # 在服务器上
   curl http://localhost:7860

   # 在本地电脑上
   telnet 服务器IP 7860
   ```

### 内存不足

编辑 `docker-compose.yml` 限制资源：

```yaml
services:
  paper-summarizer:
    # ... 其他配置
    deploy:
      resources:
        limits:
          memory: 1G
```

### 磁盘空间不足

```bash
# 清理 Docker 资源
docker system prune -a -f

# 清理旧的摘要文件
rm summaries/summaries_2024*.md
```

## 📊 监控和日志

### 设置日志滚动

编辑 `docker-compose.yml`：

```yaml
services:
  paper-summarizer:
    # ... 其他配置
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 使用 systemd 管理（开机自启）

创建服务文件：

```bash
sudo nano /etc/systemd/system/paper-summarizer.service
```

添加内容：

```ini
[Unit]
Description=Paper Summarizer Docker Compose
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/youruser/paper-summerizer
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable paper-summarizer
sudo systemctl start paper-summarizer
```

## 🔐 安全建议

1. **使用防火墙**：只开放必要的端口
2. **配置 HTTPS**：保护数据传输安全
3. **限制访问**：使用 Nginx 配置 IP 白名单
4. **定期更新**：及时更新 Docker 和应用
5. **备份配置**：定期备份 `config.json`
6. **不要暴露 API 密钥**：确保 `config.json` 权限正确

```bash
# 设置配置文件权限
chmod 600 config.json
```

## 📝 快速部署脚本

创建一键部署脚本：

```bash
#!/bin/bash
# deploy.sh

# 进入项目目录
cd ~/paper-summerizer

# 拉取最新代码
git pull

# 停止旧容器
docker-compose down

# 构建新镜像
docker-compose build --no-cache

# 启动容器
docker-compose up -d

# 查看状态
docker-compose ps

echo "部署完成！访问 http://$(curl -s ifconfig.me):7860"
```

使用：

```bash
chmod +x deploy.sh
./deploy.sh
```

## 💡 性能优化建议

1. **使用 SSD 磁盘**：提高 I/O 性能
2. **增加内存**：至少 2GB，推荐 4GB
3. **使用 CDN**：如果有大量用户访问
4. **配置缓存**：在 Nginx 中配置静态资源缓存
5. **限流**：防止 API 滥用

## 📮 需要帮助？

- 查看 [Docker 部署指南](DOCKER.md)
- 查看 [快速开始](QUICKSTART.md)
- 查看主文档 [README.md](../README.md)
