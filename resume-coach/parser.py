"""文件解析工具：PDF / DOCX / TXT → 纯文本

用法（被 skill 调用）:
  uv run python .claude/skills/resume-iq/parser.py resume.pdf
  uv run python .claude/skills/resume-iq/parser.py resume.docx
  uv run python .claude/skills/resume-iq/parser.py jd.txt
"""

import sys
from pathlib import Path


def parse_pdf(file_path: str) -> str:
    import fitz
    doc = fitz.open(file_path)
    texts = [page.get_text() for page in doc]
    doc.close()
    return "\n".join(texts)


def parse_docx(file_path: str) -> str:
    from docx import Document
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def parse_file(file_path: str) -> str:
    p = Path(file_path)
    suffix = p.suffix.lower()
    if suffix == ".pdf":
        return parse_pdf(file_path)
    elif suffix in (".docx", ".doc"):
        return parse_docx(file_path)
    elif suffix in (".txt", ".md"):
        return p.read_text(encoding="utf-8")
    else:
        raise ValueError(f"不支持的格式: {suffix}（支持 .pdf/.docx/.txt/.md）")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python parser.py <文件路径>", file=sys.stderr)
        sys.exit(1)
    try:
        print(parse_file(sys.argv[1]))
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
