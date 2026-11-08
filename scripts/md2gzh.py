# -*- coding: utf-8 -*-
"""
md2gzh.py —— 把公众号 MD 文稿转成排版 HTML（爱德数智 / 小智），支持多套主题配色

用法：
  python md2gzh.py 第63期_xxx.md [--ask "互动问句"] [--ask-sub "副文案"] [--theme 主题] [--no-preview]

主题（--theme，默认 red-white）：
  red-white     红白色系
  blue-white    蓝白专业
  green-white   绿白清新
  orange-white  橙暖温情
  purple-white  紫白创想

MD 约定：
  # 标题             → 不进正文（发布时用 --title）
  > 金句（首段）      → 引言卡（主题色渐变底+白字；==高亮== 变白底主题深字）
  > 金句（其它）      → 左竖条金句卡
  ## 章节 <!-- EN --> → 编号章节；标题以"最后"开头 → ∞ THE END
  ### 子标题          → 左侧竖线小标题
  ==文本==           → 主题下划线强调
  **文本**           → 加粗
  `代码`             → 行内代码
  - 项 / 1. 项       → 无序 / 有序列表
  | a | b |          → 对照行（主题浅色底）
  ![说明](路径)       → 图片；路径为 PLACEHOLDER 时生成占位块
  ---                → 渐变分割线
"""
import os
import re
import subprocess
import sys
from html import escape

# ---- 主题配色 ----
# main 主色 / deep 深色(表头字·渐变深端) / light 浅底 / line 边框
# under 下划线强调 / rgb 主色RGB三元组(金句卡阴影用)
THEMES = {
    "red-white": dict(label="红白色系", main="#DC2626", deep="#991B1B",
                      light="#FEF2F2", line="#FEE2E2", under="#FECACA",
                      rgb="220,38,38"),
    "blue-white": dict(label="蓝白专业", main="#2563EB", deep="#1E40AF",
                       light="#EFF6FF", line="#DBEAFE", under="#BFDBFE",
                       rgb="37,99,235"),
    "green-white": dict(label="绿白清新", main="#16A34A", deep="#15803D",
                        light="#F0FDF4", line="#DCFCE7", under="#BBF7D0",
                        rgb="22,163,74"),
    "orange-white": dict(label="橙暖温情", main="#EA580C", deep="#C2410C",
                         light="#FFF7ED", line="#FFEDD5", under="#FED7AA",
                         rgb="234,88,12"),
    "purple-white": dict(label="紫白创想", main="#7C3AED", deep="#6D28D9",
                         light="#F5F3FF", line="#EDE9FE", under="#DDD6FE",
                         rgb="124,58,237"),
}

C_MAIN = THEMES["red-white"]["main"]
C_DEEP = THEMES["red-white"]["deep"]
C_LIGHT = THEMES["red-white"]["light"]
C_LINE = THEMES["red-white"]["line"]
C_TABLE_HEAD = THEMES["red-white"]["deep"]  # 表头文字用深色：背景被公众号过滤时依然清晰
C_UNDER = THEMES["red-white"]["under"]
C_RGB = THEMES["red-white"]["rgb"]


def apply_theme(key):
    """切换主题配色（全局生效），返回主题中文名。"""
    global C_MAIN, C_DEEP, C_LIGHT, C_LINE, C_TABLE_HEAD, C_UNDER, C_RGB
    t = THEMES.get(key) or THEMES["red-white"]
    C_MAIN, C_DEEP = t["main"], t["deep"]
    C_LIGHT, C_LINE, C_UNDER = t["light"], t["line"], t["under"]
    C_TABLE_HEAD, C_RGB = t["deep"], t["rgb"]
    return t["label"]
QR_IMG = "images/pub/qrcode.jpg"
SKILL = r"C:\Users\81380\.codebuddy\skills\gzh-design\scripts"
PICK_QUOTE = os.path.join(SKILL, "pick_quote.py")
WRAP_PREVIEW = os.path.join(SKILL, "wrap_preview.py")

TOKEN = re.compile(r"==(.+?)==|\*\*(.+?)\*\*|`(.+?)`")


def fix_quotes(t):
    """半角直引号 → 中文弯引号（成对交替）。"""
    out, flag = [], True
    for ch in t:
        if ch == '"':
            out.append("\u201c" if flag else "\u201d")
            flag = not flag
        else:
            out.append(ch)
    return "".join(out)


def leaf(s):
    s = escape(s)
    return '<span leaf="">%s</span>' % s if s else ""


URL_RE = re.compile(r"https?://[^\s，。）)】\"']+")


def leaf_url(s):
    """普通文本片段：网址自动变蓝色下划线。"""
    if not s:
        return ""
    out, pos = [], 0
    for m in URL_RE.finditer(s):
        out.append(leaf(s[pos:m.start()]))
        out.append('<span style="color:#2563EB;text-decoration:underline;'
                   'word-break:break-all;">%s</span>' % leaf(m.group(0)))
        pos = m.end()
    out.append(leaf(s[pos:]))
    return "".join(out)


def inline(text, highlight=False, inverse=False):
    out, pos = [], 0
    for m in TOKEN.finditer(text):
        out.append(leaf_url(text[pos:m.start()]))
        if m.group(1) is not None:
            if highlight and inverse:
                out.append('<span style="background:#FDE047;color:#7F1D1D;padding:2px 8px;'
                           'border-radius:4px;">%s</span>' % (leaf(m.group(1))))
            elif highlight:
                out.append('<span style="background:%s;color:#FFFFFF;padding:2px 8px;'
                           'border-radius:4px;">%s</span>' % (C_MAIN, leaf(m.group(1))))
            else:
                out.append('<span style="border-bottom:2px solid %s;font-weight:600;">%s</span>'
                           % (C_UNDER, leaf(m.group(1))))
        elif m.group(2) is not None:
            out.append("<strong>%s</strong>" % leaf(m.group(2)))
        else:
            out.append('<span style="background:#F3F4F6;color:#1F2937;padding:2px 6px;'
                       'border-radius:4px;font-size:14px;font-weight:600;">%s</span>'
                       % leaf(m.group(3)))
        pos = m.end()
    out.append(leaf_url(text[pos:]))
    return "".join(out)


P_STYLE = "margin-bottom:20px;font-size:15px;line-height:1.8;text-align:left;"


def para(text, style=P_STYLE):
    return '<p style="%s">%s</p>' % (style, inline(text))


def intro_card(text):
    return (
        '<section style="margin:10px 10px 32px;padding:30px 26px 26px;'
        "background:linear-gradient(135deg,%s 0%%,%s 100%%);border-radius:16px;text-align:center;"
        'color:#fff;box-shadow:0 8px 28px -6px rgba(%s,0.38);">\n'
        '    <p style="font-size:30px;color:rgba(255,255,255,0.5);font-weight:900;'
        'margin:0 0 4px;line-height:1;text-align:left;">%s</p>\n'
        '    <p style="font-size:17px;font-weight:800;color:#FFFFFF;margin:0 0 14px;'
        'line-height:1.8;text-align:center;">%s</p>\n'
        '    <p style="font-size:12px;color:rgba(255,255,255,0.78);margin:0;'
        'letter-spacing:1px;text-align:right;">%s</p>\n'
        "  </section>" % (C_MAIN, C_DEEP, C_RGB, leaf("\u201c"), inline(text, highlight=True, inverse=True), leaf("—— 小智")))


def quote_card(text):
    return (
        '<section style="background:%s;border-radius:0 10px 10px 0;border-left:4px solid %s;'
        "padding:18px 22px;margin-bottom:24px;\">\n"
        '      <p style="font-size:16px;font-weight:800;color:%s;margin:0;line-height:1.8;">%s</p>\n'
        "    </section>" % (C_LIGHT, C_MAIN, C_DEEP, inline(text)))


def section_head(num, title, en):
    if (en or "").upper() in ("END", "FINAL"):
        badge, en_show = "\u221e", "THE END"
    else:
        badge, en_show = "%02d" % num, (en or "PART").upper()
    return (
        '<section style="display:flex;align-items:center;justify-content:space-between;'
        "margin-bottom:20px;padding-bottom:14px;border-bottom:3px solid %s;\">\n"
        '      <section style="display:flex;align-items:center;">\n'
        '        <span style="display:inline-block;background:%s;color:#FFFFFF;font-size:18px;'
        "font-weight:900;padding:4px 14px;border-radius:6px;margin-right:14px;line-height:1.3;\">%s</span>\n"
        "        <section>\n"
        '          <p style="font-size:10px;color:%s;font-weight:700;letter-spacing:3px;'
        "margin:0 0 2px;text-transform:uppercase;\">%s</p>\n"
        '          <h3 style="font-size:18px;font-weight:800;color:#1C1917;margin:0;'
        "letter-spacing:0.5px;\">%s</h3>\n"
        "        </section>\n"
        "      </section>\n"
        "    </section>" % (C_MAIN, C_MAIN, leaf(badge), C_MAIN, leaf(en_show), inline(title)))


def sub_head(text):
    return (
        '<p style="font-size:15px;font-weight:800;color:#1C1917;margin:28px 0 14px;'
        "padding-left:10px;border-left:3px solid %s;line-height:1.4;\">%s</p>"
        % (C_MAIN, inline(text)))


def divider():
    return (
        '<section style="padding:0 10px;">\n'
        '    <section style="height:1px;background:linear-gradient(to right,transparent,%s,%s,%s,transparent);'
        'margin:0;"><span leaf=""><br></span></section>\n'
        "  </section>" % (C_UNDER, C_MAIN, C_UNDER))


def image_block(src, alt):
    if src == "PLACEHOLDER":
        return (
            "    <!-- 配图占位：%s｜待替换 -->\n"
            '    <section style="margin:0 0 24px;padding:14px 18px;border:1px dashed #E5E7EB;'
            "border-radius:10px;background:%s;text-align:center;\">\n"
            '      <p style="margin:0;font-size:12px;color:#9CA3AF;line-height:1.7;">%s</p>\n'
            "    </section>"
            % (alt, C_LIGHT, leaf(alt)))
    return (
        '    <section style="background:#FFF;border-radius:12px;padding:6px;border:1px solid #E5E7EB;'
        "box-shadow:0 4px 12px -2px rgba(0,0,0,0.08);margin-bottom:8px;\">\n"
        '      <section style="margin:0;border-radius:8px;overflow:hidden;">\n'
        '        <span leaf=""><img src="%s" style="max-width:100%%;height:auto;display:block;'
        'margin:0 auto;"></span>\n'
        "      </section>\n"
        "    </section>\n"
        '    <p style="font-size:12px;color:#9CA3AF;text-align:center;margin:0 0 24px;">%s</p>'
        % (src, leaf("— " + alt)))


def ul_item(text):
    return (
        '<section style="display:flex;align-items:flex-start;gap:10px;margin-bottom:12px;">\n'
        '        <span style="display:inline-flex;align-items:center;justify-content:center;'
        "width:6px;height:6px;background:%s;border-radius:50%%;flex-shrink:0;margin-top:10px;\">"
        '<span leaf="">&nbsp;</span></span>\n'
        '        <p style="font-size:15px;color:#374151;margin:0;line-height:1.8;flex:1;">%s</p>\n'
        "      </section>" % (C_MAIN, inline(text)))


def ol_item(idx, text):
    return (
        '<section style="display:flex;align-items:flex-start;gap:10px;margin-bottom:12px;">\n'
        '        <span style="display:inline-flex;align-items:center;justify-content:center;'
        "width:22px;height:22px;background:%s;color:#fff;font-size:12px;font-weight:700;"
        "border-radius:50%%;flex-shrink:0;margin-top:2px;\">%s</span>\n"
        '        <p style="font-size:15px;color:#374151;margin:0;line-height:1.8;flex:1;">%s</p>\n'
        "      </section>" % (C_MAIN, leaf(str(idx)), inline(text)))


def table_block(rows):
    """Markdown 表格 → 真正的 HTML 表格（首行为表头）。

    公众号编辑器对 table 支持有限，所以：
    - 用 border-collapse:collapse（不用 separate，圆角/overflow 常被过滤）
    - 所有样式写在 td/th 上，避免依赖 table 标签自身的样式
    """
    if not rows:
        return ""
    ncol = max(len(r) for r in rows)

    def pad(cells):
        return cells + [""] * (ncol - len(cells))

    # 表头：浅红底 + 深红字 + 红色粗下边框。
    # 不依赖背景色来显示文字——公众号常过滤 background，
    # 背景一旦丢失，深色字在白底上仍然可读。
    th = "".join(
        '<th style="padding:9px 10px;text-align:left;font-weight:700;'
        'color:%s;background:%s;border:1px solid %s;border-bottom:3px solid %s;">%s</th>'
        % (C_TABLE_HEAD, C_LINE, C_LINE, C_MAIN, inline(c))
        for c in pad(rows[0]))
    head = '<tr>%s</tr>' % th

    body = []
    for r in rows[1:]:
        tds = "".join(
            '<td style="padding:9px 10px;color:#374151;vertical-align:top;'
            'border:1px solid %s;">%s</td>' % (C_LINE, inline(c))
            for c in pad(r))
        body.append('<tr style="background:%s;">%s</tr>' % (C_LIGHT, tds))

    return (
        '<table style="width:100%%;border-collapse:collapse;margin-bottom:20px;'
        'font-size:14px;line-height:1.6;border:1px solid %s;">\n'
        "      <thead>%s</thead>\n"
        "      <tbody>\n      %s\n      </tbody>\n"
        "    </table>" % (C_LINE, head, "\n      ".join(body)))


def kv_row(cells):
    left = cells[0] if cells else ""
    right = " · ".join(cells[1:])
    return (
        '<section style="display:flex;align-items:center;justify-content:space-between;'
        "background:%s;border-radius:8px;padding:10px 14px;margin-bottom:8px;border:1px solid %s;\">\n"
        '        <p style="font-size:14px;color:#374151;margin:0;">%s</p>\n'
        '        <p style="font-size:14px;color:%s;font-weight:700;margin:0;">%s</p>\n'
        "      </section>" % (C_LIGHT, C_LINE, inline(left), C_MAIN, inline(right)))


def ask_card(ask, sub):
    return (
        '<section style="margin:0 10px 24px;padding:24px 22px;'
        "background:linear-gradient(135deg,%s 0%%,%s 100%%);border-radius:16px;text-align:center;"
        'color:#fff;">\n'
        '    <p style="font-size:18px;font-weight:800;margin:0 0 10px;">%s</p>\n'
        '    <p style="font-size:14px;margin:0 0 18px;opacity:0.9;line-height:1.7;">%s</p>\n'
        '    <p style="display:inline-block;margin:0;background:#fff;color:%s;font-size:14px;'
        "font-weight:700;padding:10px 26px;border-radius:999px;\">%s</p>\n"
        "  </section>" % (C_MAIN, C_DEEP, inline(ask), inline(sub), C_MAIN, leaf("下期见 · 评论区聊聊")))


def name_card():
    return (
        '<section style="margin:0 10px 28px;padding:20px 18px;background:#fff;'
        "border:1.5px solid %s;border-radius:16px;\">\n"
        '    <section style="display:flex;align-items:center;justify-content:space-between;gap:14px;">\n'
        '      <section style="flex:1;text-align:left;">\n'
        '        <p style="font-size:18px;font-weight:800;color:%s;margin:0 0 8px;">%s</p>\n'
        '        <p style="font-size:14px;color:#374151;margin:0 0 14px;line-height:1.6;">%s</p>\n'
        '        <p style="font-size:13px;color:%s;margin:0;font-weight:600;">%s</p>\n'
        "      </section>\n"
        '      <section style="flex:0 0 110px;width:110px;height:110px;background:#fff;'
        "border-radius:10px;overflow:hidden;border:1px solid %s;\">\n"
        '        <span leaf=""><img src="%s" style="width:100%%;height:100%%;display:block;" '
        'alt="公众号二维码"></span>\n'
        "      </section>\n"
        "    </section>\n"
        "  </section>"
        % (C_MAIN, C_MAIN, leaf("爱德数智"), leaf("分享 AI 观察与干货，用得上、看得懂"),
           C_MAIN, leaf("长按识别二维码 · 关注不迷路"), C_LINE, QR_IMG))


def sign_area():
    return (
        '  <section style="padding:0 10px;">\n'
        "    %s\n"
        "  </section>"
        % para("如果你觉得今天这篇有收获，欢迎 **点赞、在看、转发** 三连，我们下篇见。"))


def footer_quote(md_path):
    try:
        out = subprocess.run(
            [sys.executable, PICK_QUOTE, "--footer", "--source", "tech",
             "--color", C_MAIN, "--bg", C_LIGHT, "--deep", C_DEEP,
             "--avoid-file", md_path],
            capture_output=True, text=True, encoding="utf-8", timeout=60)
        if out.returncode == 0 and "<section" in out.stdout:
            return out.stdout.strip()
    except Exception:
        pass
    return ('<section style="padding:20px 0;margin-top:24px;text-align:center;">'
            '<p style="font-size:12px;font-weight:600;color:%s;line-height:1.9;margin:0 0 10px;">%s</p>'
            "</section>" % (C_DEEP, leaf("保持好奇，也要保持清醒。")))


def render_block(blk):
    """返回 (inner_html, is_chapter)。inner_html 已缩进 4 空格。"""
    head = blk[0].strip()

    m = re.match(r"^##\s+(.*?)(?:\s*<!--\s*(.*?)\s*-->)?$", head)
    if m:
        return ("CHAP", m.group(1).strip(), (m.group(2) or ""))

    if head.startswith("### "):
        return ("    " + sub_head(head[4:].strip()), None, None)

    if head.startswith("> "):
        text = " ".join(l[2:].strip() for l in blk)
        return ("QUOTE", text, None)

    mm = re.match(r"^!\[(.*?)\]\((.*?)\)$", head)
    if mm:
        return (image_block(mm.group(2), mm.group(1)), None, None)

    if head.startswith("|"):
        rows = []
        for l in blk:
            if re.match(r"^\|[\s:\-|]+\|$", l.strip()):
                continue
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            rows.append(cells)
        return ("    " + table_block(rows), None, None)

    if head.startswith("- "):
        items = ["    " + ul_item(l.strip()[2:]) for l in blk if l.strip().startswith("- ")]
        return ("\n".join(items), None, None)

    if re.match(r"^\d+\.\s", head):
        items = []
        for l in blk:
            m2 = re.match(r"^(\d+)\.\s+(.*)$", l.strip())
            if m2:
                items.append("    " + ol_item(m2.group(1), m2.group(2)))
        return ("\n".join(items), None, None)

    if set(head) == {"-"} or head.startswith("---"):
        return ("DIV", None, None)

    text = " ".join(l.strip() for l in blk)
    if len(blk) == 1 and re.match(r"^\*\*(.+?)\*\*$", text.strip()):
        text = text.strip().strip("*")
        return ('    <p style="font-size:15px;font-weight:800;color:#1C1917;margin:28px 0 14px;'
                'padding-left:10px;border-left:3px solid %s;line-height:1.4;">%s</p>'
                % (C_MAIN, inline(text)), None, None)
    if len(blk) == 1 and re.match(r"^\*(.+?)\*$", text.strip()):
        text = text.strip().strip("*")
        return ('    <p style="font-size:12px;color:#9CA3AF;margin:0 0 24px;'
                'line-height:1.8;text-align:left;">%s</p>' % inline(text), None, None)

    return ("    " + para(text), None, None)


def convert(md_path, ask, ask_sub):
    src = fix_quotes(open(md_path, encoding="utf-8").read())
    lines = src.replace("\r\n", "\n").split("\n")
    for i, ln in enumerate(lines):          # 末尾配图规范章节不进正文
        if "IMGSPEC" in ln:
            lines = lines[:i]
            break
    src = re.sub(r"<!--\s*IMGSPEC.*?-->", "", "\n".join(lines), flags=re.S)
    lines = src.split("\n")

    blocks, buf = [], []
    for ln in lines:
        if ln.strip() == "":
            if buf:
                blocks.append(buf)
                buf = []
        else:
            buf.append(ln)
    if buf:
        blocks.append(buf)

    body, num, open_sec, first_quote, last_div = [], 0, False, False, False
    pad_open = '<section style="padding:0 10px;">'
    pad_close = "</section>"

    for blk in blocks:
        if blk[0].strip().startswith("# "):
            continue

        kind, a, b = render_block(blk)
        if kind != "DIV":
            last_div = False          # 连续 --- 只渲染一条，避免文末叠线

        if kind == "CHAP":
            title, en = a, b
            if title.startswith("最后") or title.startswith("收心"):
                en = "END"
            if open_sec:
                body.append("  " + pad_close)
            num += 1
            if num > 1:
                body.append("  " + divider())
            body.append('  <section style="margin-top:%s;margin-bottom:28px;padding:0 10px;">'
                        % ("48px" if num > 1 else "16px"))
            body.append("    " + section_head(num, title, en))
            open_sec = True
            continue

        if kind == "QUOTE":
            if not first_quote:
                body.append("  " + intro_card(a))
                first_quote = True
            else:
                inner = "    " + quote_card(a)
                if open_sec:
                    body.append(inner)
                else:
                    body.append("  " + pad_open + "\n" + inner + "\n  " + pad_close)
            continue

        if kind == "DIV":
            if open_sec:
                body.append("  " + pad_close)
                open_sec = False
            if not last_div:
                body.append("  " + divider())
            last_div = True
            continue

        if open_sec:
            body.append(kind)
        else:
            body.append("  " + pad_open + "\n" + kind + "\n  " + pad_close)

    if open_sec:
        body.append("  " + pad_close)

    tail = [
        '  <section style="padding:0 10px;">',
        '    <section style="text-align:center;margin:0 0 32px;">',
        '      <section style="display:flex;align-items:center;justify-content:center;">',
        '        <span style="height:2px;width:60px;background:%s;margin-right:12px;">'
        '<span leaf=""><br></span></span>' % C_MAIN,
        '        <span style="font-size:11px;color:%s;letter-spacing:3px;font-weight:700;">%s</span>'
        % (C_MAIN, leaf("END")),
        '        <span style="height:2px;width:60px;background:%s;margin-left:12px;">'
        '<span leaf=""><br></span></span>' % C_MAIN,
        "      </section>",
        "    </section>",
        "  </section>",
        "  " + ask_card(ask, ask_sub),
        "  " + name_card(),
        "  " + sign_area(),
        "  " + footer_quote(md_path),
    ]

    return ('<section style="max-width:677px;margin:0 auto;background:#ffffff;'
            "font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB',"
            "'Microsoft YaHei',sans-serif;color:#374151;line-height:1.75;letter-spacing:0.5px;"
            'overflow-x:hidden;">\n\n'
            + "\n".join(body) + "\n\n" + "\n".join(tail) + "\n\n</section>\n")


def main():
    args = list(sys.argv[1:])
    if not args:
        print("用法: python md2gzh.py 文稿.md [--ask 问句] [--ask-sub 副文案] "
              "[--theme 主题] [--no-preview]")
        return
    md_path = args[0]
    ask = "这个假期，你用 AI 干过最有用的一件事是什么？"
    ask_sub = "评论区聊聊，小智攒一攒，节后做一期「大家用 AI 的真实清单」。"
    preview = True
    theme = "red-white"
    for i, a in enumerate(args):
        if a == "--ask":
            ask = args[i + 1]
        elif a == "--ask-sub":
            ask_sub = args[i + 1]
        elif a == "--theme":
            theme = args[i + 1]
        elif a == "--no-preview":
            preview = False

    label = apply_theme(theme)
    out_path = os.path.splitext(md_path)[0] + "_排版_%s(%s).html" % (label, theme)
    open(out_path, "w", encoding="utf-8").write(convert(md_path, ask, ask_sub))
    print("生成:", out_path)

    if preview and os.path.exists(WRAP_PREVIEW):
        subprocess.run([sys.executable, WRAP_PREVIEW, out_path])
        print("预览:", os.path.splitext(out_path)[0] + "_预览.html")


if __name__ == "__main__":
    main()
