# -*- coding: utf-8 -*-
"""把排版 HTML 里的「配图占位块」替换成已生成的真实图片。

占位格式（当前 md2gzh 输出）：
    <!-- 配图占位：配图01｜封面｜智能体跑出围栏｜待替换 -->
    <section ...dashed...> 🖼 配图占位 · ... </section>

按「配图序号 01/02/03」去 images/第NN期/ 里找 NN_01_* / NN_02_* / NN_03_*。
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 占位注释
PLACE = re.compile(r"<!--\s*配图占位：配图(\d+)｜([^>]*?)-->")
# 占位展示区（虚线框那段）
BOX = re.compile(
    r"\s*<section[^>]*border:1px dashed[^>]*>.*?</section>",
    re.S,
)


def find_section(html, start):
    """从 start 起找到 <section ...> ... </section> 的完整区间（含嵌套）"""
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


def pick_image(img_dir, num):
    pat = os.path.join(img_dir, "*_%s_*.*" % num)
    hit = [p for p in glob.glob(pat)
           if os.path.splitext(p)[1].lower() in (".jpg", ".jpeg", ".png")]
    return sorted(hit)[0] if hit else None


def img_block(rel, desc):
    return (
        '  <section style="margin:24px 0;padding:0 10px;">\n'
        '    <section style="border-radius:12px;overflow:hidden;background:#FFFFFF;'
        'border:1px solid #E5E7EB;">\n'
        '      <img src="%s" alt="%s" '
        'style="max-width:100%%;height:auto;display:block;margin:0 auto;">\n'
        '    </section>\n'
        '    <p style="text-align:center;font-size:12px;color:#9CA3AF;'
        'margin:10px 0 0;line-height:1.7;"><span leaf="">%s</span></p>\n'
        '  </section>' % (rel, desc, desc)
    )


def process(html_path, img_dir):
    with open(html_path, encoding="utf-8") as f:
        html = f.read()

    blocks = [(m.group(1), m.group(2), m.start(), m.end())
              for m in PLACE.finditer(html)]
    if not blocks:
        return 0, 0

    replaced = 0
    for num, desc_raw, s, e in reversed(blocks):
        # 图注：取倒数第二段有效描述（末尾「待替换」「建议 …」都不算）
        parts = [p.strip() for p in desc_raw.split("｜") if p.strip()]
        parts = [p for p in parts if p != "待替换"]
        desc = parts[-1] if parts else "配图%s" % num
        desc = re.sub(r"\s*建议.*$", "", desc).strip() or ("配图%s" % num)

        path = pick_image(img_dir, num.zfill(2))
        if not path:
            print("  ⚠️  配图%s 未找到图片（%s）" % (num, desc))
            continue
        rel = os.path.relpath(path, ROOT).replace("\\", "/")

        # 占位注释 + 紧随的虚线展示区 → 换成真图
        tail = e
        m_box = BOX.match(html, tail)
        if m_box:
            tail = m_box.end()

        html = html[:s] + img_block(rel, desc) + html[tail:]
        replaced += 1
        print("  ✅ 配图%s → %s（%s）" % (num, os.path.basename(path), desc))

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    return replaced, len(blocks)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--issues", default="73-77", help="期号范围，如 66-71")
    ap.add_argument("--only", type=int, default=0, help="只处理某一期")
    args = ap.parse_args()
    if args.only:
        lo = hi = args.only
    else:
        lo, hi = [int(x) for x in args.issues.split("-")]

    total = 0
    for n in range(lo, hi + 1):
        img_dir = os.path.join(ROOT, "images", "第%d期" % n)
        if not os.path.isdir(img_dir):
            print("跳过 %d（无图片目录）" % n)
            continue
        for html in glob.glob(os.path.join(
                ROOT, "第%d期_*_排版_*.html" % n)):
            print("%s" % os.path.basename(html))
            rep, allb = process(html, img_dir)
            total += rep
            print("  → %d/%d" % (rep, allb))
    print("共替换 %d 处" % total)


if __name__ == "__main__":
    main()
