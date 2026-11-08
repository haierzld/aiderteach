# -*- coding: utf-8 -*-
"""把排版 HTML 里的「配图占位块」替换成真实图片组件。

用法：
    python replace_placeholders.py --html 第60期_xxx_排版_小智科技(xiaozhi-tech).html --dir images/pub/还要背课文

匹配规则：占位块标题（如「🖼 配图 02 · 第01章 两个实验」）去掉「第XX章 / 结尾」等位置前缀后，
得到的关键词在图片目录里找同名文件（支持 .jpg/.jpeg/.png）。图注自动取占位块里的「画面：…」描述。
"""
import argparse
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLACEHOLDER = re.compile(r"<!--\s*配图占位\s*(\d+)[^>]*-->")


def find_block(html, start):
    """从占位注释起点找到它那个 section 块的完整区间（含嵌套）"""
    i = html.index("<section", start)
    depth, j = 0, i
    while True:
        op = re.compile(r"<section\b").search(html, j)
        cl = re.compile(r"</section>").search(html, j)
        if cl is None:
            return i, len(html)
        if op and op.start() < cl.start():
            depth += 1
            j = op.end()
        else:
            depth -= 1
            j = cl.end()
            if depth == 0:
                return i, j


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", default=None, help="默认原地覆盖")
    args = ap.parse_args()

    html_path = args.html if os.path.isabs(args.html) else os.path.join(ROOT, args.html)
    img_dir = args.dir if os.path.isabs(args.dir) else os.path.join(ROOT, args.dir)
    files = os.listdir(img_dir)

    with open(html_path, encoding="utf-8") as f:
        html = f.read()

    # 占位块：倒序替换，避免位置偏移
    blocks = [(m.group(1), m.start(), m.end()) for m in PLACEHOLDER.finditer(html)]
    replaced = 0
    for num, s, e in reversed(blocks):
        b_start, b_end = find_block(html, e)
        block = html[b_start:b_end]

        title_m = re.search(r"🖼\s*配图\s*\d+\s*·\s*([^<]+)", block)
        raw = title_m.group(1).strip() if title_m else ""
        keyword = re.sub(r"^第\d+章\s*", "", raw)
        keyword = re.sub(r"^(封面|结尾|正文)\s*", "", keyword).strip()
        if not keyword:
            keyword = raw

        hit = [f for f in files if keyword and keyword in os.path.splitext(f)[0]]
        if not hit:
            print(f"⚠️  配图 {num}（{raw}）未找到图片，跳过")
            continue
        fname = hit[0]

        desc_m = re.search(r"画面：(.+?)\s*·\s*风格", block)
        desc = desc_m.group(1).strip() if desc_m else keyword

        rel = os.path.join(args.dir, fname).replace("\\", "/")
        new_block = (
            f'  <!-- 配图 {num} · {raw} -->\n'
            f'  <section style="margin:24px 0;border-radius:12px;overflow:hidden;'
            f'background:#F8FAFF;border:1px solid #E5E7EB;">\n'
            f'    <img src="{rel}" alt="{desc}" '
            f'style="max-width:100%;height:auto;display:block;margin:0 auto;">\n'
            f'    <p style="text-align:center;font-size:12px;color:#6B7280;margin:8px 0 0;'
            f'padding:0 12px 12px;"><span leaf="">{desc}</span></p>\n'
            f'  </section>'
        )
        html = html[:s] + new_block + html[b_end:]
        replaced += 1
        print(f"✅ 配图 {num}（{raw}）→ {fname}")

    out = args.out or html_path
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"💾 已保存: {out}　共替换 {replaced}/{len(blocks)} 处")


if __name__ == "__main__":
    main()
