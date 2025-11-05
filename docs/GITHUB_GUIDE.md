# 📦 GitHub 上传和部署指南

本文档介绍如何将项目上传到 GitHub，以及如何从 GitHub 拉取到服务器部署。

## 📋 目录

- [一、上传到 GitHub](#一上传到-github)
- [二、从 GitHub 部署到服务器](#二从-github-部署到服务器)
- [三、更新和维护](#三更新和维护)

---

## 一、上传到 GitHub

### 1.1 需要上传的文件

✅ **应该上传的文件：**

```
paper-summerizer/
├── README.md                 # 项目说明
├── app.py                    # 主应用
├── paper_summarizer.py       # 核心逻辑
├── requirements.txt          # Python依赖
├── .gitignore               # Git忽略规则
├── .env.example             # 环境变量示例
├── Dockerfile               # Docker配置
├── docker-compose.yml       # Docker Compose配置
├── .dockerignore            # Docker忽略规则
├── docs/                    # 文档目录
├── scripts/                 # 启动脚本
├── config/                  # 配置示例
└── summaries/.gitkeep       # 保留空目录
```

❌ **不应该上传的文件（已在 .gitignore 中）：**

- `config.json` - 包含 API 密钥（敏感信息）
- `.env` - 环境变量（敏感信息）
- `venv/` - 虚拟环境
- `__pycache__/` - Python缓存
- `summaries/*.md` - 生成的摘要文件
- `*.pdf` - PDF文件

### 1.2 创建 GitHub 仓库

**在 GitHub 网站上：**

1. 登录 GitHub
2. 点击右上角 `+` → `New repository`
3. 填写仓库信息：
   - **Repository name**: `paper-summarizer`
   - **Description**: `PDF 论文总结工具 - 支持 OpenAI/Gemini/Claude 等多种 AI API`
   - **Public/Private**: 选择公开或私有
   - ❌ 不要勾选 "Add README"（我们已有 README.md）
4. 点击 `Create repository`

### 1.3 初始化 Git 仓库并上传

**在项目目录中执行：**

```bash
# 进入项目目录
cd paper-summerizer

# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 查看将要提交的文件
git status

# 提交
git commit -m "Initial commit: PDF论文总结工具"

# 关联远程仓库（替换为你的 GitHub 用户名和仓库名）
git remote add origin https://github.com/你的用户名/paper-summarizer.git

# 推送到 GitHub
git push -u origin main
```

如果 Git 默认分支是 `master` 而不是 `main`：

```bash
# 重命名分支为 main
git branch -M main

# 推送
git push -u origin main
```

### 1.4 验证上传

访问你的 GitHub 仓库页面，应该能看到所有文件已成功上传。

---

## 二、从 GitHub 部署到服务器

### 2.1 前置准备

**服务器要求：**
- Linux 服务器（Ubuntu/CentOS/Debian）
- 已安装 Docker 和 Docker Compose
- 已开放 7860 端口

如未安装 Docker，查看：[服务器部署指南](SERVER_DEPLOYMENT.md)

### 2.2 方法一：一键部署（推荐）

**在服务器上执行：**

```bash
# 克隆仓库
git clone https://github.com/你的用户名/paper-summarizer.git
cd paper-summarizer

# 运行部署脚本
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

部署脚本会自动：
- ✅ 检查 Docker 环境
- ✅ 构建 Docker 镜像
- ✅ 启动容器
- ✅ 显示访问地址

### 2.3 方法二：手动部署

**步骤详解：**

```bash
# 1. 克隆仓库
git clone https://github.com/你的用户名/paper-summarizer.git
cd paper-summarizer

# 2. （可选）创建配置文件
cp config/config.example.json config.json
# 编辑 config.json 填入你的 API 配置

# 3. 使用 Docker Compose 启动
docker-compose up -d

# 4. 查看日志
docker-compose logs -f

# 5. 检查状态
docker-compose ps
```

### 2.4 方法三：使用 Git + 自动部署

**设置 SSH 密钥（可选，避免每次输入密码）：**

```bash
# 生成 SSH 密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 查看公钥
cat ~/.ssh/id_ed25519.pub

# 将公钥添加到 GitHub：
# GitHub → Settings → SSH and GPG keys → New SSH key
```

**使用 SSH 方式克隆：**

```bash
git clone git@github.com:你的用户名/paper-summarizer.git
cd paper-summarizer
./scripts/deploy.sh
```

### 2.5 验证部署

**检查容器状态：**

```bash
docker-compose ps
```

应该看到类似输出：
```
NAME                 STATUS          PORTS
paper-summarizer     Up 2 minutes    0.0.0.0:7860->7860/tcp
```

**访问应用：**

```bash
# 获取服务器 IP
curl ifconfig.me

# 在浏览器中访问
# http://你的服务器IP:7860
```

---

## 三、更新和维护

### 3.1 本地更新后推送到 GitHub

```bash
# 添加修改的文件
git add .

# 提交
git commit -m "更新说明"

# 推送到 GitHub
git push
```

### 3.2 服务器拉取最新代码

```bash
# SSH 登录服务器
ssh user@your-server

# 进入项目目录
cd paper-summarizer

# 拉取最新代码
git pull

# 重新部署
docker-compose down
docker-compose up -d --build
```

### 3.3 自动化更新脚本

创建更新脚本 `scripts/update.sh`：

```bash
#!/bin/bash
# 服务器更新脚本

cd ~/paper-summarizer

echo "正在拉取最新代码..."
git pull

echo "重新构建并启动容器..."
docker-compose down
docker-compose up -d --build

echo "更新完成！"
docker-compose ps
```

使用：

```bash
chmod +x scripts/update.sh
./scripts/update.sh
```

---

## 四、常见问题

### 4.1 首次部署后如何配置 API？

两种方式：

**方式一：通过 Web 界面配置**
1. 访问 `http://服务器IP:7860`
2. 在界面中填写 API 配置
3. 勾选"保存配置"
4. 配置会保存到 `config.json`

**方式二：手动创建配置文件**
```bash
# 复制示例文件
cp config/config.example.json config.json

# 编辑配置
nano config.json

# 重启容器
docker-compose restart
```

### 4.2 如何保护 API 密钥？

✅ **正确做法：**
- 使用 `.gitignore` 排除 `config.json` 和 `.env`
- 在服务器上手动创建这些文件
- 不要在代码中硬编码 API 密钥

❌ **错误做法：**
- 将包含真实 API 密钥的文件提交到 Git
- 在公开仓库中暴露密钥

### 4.3 私有仓库 vs 公开仓库

**公开仓库（Public）：**
- ✅ 免费
- ✅ 任何人都可以查看和克隆
- ❌ 必须小心不要提交敏感信息

**私有仓库（Private）：**
- ✅ 只有你授权的人可以访问
- ✅ 更安全
- ✅ GitHub 免费账户也支持私有仓库

**推荐：** 使用私有仓库，即使如此也要确保 `.gitignore` 正确配置。

### 4.4 克隆私有仓库需要认证

**使用 Personal Access Token：**

1. GitHub → Settings → Developer settings → Personal access tokens → Generate new token
2. 选择权限：`repo`（完整仓库访问权限）
3. 生成并复制 token
4. 克隆时使用：
   ```bash
   git clone https://TOKEN@github.com/用户名/仓库名.git
   ```

或配置 Git 凭据：
```bash
git config --global credential.helper store
git clone https://github.com/用户名/仓库名.git
# 输入用户名和 token（作为密码）
```

### 4.5 如何管理多个服务器？

**使用 Git 分支：**

```bash
# 创建生产环境分支
git checkout -b production

# 创建测试环境分支
git checkout -b staging

# 不同服务器拉取不同分支
git clone -b production https://github.com/用户名/仓库名.git
```

---

## 五、完整部署流程示例

### 场景：从零开始部署到阿里云服务器

**第一步：在 GitHub 创建仓库并上传代码**

```bash
# 本地电脑
cd paper-summerizer
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/你的用户名/paper-summarizer.git
git push -u origin main
```

**第二步：购买并配置服务器**

1. 购买阿里云 ECS（1核2G即可）
2. 选择 Ubuntu 20.04 系统
3. 在安全组开放 7860 端口

**第三步：SSH 登录服务器**

```bash
# 本地电脑
ssh root@你的服务器IP
```

**第四步：安装 Docker**

```bash
# 在服务器上
curl -fsSL https://get.docker.com | sh
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

**第五步：克隆并部署**

```bash
# 在服务器上
cd ~
git clone https://github.com/你的用户名/paper-summarizer.git
cd paper-summarizer
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

**第六步：访问应用**

```bash
# 获取服务器 IP
curl ifconfig.me

# 在浏览器访问
# http://你的IP:7860
```

**第七步：配置 API**

在 Web 界面中：
1. 选择 API 提供商（如 Gemini）
2. 输入 API 密钥
3. 输入 Base URL
4. 勾选"保存配置"
5. 上传 PDF 测试

---

## 六、最佳实践

### ✅ 推荐做法

1. **使用私有仓库** - 更安全
2. **定期备份 `config.json`** - 避免配置丢失
3. **使用环境变量** - 更灵活的配置方式
4. **编写 README** - 记录部署步骤和注意事项
5. **使用 Git 标签** - 标记稳定版本
   ```bash
   git tag -a v1.0.0 -m "第一个稳定版本"
   git push origin v1.0.0
   ```

### ❌ 避免做法

1. ❌ 提交包含 API 密钥的文件
2. ❌ 提交虚拟环境 `venv/`
3. ❌ 提交生成的摘要文件
4. ❌ 在公开仓库中存储敏感信息
5. ❌ 不写 `.gitignore`

---

## 七、相关文档

- 📘 [服务器部署指南](SERVER_DEPLOYMENT.md) - 详细的服务器部署步骤
- 📗 [Docker 部署指南](DOCKER.md) - Docker 使用说明
- 📙 [快速开始](QUICKSTART.md) - 本地开发指南
- 📕 [主文档](../README.md) - 项目说明

---

## 八、获取帮助

如遇到问题：

1. 查看项目 Issues：https://github.com/你的用户名/paper-summarizer/issues
2. 查看 Docker 日志：`docker-compose logs`
3. 查看服务器部署指南：[SERVER_DEPLOYMENT.md](SERVER_DEPLOYMENT.md)
