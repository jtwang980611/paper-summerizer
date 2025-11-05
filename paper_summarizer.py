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

        # 默认的总结prompt（针对实证研究论文）
        self.default_prompt = """请按照实证研究论文的结构，对以下论文进行详细总结：

## 1. 论文基本信息
- 标题，作者和年份（如果能识别）
- 研究问题/研究假设

## 2. 研究背景与理论基础
- 研究背景和动机
- 文献回顾与理论框架
- 研究贡献和创新点

## 3. 研究方法
- 样本来源和数据说明
- 变量定义（因变量、自变量、控制变量）
- 研究设计和模型设定

## 4. 实证结果
- 描述性统计
- 基准回归结果
- 稳健性检验（如果有）
- 机制分析或异质性分析（如果有）

## 5. 结论与启示
- 主要研究发现
- 理论贡献和实践意义
- 政策建议
- 研究局限性和未来研究方向

请用中文总结，条理清晰，重点突出实证研究的核心要素。

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

                # 验证提取的文本
                if not text or len(text.strip()) < 100:
                    raise Exception(f"PDF文本提取失败或内容太少（提取到 {len(text)} 字符）")

                print(f"成功提取 {len(text)} 字符，共 {len(pdf_reader.pages)} 页")
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
            prompt = prompt_template.format(content=text[:16000])  # 增加输入长度限制

            print(f"准备调用API，模型: {self.model}，输入长度: {len(prompt)} 字符")

            # 调用OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的学术论文分析助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000  # 增加输出token限制
            )

            # 验证响应
            if not response.choices or len(response.choices) == 0:
                raise Exception("API返回为空，没有生成任何内容")

            summary = response.choices[0].message.content

            if not summary or len(summary.strip()) < 50:
                raise Exception(f"API返回内容太少或为空（长度: {len(summary) if summary else 0}）")

            print(f"API调用成功，生成总结长度: {len(summary)} 字符")
            return summary

        except Exception as e:
            print(f"❌ API调用错误详情: {str(e)}")
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
