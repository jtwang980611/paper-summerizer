import os
import json
from pathlib import Path
from typing import List, Dict
import PyPDF2
from openai import OpenAI


class PaperSummarizer:
    """论文总结器 - 使用OpenAI API总结PDF论文"""

    def __init__(self, api_key: str, base_url: str = None, model: str = "gpt-3.5-turbo"):
        """
        初始化论文总结器

        Args:
            api_key: OpenAI API密钥
            base_url: API基础URL（支持兼容OpenAI格式的API）
            model: 使用的模型名称
        """
        self.api_key = api_key
        self.model = model

        # 初始化OpenAI客户端
        if base_url:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = OpenAI(api_key=api_key)

        # 默认的总结prompt
        self.default_prompt = """请对以下论文内容进行详细总结，包括：
1. 论文标题和作者（如果能识别）
2. 研究背景和动机
3. 主要方法和创新点
4. 实验结果
5. 主要结论和贡献

请用中文总结，格式清晰。

论文内容：
{content}"""

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        从PDF文件中提取文本

        Args:
            pdf_path: PDF文件路径

        Returns:
            提取的文本内容
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""

                # 提取所有页面的文本
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()

                return text
        except Exception as e:
            raise Exception(f"PDF文本提取失败: {str(e)}")

    def summarize_text(self, text: str, custom_prompt: str = None) -> str:
        """
        使用OpenAI API总结文本

        Args:
            text: 要总结的文本
            custom_prompt: 自定义的prompt模板

        Returns:
            总结后的文本
        """
        try:
            # 使用自定义prompt或默认prompt
            prompt_template = custom_prompt if custom_prompt else self.default_prompt
            prompt = prompt_template.format(content=text[:8000])  # 限制长度避免超出token限制

            # 调用OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的学术论文分析助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )

            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"API调用失败: {str(e)}")

    def summarize_paper(self, pdf_path: str, custom_prompt: str = None) -> Dict:
        """
        总结单篇论文

        Args:
            pdf_path: PDF文件路径
            custom_prompt: 自定义prompt

        Returns:
            包含文件名和总结的字典
        """
        file_name = Path(pdf_path).name
        print(f"正在处理: {file_name}")

        # 提取文本
        text = self.extract_text_from_pdf(pdf_path)

        # 生成总结
        summary = self.summarize_text(text, custom_prompt)

        return {
            "file_name": file_name,
            "summary": summary,
            "file_path": pdf_path
        }

    def summarize_papers_in_folder(self, folder_path: str, custom_prompt: str = None) -> List[Dict]:
        """
        总结文件夹中的所有PDF论文

        Args:
            folder_path: 包含PDF文件的文件夹路径
            custom_prompt: 自定义prompt

        Returns:
            所有论文总结的列表
        """
        summaries = []
        pdf_files = list(Path(folder_path).glob("*.pdf"))

        if not pdf_files:
            raise Exception(f"在 {folder_path} 中未找到PDF文件")

        print(f"找到 {len(pdf_files)} 个PDF文件")

        for pdf_file in pdf_files:
            try:
                summary_data = self.summarize_paper(str(pdf_file), custom_prompt)
                summaries.append(summary_data)
            except Exception as e:
                print(f"处理 {pdf_file.name} 时出错: {str(e)}")
                summaries.append({
                    "file_name": pdf_file.name,
                    "summary": f"处理失败: {str(e)}",
                    "file_path": str(pdf_file)
                })

        return summaries

    def save_summaries_to_markdown(self, summaries: List[Dict], output_path: str):
        """
        将所有总结保存到Markdown文件

        Args:
            summaries: 论文总结列表
            output_path: 输出Markdown文件路径
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# 论文总结合集\n\n")
            f.write(f"生成时间: {Path(output_path).stat().st_mtime}\n\n")
            f.write(f"共 {len(summaries)} 篇论文\n\n")
            f.write("---\n\n")

            for i, summary_data in enumerate(summaries, 1):
                f.write(f"## {i}. {summary_data['file_name']}\n\n")
                f.write(f"**文件路径**: `{summary_data['file_path']}`\n\n")
                f.write(f"{summary_data['summary']}\n\n")
                f.write("---\n\n")

        print(f"总结已保存到: {output_path}")


def main():
    """命令行使用示例"""
    import argparse

    parser = argparse.ArgumentParser(description='PDF论文总结工具')
    parser.add_argument('--folder', type=str, required=True, help='包含PDF文件的文件夹路径')
    parser.add_argument('--output', type=str, default='summaries.md', help='输出Markdown文件路径')
    parser.add_argument('--api-key', type=str, help='OpenAI API密钥（或从环境变量读取）')
    parser.add_argument('--base-url', type=str, help='API基础URL（可选）')
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo', help='使用的模型')
    parser.add_argument('--prompt', type=str, help='自定义prompt文件路径')

    args = parser.parse_args()

    # 获取API密钥
    api_key = args.api_key or os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("错误: 请提供API密钥（通过--api-key参数或OPENAI_API_KEY环境变量）")
        return

    # 读取自定义prompt（如果提供）
    custom_prompt = None
    if args.prompt and os.path.exists(args.prompt):
        with open(args.prompt, 'r', encoding='utf-8') as f:
            custom_prompt = f.read()

    # 创建总结器
    summarizer = PaperSummarizer(
        api_key=api_key,
        base_url=args.base_url,
        model=args.model
    )

    # 处理论文
    summaries = summarizer.summarize_papers_in_folder(args.folder, custom_prompt)

    # 保存结果
    summarizer.save_summaries_to_markdown(summaries, args.output)
    print("完成!")


if __name__ == "__main__":
    main()
