#!/usr/bin/env python3
"""
build_resumes.py — Reads data/resume.yml and uses the Anthropic Claude API
to generate four resume variants, writing them to the output/ directory.

Usage:
    python scripts/build_resumes.py

Environment variable required:
    OPENROUTER_API_KEY
"""

import os
import sys
import yaml
from openai import OpenAI

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(ROOT_DIR, "data", "resume.yml")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")


# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------

PROMPT_ZH_FULL = """
你是一位专业的简历撰写专家。请根据以下 YAML 格式的个人信息，生成一份详尽的中文简历（Markdown 格式），
内容相当于约两页纸。要求：
- 使用专业、正式的中文表达
- 按照：个人信息 → 个人简介 → 工作经历 → 技能 → 教育背景 → 语言能力 的顺序排列
- 工作经历部分只能对 YAML 中已有的内容做措辞润色和结构重组，不得新增事实
- 技能部分用分类表格或分类列表呈现
- 整体风格简洁、专业，适合投递至中国一线互联网/科技企业

简历数据（YAML）：
{yaml_data}

请直接输出 Markdown 内容，不要有任何前缀说明。
"""

PROMPT_EN_FULL = """
You are a professional resume writer. Based on the YAML data below, generate a comprehensive English resume
in Markdown format, equivalent to about two pages. Requirements:
- Use polished, professional English suitable for senior engineering roles
- Order: Personal Info → Professional Summary → Work Experience → Skills → Education → Languages
- For each experience highlight, only rephrase and restructure what the YAML already states.
  Do not add facts
- Present skills in categorized lists or tables
- Style: clean, ATS-friendly, appropriate for top-tier tech companies globally

Resume data (YAML):
{yaml_data}

Output only the Markdown content, no preamble or commentary.
"""

PROMPT_ZH_ONEPAGE = """
你是一位专业的简历撰写专家。请根据以下 YAML 格式的个人信息，生成一份精简的中文简历（Markdown 格式），
控制在一页纸篇幅内（约 400-500 字）。要求：
- 突出最核心的技能与成就
- 工作经历每条只保留最关键的 1-2 个亮点
- 技能简洁列举，不需要过多展开
- 整体结构清晰，信息密度高，一眼可抓住重点

简历数据（YAML）：
{yaml_data}

请直接输出 Markdown 内容，不要有任何前缀说明。
"""

PROMPT_EN_ONEPAGE = """
You are a professional resume writer. Based on the YAML data below, generate a concise one-page English
resume in Markdown format (approximately 350-450 words). Requirements:
- Lead with the strongest skills and top achievements
- Each role: 1-2 bullet points max, focused on impact and scale
- Skills: brief inline list, no tables
- Crisp, high-signal content recruiters can scan in 30 seconds

Resume data (YAML):
{yaml_data}

Output only the Markdown content, no preamble or commentary.
"""

FACT_GUARD = """

=== 事实约束（最高优先级，覆盖以上任何要求）===
这是一份真实求职者的简历，任何编造都可能在面试或背调中造成严重后果。
1. 只能使用上面 YAML 中明确写出的事实。严禁新增、推断或"合理补充"任何内容。
2. 严禁编造任何数字：百分比、耗时、QPS、并发量、覆盖率、延迟、吞吐、人数、时长。
   YAML 里没有的数字，一个都不许出现。
3. 严禁编造 YAML 未提及的技术名词、中间件、框架、项目或职责。
4. 如果某段经历信息很少，就让它保持简短——宁可简历短，也不许填充虚构内容。
5. 你可以做的只有：翻译、措辞润色、结构重组、条目排序。
"""

VARIANTS = [
    {
        "key": "resume_zh",
        "filename": "resume_zh.md",
        "prompt_template": PROMPT_ZH_FULL,
        "label": "Full Chinese Resume",
    },
    {
        "key": "resume_en",
        "filename": "resume_en.md",
        "prompt_template": PROMPT_EN_FULL,
        "label": "Full English Resume",
    },
    {
        "key": "resume_onepage_zh",
        "filename": "resume_onepage_zh.md",
        "prompt_template": PROMPT_ZH_ONEPAGE,
        "label": "One-Page Chinese Resume",
    },
    {
        "key": "resume_onepage_en",
        "filename": "resume_onepage_en.md",
        "prompt_template": PROMPT_EN_ONEPAGE,
        "label": "One-Page English Resume",
    },
]

MODEL = os.environ.get("LLM_MODEL") or os.environ.get("OPENROUTER_MODEL") or "deepseek-v4-flash"
OPENROUTER_BASE = os.environ.get("LLM_BASE_URL") or "https://api.deepseek.com"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def load_resume_data(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def yaml_dump(data: dict) -> str:
    return yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)


def generate_variant(client: OpenAI, yaml_text: str, variant: dict) -> str:
    prompt = variant["prompt_template"].format(yaml_data=yaml_text) + FACT_GUARD
    print(f"  Generating: {variant['label']} ...")
    message = client.chat.completions.create(
        model=MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.choices[0].message.content


def write_output(filename: str, content: str) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Written: {path}")


def main():
    api_key = os.environ.get("LLM_API_KEY") or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: LLM_API_KEY (or OPENROUTER_API_KEY) environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(DATA_FILE):
        print(f"ERROR: Data file not found: {DATA_FILE}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading resume data from {DATA_FILE}")
    resume_data = load_resume_data(DATA_FILE)
    yaml_text = yaml_dump(resume_data)

    client = OpenAI(base_url=OPENROUTER_BASE, api_key=api_key)

    print(f"\nGenerating resume variants using model: {MODEL}")
    for variant in VARIANTS:
        try:
            content = generate_variant(client, yaml_text, variant)
            write_output(variant["filename"], content)
        except Exception as e:
            print(f"  ERROR generating {variant['label']}: {e}", file=sys.stderr)
            sys.exit(1)

    print("\nAll resume variants generated successfully.")


if __name__ == "__main__":
    main()
