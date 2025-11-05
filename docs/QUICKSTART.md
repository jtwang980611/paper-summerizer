# 快速开始指南

## 5分钟上手使用

### 1️⃣ 创建虚拟环境（推荐）

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

### 3️⃣ 启动应用

**Windows用户：**
```bash
scripts\run.bat
```

**Linux/Mac用户：**
```bash
bash scripts/run.sh
```

或直接运行：
```bash
python app.py
```

### 4️⃣ 使用Web界面

1. 浏览器自动打开 `http://localhost:7860`
2. 配置API：
   - **选择API提供商**: OpenAI / Gemini / Claude / 自定义
   - **API密钥**: 输入你的API密钥
   - **API基础URL**: 根据选择的提供商，系统会自动提示
   - **模型名称**: 会根据提供商自动推荐，也可自定义

3. 上传PDF文件（支持多选）

4. 点击"开始总结"按钮

5. 等待处理完成，查看结果

### 5️⃣ 下载结果

生成的Markdown文件会自动保存在当前目录，文件名格式：
```
summaries_YYYYMMDD_HHMMSS.md
```

## 命令行快速使用

如果你更喜欢命令行：

```bash
# 设置API密钥
export OPENAI_API_KEY="sk-your-api-key"

# 处理论文
python paper_summarizer.py --folder ./papers --output results.md
```

## 自定义Prompt

在Web界面的"自定义Prompt模板"文本框中修改prompt，或者：

1. 编辑 `config/prompt_template.txt` 文件
2. 使用命令行参数：
   ```bash
   python paper_summarizer.py --folder ./papers --prompt my_prompt.txt
   ```

## 常用API配置

### OpenAI
```
提供商: OpenAI
API密钥: sk-...
基础URL: https://api.openai.com/v1（可选）
模型: gpt-3.5-turbo
```

### Gemini（通过new_api）
```
提供商: Gemini
API密钥: 你的Gemini密钥
基础URL: https://your-new-api-url/v1（必填）
模型: gemini-pro
```

### Claude（通过new_api）
```
提供商: Claude
API密钥: 你的Claude密钥
基础URL: https://your-api-url/v1（必填）
模型: claude-3-sonnet
```

### 自定义API
在界面中选择"自定义"，然后填入相应的配置

## 提示

- ✅ 勾选"保存配置"可以在下次启动时自动加载
- ✅ 支持批量处理，一次上传多个PDF
- ✅ Prompt中必须包含 `{content}` 占位符
- ✅ 建议PDF文件不要太大（<50页）

## 遇到问题？

查看 [README.md](../README.md) 的"常见问题"部分。
