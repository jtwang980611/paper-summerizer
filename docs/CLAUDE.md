# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A PDF paper summarization tool that uses OpenAI-compatible APIs to automatically generate summaries of academic papers. The tool provides both a Gradio web interface and a command-line interface for batch processing.

## Running the Application

### Setup (Virtual Environment Recommended)
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Web Interface (Primary Usage)
```bash
python app.py
```
Launches Gradio interface on `http://localhost:7860`

### Command Line Interface
```bash
python paper_summarizer.py --folder ./papers --output summaries.md
```

Required environment variable or CLI argument: `OPENAI_API_KEY`

**Note**: The `scripts/run.bat` (Windows) and `scripts/run.sh` (Linux/Mac) scripts automatically detect and activate virtual environments, or prompt to create one.

## Architecture

### Two-Component Design

1. **`paper_summarizer.py`** - Core logic module
   - `PaperSummarizer` class: Handles PDF text extraction and API communication
   - Stateless processing: Each paper is processed independently
   - Error handling: Individual paper failures don't stop batch processing
   - Content truncation: Limits text to 8000 characters before API call to avoid token limits

2. **`app.py`** - Gradio web interface
   - `PaperSummarizerApp` class: Wraps core logic with UI
   - Configuration persistence: Saves/loads from `config.json` (gitignored)
   - Real-time processing: Shows progress and results in browser
   - Auto-saves output: Creates timestamped `summaries_YYYYMMDD_HHMMSS.md` files

### Key Design Patterns

- **Configuration precedence**: Web UI > `config.json` > environment variables > CLI arguments
- **Prompt templating**: All prompts must contain `{content}` placeholder for paper text injection
- **API abstraction**: Supports any OpenAI-compatible API via `base_url` parameter (OpenAI, Azure, domestic APIs)
- **Graceful degradation**: Failed papers generate error entries in output rather than stopping the batch

## Configuration

### API Configuration Methods
1. Environment variable: `OPENAI_API_KEY`
2. Config file: `config.json` (auto-created by web UI if "保存配置" is checked)
3. CLI arguments: `--api-key`, `--base-url`, `--model`
4. Web UI inputs (priority over all others)

### Custom Prompts
- Template files can be passed via `--prompt` CLI arg
- Web UI provides editable prompt textarea
- Must include `{content}` placeholder
- Default prompt in `paper_summarizer.py:31-41`

## Important Constraints

- **Text extraction**: Only works with text-based PDFs (not scanned images)
- **Token limit**: Content truncated to 8000 chars in `summarize_text()` at line 81
- **API parameters**: Hard-coded `temperature=0.7` and `max_tokens=2000` in `paper_summarizer.py:90-91`
- **Batch size**: README recommends max 10-20 papers per batch to avoid rate limits

## File Outputs

- Output markdown files follow pattern: `summaries_YYYYMMDD_HHMMSS.md`
- Format: Header with metadata, then numbered sections per paper
- Includes both successful summaries and error messages for failed papers

## Modifying Behavior

When users want to change:
- **Summary style**: Edit prompt template (preserve `{content}` placeholder)
- **API settings**: Modify config.json or web UI inputs
- **Token/temperature**: Edit `paper_summarizer.py:90-91` (requires code change)
- **Content length**: Edit `paper_summarizer.py:81` truncation limit
- **Output format**: Modify `generate_markdown()` in app.py or `save_summaries_to_markdown()` in paper_summarizer.py

## Dependencies

Core: `PyPDF2` (text extraction), `openai>=1.0.0` (API client), `gradio>=4.0.0` (web UI)

Install: `pip install -r requirements.txt`
