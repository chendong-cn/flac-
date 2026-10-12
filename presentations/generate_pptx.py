# generate_pptx.py
# Requires: python-pptx (pip install python-pptx)
# Usage: python generate_pptx.py presentations/AI-customer-service-deck.md presentations/AI-customer-service-deck.pptx

from pptx import Presentation
from pptx.util import Inches, Pt
import sys

MARKDOWN_ENCODING = 'utf-8'

def parse_markdown(md_path):
    with open(md_path, 'r', encoding=MARKDOWN_ENCODING) as f:
        text = f.read()
    sections = [s.strip() for s in text.split('\n\n---\n\n') if s.strip()]
    slides = []
    for sec in sections:
        lines = [l.strip() for l in sec.splitlines() if l.strip()]
        if not lines:
            continue
        title = lines[0].lstrip('#').strip()
        body_lines = []
        for l in lines[1:]:
            # skip design/notes lines that start with "设计建议" or "演讲备注" or "图表建议"
            if l.startswith('设计建议') or l.startswith('演讲备注') or l.startswith('图表建议') or l.startswith('结束语'):
                continue
            body_lines.append(l)
        slides.append((title, body_lines))
    return slides


def add_slide(prs, title, bullets):
    # Title and Content layout index 1 is common, fallback to blank
    layout = prs.slide_layouts[1] if len(prs.slide_layouts) > 1 else prs.slide_layouts[0]
    slide = prs.slides.add_slide(layout)
    try:
        slide.shapes.title.text = title
    except Exception:
        pass
    if bullets:
        body = slide.shapes.placeholders[1]
        tf = body.text_frame
        tf.clear()
        for i, b in enumerate(bullets):
            p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
            p.text = b
            p.level = 0
            p.font.size = Pt(18)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python generate_pptx.py input.md output.pptx')
        sys.exit(1)
    md_in = sys.argv[1]
    pptx_out = sys.argv[2]
    slides = parse_markdown(md_in)
    prs = Presentation()
    # Remove initial blank slide if present
    if len(prs.slides) > 0:
        # keep default first layout for title; we'll replace it
        pass
    for title, body in slides:
        # body: list of lines, collapse continuous lines into bullets by newline
        bullets = []
        # Convert lines that start with '-' or '·' into bullets, otherwise keep as paragraph
        for line in body:
            if line.startswith('- '):
                bullets.append(line[2:])
            else:
                bullets.append(line)
        add_slide(prs, title, bullets)
    prs.save(pptx_out)
    print(f'Generated {pptx_out}')
