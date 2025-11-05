# ✅ GitHub 上传检查清单

在上传到 GitHub 之前，请检查以下项目：

## 🔒 安全检查

- [ ] `config.json` 已添加到 `.gitignore`（包含 API 密钥）
- [ ] `.env` 已添加到 `.gitignore`（包含敏感信息）
- [ ] `.env.example` 已创建（不包含真实密钥）
- [ ] `config/config.example.json` 已创建（不包含真实密钥）
- [ ] 没有在代码中硬编码 API 密钥

## 📦 必须上传的文件

- [ ] `README.md` - 项目说明
- [ ] `app.py` - 主应用
- [ ] `paper_summarizer.py` - 核心逻辑
- [ ] `requirements.txt` - Python 依赖
- [ ] `.gitignore` - Git 忽略规则
- [ ] `.env.example` - 环境变量示例
- [ ] `Dockerfile` - Docker 配置
- [ ] `docker-compose.yml` - Docker Compose 配置
- [ ] `.dockerignore` - Docker 忽略规则
- [ ] `docs/` - 文档目录
- [ ] `scripts/` - 启动脚本
- [ ] `config/` - 配置示例
- [ ] `summaries/.gitkeep` - 保留目录结构

## ❌ 不应上传的文件

- [ ] `config.json` ❌ 包含 API 密钥
- [ ] `.env` ❌ 包含敏感信息
- [ ] `venv/` ❌ 虚拟环境
- [ ] `__pycache__/` ❌ Python 缓存
- [ ] `summaries/*.md` ❌ 生成的摘要
- [ ] `*.pdf` ❌ PDF 文件
- [ ] `*.log` ❌ 日志文件

## 📝 上传前执行

```bash
# 1. 查看将要提交的文件
git status

# 2. 检查是否有敏感文件
git ls-files

# 3. 查看差异
git diff

# 4. 确认无误后提交
git add .
git commit -m "Initial commit"
git push
```

## 🔍 验证上传结果

访问 GitHub 仓库页面，确认：

- [ ] 只看到应该上传的文件
- [ ] 没有 `config.json` 文件
- [ ] 没有 `.env` 文件
- [ ] 没有 `venv/` 目录
- [ ] `summaries/` 目录存在但为空（只有 .gitkeep）

## 📖 相关文档

- [GitHub 上传和部署指南](docs/GITHUB_GUIDE.md)
- [服务器部署指南](docs/SERVER_DEPLOYMENT.md)
