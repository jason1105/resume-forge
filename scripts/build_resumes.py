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

PROMPT_ZH_TARGETED = """
你是一位专业的简历撰写专家。下面给出一段招聘 JD 和一份 YAML 个人信息。
请生成一份**针对该 JD 定向优化**的中文简历（Markdown 格式），要求：
- 从 YAML 已有事实中，挑选并前置与该 JD 最相关的经历、技能与关键词
- 措辞贴合 JD 的用语与关注点，但严禁改变或夸大事实
- 与该岗位关系不大的次要内容可以弱化或省略
- 结构：个人信息 → 针对性简介（点明与该岗位的匹配点）→ 相关工作经历 → 技能 → 教育背景 → 语言能力
- 整体简洁、专业，适合投递中国一线互联网/科技企业

招聘 JD：
{jd}

简历数据（YAML）：
{yaml_data}

请直接输出 Markdown 内容，不要有任何前缀说明。
"""

PROMPT_EN_TARGETED = """
You are a professional resume writer. Below is a job description (JD) and a candidate's YAML profile.
Generate a resume in Markdown, **tailored to this JD**. Requirements:
- From the facts already in the YAML, surface and lead with the experience, skills and keywords most relevant to this JD
- Mirror the JD's terminology and priorities, but never alter or overstate the facts
- De-emphasize or omit content not relevant to the role
- Order: Personal Info → Targeted Summary (state the fit for this role) → Relevant Experience → Skills → Education → Languages
- Clean, ATS-friendly, suitable for top-tier tech companies

Job description (JD):
{jd}

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

# Targeted variants — only generated when a JD is supplied via JD_TEXT
TARGETED_VARIANTS = [
    {
        "key": "resume_targeted_zh",
        "filename": "resume_targeted_zh.md",
        "prompt_template": PROMPT_ZH_TARGETED,
        "label": "JD-Targeted Chinese Resume",
    },
    {
        "key": "resume_targeted_en",
        "filename": "resume_targeted_en.md",
        "prompt_template": PROMPT_EN_TARGETED,
        "label": "JD-Targeted English Resume",
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


# 认为“有效产出”的最小字符数——低于此视为空/截断响应
MIN_CONTENT_LEN = 80


def _chat_with_retry(client: OpenAI, prompt: str, label: str, attempts: int = 3) -> str:
    """调用模型，对空/过短响应重试。返回去除首尾空白后的文本（可能仍为空，由调用方决定如何处理）。"""
    last = ""
    for i in range(attempts):
        message = client.chat.completions.create(
            model=MODEL,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        content = (message.choices[0].message.content or "").strip()
        if len(content) >= MIN_CONTENT_LEN:
            return content
        last = content
        print(f"    (尝试 {i + 1}/{attempts}) {label} 返回空/过短响应（{len(content)} 字），重试…")
    return last


def generate_variant(client: OpenAI, yaml_text: str, variant: dict) -> str:
    prompt = variant["prompt_template"].format(yaml_data=yaml_text) + FACT_GUARD
    print(f"  Generating: {variant['label']} ...")
    return _chat_with_retry(client, prompt, variant["label"])


def generate_targeted_variant(client: OpenAI, yaml_text: str, jd: str, variant: dict) -> str:
    prompt = variant["prompt_template"].format(yaml_data=yaml_text, jd=jd) + FACT_GUARD
    print(f"  Generating: {variant['label']} ...")
    return _chat_with_retry(client, prompt, variant["label"])


def write_output(filename: str, content: str) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Written: {path}")


def write_if_valid(filename: str, content: str, label: str, skipped: list) -> None:
    """仅在响应有效时写入；空/过短响应则跳过并保留已有文件，绝不用空内容覆盖好内容。"""
    if not content or len(content.strip()) < MIN_CONTENT_LEN:
        print(f"  跳过 {label}：响应为空/过短，保留已有文件（不覆盖）", file=sys.stderr)
        skipped.append(label)
        return
    write_output(filename, content)


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

    skipped: list = []

    print(f"\nGenerating resume variants using model: {MODEL}")
    for variant in VARIANTS:
        try:
            content = generate_variant(client, yaml_text, variant)
            write_if_valid(variant["filename"], content, variant["label"], skipped)
        except Exception as e:
            print(f"  ERROR generating {variant['label']}: {e}", file=sys.stderr)
            sys.exit(1)

    # JD-targeted variants — only when a job description is provided
    jd_text = (os.environ.get("JD_TEXT") or "").strip()
    if jd_text:
        jd_title = (os.environ.get("JD_TITLE") or "").strip()
        jd_full = (f"目标岗位：{jd_title}\n\n" if jd_title else "") + jd_text
        print(f"\nJD provided ({len(jd_text)} chars) — generating targeted variants")
        for variant in TARGETED_VARIANTS:
            try:
                content = generate_targeted_variant(client, yaml_text, jd_full, variant)
                write_if_valid(variant["filename"], content, variant["label"], skipped)
            except Exception as e:
                print(f"  ERROR generating {variant['label']}: {e}", file=sys.stderr)
                sys.exit(1)
    else:
        print("\nNo JD_TEXT provided — skipping targeted variants.")

    if skipped:
        print(f"\n⚠️  {len(skipped)} 个版本因空/过短响应被跳过（已保留旧内容，未覆盖）："
              f"{', '.join(skipped)}", file=sys.stderr)
        print("   常见原因：LLM 供应商额度不足/限流，或该提示词被拒。请检查 DeepSeek 余额与限流。",
              file=sys.stderr)

    print("\nAll resume variants processed.")


if __name__ == "__main__":
    main()
