"""Render the handout to the Pages publishing folder."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent
CHAPTERS = [
    ("overview", "00 复习总览.md"),
    ("chapter-1", "01 第一章 离散时间信号与系统.md"),
    ("chapter-2", "02 第二章 采样与重建.md"),
    ("chapter-3", "03 第三章 DFT与FFT.md"),
    ("chapter-4", "05 第四章 IIR滤波器设计.md"),
    ("chapter-5", "06 第五章 FIR滤波器设计.md"),
    ("chapter-6", "07 第六章 数字滤波器结构.md"),
    ("reference", "04 题型与公式速查.md"),
]


def build():
    sections = []
    for slug, filename in CHAPTERS:
        source = (ROOT / "handout" / filename).read_text(encoding="utf-8")
        heading, body = source.split("\n", 1)
        for target, linked_filename in CHAPTERS:
            body = body.replace(f"]({linked_filename.replace(' ', '%20')})", f"](#{target})")
        sections.append(f"{heading} {{#{slug}}}\n{body}")
    result = subprocess.run(
        ["pandoc", "--from=markdown+tex_math_dollars", "--to=html5", "--section-divs",
         "--mathml", "--toc", "--toc-depth=2", "--template=site/page.html"],
        cwd=ROOT, input="\n\n".join(sections), encoding="utf-8",
        capture_output=True, check=True,
    )
    if result.stderr.strip():
        raise RuntimeError(result.stderr)
    # Pandoc/texmath may encode unary minus as an identifier. Keep it an operator.
    mathml = result.stdout.replace('<mi>−</mi>', '<mo form="prefix">−</mo>')
    html = re.sub(r'(<math display="block".*?</math>)', r'<span class="formula">\1</span>',
                  mathml, flags=re.DOTALL)
    (ROOT / "docs" / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    build()
