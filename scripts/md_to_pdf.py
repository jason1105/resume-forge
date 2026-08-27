#!/usr/bin/env python3
"""
md_to_pdf.py — Render each output/*.md resume variant to output/*.pdf.

Uses WeasyPrint (HTML/CSS → PDF) with a CJK-capable font stack so Chinese
renders correctly. Empty/near-empty markdown is skipped (no blank PDFs).

Reproducible builds: set SOURCE_DATE_EPOCH (WeasyPrint honours it for PDF
metadata dates), so identical content yields identical bytes and avoids
needless binary churn in git.

Deps: weasyprint, markdown  (system: libpango + fonts-noto-cjk)
"""

import glob
import os
import sys

import markdown
from weasyprint import HTML

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(ROOT, "output")

# Content shorter than this is treated as empty/failed generation — no PDF.
MIN_CONTENT_LEN = 40

CSS = """
@page { size: A4; margin: 1.6cm 1.6cm; }
* { box-sizing: border-box; }
body {
  font-family: "Noto Sans CJK SC", "Noto Sans CJK", "PingFang SC",
               "Microsoft YaHei", "DejaVu Sans", sans-serif;
  font-size: 10.5pt; line-height: 1.6; color: #1a1a1a;
}
h1 { font-size: 20pt; font-weight: 700; margin: 0 0 4pt; line-height: 1.2; }
h1 + p { color: #666; margin-top: 0; }
h2 {
  font-size: 12pt; font-weight: 700; text-transform: uppercase;
  letter-spacing: .04em; color: #444;
  margin: 16pt 0 6pt; padding-bottom: 3pt; border-bottom: 1px solid #ddd;
}
h3 { font-size: 11pt; font-weight: 700; margin: 10pt 0 3pt; }
p { margin: 4pt 0; }
ul, ol { margin: 4pt 0; padding-left: 18pt; }
li { margin: 2pt 0; }
strong { color: #000; }
hr { border: none; border-top: 1px solid #ddd; margin: 10pt 0; }
table { width: 100%; border-collapse: collapse; margin: 6pt 0; font-size: 9.5pt; }
th, td { border: 1px solid #ddd; padding: 4pt 6pt; text-align: left; vertical-align: top; }
th { background: #f5f4f2; font-weight: 700; }
code {
  font-family: "DejaVu Sans Mono", monospace; font-size: .88em;
  background: #f2f4f8; padding: 1pt 3pt; border-radius: 3px;
}
pre { background: #f7f8fa; border: 1px solid #e5e7eb; border-radius: 5px; padding: 8pt; overflow-x: auto; }
pre code { background: none; padding: 0; }
blockquote { border-left: 3px solid #b45309; padding-left: 10pt; color: #666; margin: 6pt 0; }
a { color: #1a1a1a; text-decoration: none; }
"""


def md_to_html(md_text: str, title: str) -> str:
    body = markdown.markdown(
        md_text, extensions=["tables", "fenced_code", "sane_lists"]
    )
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<title>{title}</title><style>{CSS}</style></head>"
        f"<body>{body}</body></html>"
    )


def main() -> None:
    md_files = sorted(glob.glob(os.path.join(OUTPUT_DIR, "*.md")))
    if not md_files:
        print("No markdown files found — nothing to convert.")
        return

    made, skipped = 0, []
    for md_path in md_files:
        base = os.path.splitext(os.path.basename(md_path))[0]
        text = open(md_path, encoding="utf-8").read()
        if len(text.strip()) < MIN_CONTENT_LEN:
            print(f"  skip (empty/short): {base}.md")
            skipped.append(base)
            # remove any stale PDF so we never ship a PDF for empty content
            stale = os.path.join(OUTPUT_DIR, base + ".pdf")
            if os.path.exists(stale):
                os.remove(stale)
                print(f"    removed stale: {base}.pdf")
            continue
        html = md_to_html(text, base)
        pdf_path = os.path.join(OUTPUT_DIR, base + ".pdf")
        HTML(string=html, base_url=OUTPUT_DIR).write_pdf(pdf_path)
        print(f"  Written: {pdf_path}")
        made += 1

    print(f"\nDone. {made} PDF(s) generated" + (f", {len(skipped)} skipped." if skipped else "."))


if __name__ == "__main__":
    main()
