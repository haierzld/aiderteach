# -*- coding: utf-8 -*-
"""第82期配图 v4。

封面 82_01：还原上一版 —— 订单照片 + 制造表照片 双拼（照片原图，已脱敏）。
正文 82_02：订单照片原图 + 我们用 Excel 技能生成的「内部制造表」真实渲染图。

素材：
  客户订单照片  = 表格转换/客户材料/客户下单.jpg   （竖拍、内容横放；rotate -90）
  制造表照片    = 表格转换/客户材料/公司内部转换.jpg（竖拍、内容横放；rotate +90）
制造表数据源  = 表格转换/广州冠锋(NAKASONE)…制作表（内部生产）.xlsx
"""
import os
from PIL import Image, ImageDraw, ImageFont
import openpyxl

SRC = r"D:\Users\Work\Trae\表格转换\客户材料"
ROOT = r"D:\Users\Work\Trae\表格转换"
OUT = r"D:\Users\Work\Trae\DoGongZongHao\images\pub"

ORDER_IMG = os.path.join(SRC, "客户下单.jpg")
ORDER_XLS_IMG = os.path.join(OUT, "_src_82_order_excel.png")  # 订单 Excel 截图（德哥提供）
TABLE_IMG = os.path.join(SRC, "公司内部转换.jpg")
TABLE_XLSX = os.path.join(ROOT, "广州冠锋(NAKASONE)2026.09.25 活塞组件制作表（内部生产）.xlsx")

FONTS_B = [r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf"]
FONTS_R = [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simsun.ttc"]
C_LINE, C_HEAD_BG, C_HEAD_TX, C_TX = "#D1D5DB", "#F3F4F6", "#1C1917", "#374151"
C_MAIN, C_YELLOW = "#DC2626", "#FFF3C4"


def font(size, bold=False):
    for p in (FONTS_B if bold else FONTS_R):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def tw(d, t, f):
    bb = d.textbbox((0, 0), t, font=f)
    return bb[2] - bb[0], bb[3] - bb[1]


# ---------------- 照片处理 ----------------
def crop_work_area(im):
    w, h = im.size
    return im.crop((int(w*0.10), int(h*0.10), int(w*0.92), int(h*0.92)))


def redact(im, boxes):
    d = ImageDraw.Draw(im)
    W, H = im.size
    for (x0, y0, x1, y1) in boxes:
        d.rectangle([int(x0*W), int(y0*H), int(x1*W), int(y1*H)], fill=C_MAIN)
    return im


def prep_order_photo(top_ratio=None):
    o = Image.open(ORDER_IMG).convert("RGB").rotate(-90, expand=True)
    o = crop_work_area(o)
    def c(v):
        return (v - 0.10) / 0.82
    o = redact(o, [
        (c(0.28), c(0.185), c(0.72), c(0.215)),
        (c(0.25), c(0.225), c(0.60), c(0.245)),
        (c(0.10), c(0.235), c(0.95), c(0.275)),
        (c(0.815), c(0.27), c(0.95), c(0.76)),
        (c(0.60), c(0.70), c(0.80), c(0.83)),
        (c(0.10), c(0.775), c(0.95), c(0.835)),
    ])
    if top_ratio:
        o = o.crop((0, 0, o.width, int(o.height * top_ratio)))
    return o


def prep_table_photo():
    t = Image.open(TABLE_IMG).convert("RGB").rotate(90, expand=True)
    t = crop_work_area(t)
    def c(v):
        return (v - 0.10) / 0.82
    t = redact(t, [
        (c(0.28), c(0.045), c(0.75), c(0.075)),
        (c(0.36), c(0.155), c(0.62), c(0.185)),
        (c(0.28), c(0.955), c(0.85), c(1.00)),
    ])
    return t


def fit_h(im, h):
    return im.resize((int(im.width*h/im.height), h))


# ---------------- 制造表渲染 ----------------
def draw_table(cols, rows, col_w, row_h, head_h, title=None, scale=1, highlight=None):
    W = sum(col_w)
    H = head_h + row_h*len(rows) + (row_h if title else 0)
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    f_h = font(int(20*scale), bold=True)
    y = 0
    if title:
        d.rectangle([0, 0, W, row_h], fill=C_MAIN)
        bw, _ = tw(d, title, f_h)
        d.text(((W-bw)//2, (row_h-int(20*scale))//2), title, font=f_h, fill="white")
        y = row_h
    x = 0
    for i, c in enumerate(cols):
        d.rectangle([x, y, x+col_w[i], y+head_h], fill=C_HEAD_BG, outline=C_LINE)
        bw, bh = tw(d, c, f_h)
        d.text((x+(col_w[i]-bw)//2, y+(head_h-bh)//2-2), c, font=f_h, fill=C_HEAD_TX)
        x += col_w[i]
    y += head_h
    for ri, row in enumerate(rows):
        bg = C_YELLOW if (highlight and ri in highlight) else "white"
        x = 0
        for ci, val in enumerate(row):
            d.rectangle([x, y, x+col_w[ci], y+row_h], fill=bg, outline=C_LINE)
            s = str(val)
            fs = int(18*scale); f_c = font(fs)
            while tw(d, s, f_c)[0] > col_w[ci]-8 and fs > 10:
                fs -= 1; f_c = font(fs)
            bw, bh = tw(d, s, f_c)
            d.text((x+(col_w[ci]-bw)//2, y+(row_h-bh)//2-2), s, font=f_c, fill=C_TX)
            x += col_w[ci]
        y += row_h
    return im


def render_table(scale=1, max_group=4):
    wb = openpyxl.load_workbook(TABLE_XLSX)
    ws = wb.active
    tiers = ["STD", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]
    rows, hl = [], set()
    r, grp = 5, 0
    while r <= ws.max_row and grp < max_group:
        car = ws.cell(r, 2).value
        if car is None:
            break
        rows.append([str(car), str(ws.cell(r, 3).value or ""), str(ws.cell(r, 4).value or "")]
                    + ["" if ws.cell(r, c).value is None else str(ws.cell(r, c).value)
                       for c in range(5, 14)] + [str(ws.cell(r, 14).value or "")])
        r2 = r+1
        rows.append([str(ws.cell(r2, 2).value or ""), str(ws.cell(r2, 3).value or ""),
                     str(ws.cell(r2, 4).value or "")]
                    + ["" if ws.cell(r2, c).value is None else str(ws.cell(r2, c).value)
                       for c in range(5, 14)] + [""])
        r3 = r+2
        rows.append([str(ws.cell(r3, 2).value or ""), str(ws.cell(r3, 4).value or ""), ""]
                    + ["" if ws.cell(r3, c).value is None else str(ws.cell(r3, c).value)
                       for c in range(5, 14)] + [""])
        hl.add(len(rows)-1)
        grp += 1; r += 3
    cols = ["车种", "代号", "规格"] + tiers + ["备注"]
    cw = [int(100*scale), int(150*scale), int(122*scale)] + [int(38*scale)]*9 + [int(58*scale)]
    return draw_table(cols, rows, cw, int(30*scale), int(36*scale),
                      title="内部制造表（技能生成 · 已脱敏）", scale=scale, highlight=hl)


def center_text(d, W, text, y, f, fill):
    bw, _ = tw(d, text, f)
    d.text(((W-bw)//2, y), text, font=f, fill=fill)


# ---------------- 组图 ----------------
def make_cover():
    o = fit_h(prep_order_photo(top_ratio=0.55), 700)
    t = fit_h(prep_table_photo(), 700)
    GAP = 24
    W = o.width + t.width + GAP*3
    canvas = Image.new("RGB", (W, 700+GAP*2+46), "white")
    canvas.paste(o, (GAP, GAP))
    canvas.paste(t, (GAP*2+o.width, GAP))
    d = ImageDraw.Draw(canvas)
    d.text((GAP+o.width+GAP//2-16, GAP+350-26), "→", font=font(44, True), fill=C_MAIN)
    center_text(d, canvas.width,
                "左：客户订单（照片·已脱敏）　→　右：内部制造表（照片·已脱敏）",
                700+GAP*2+10, font(18), "#6B7280")
    canvas = canvas.resize((900, int(canvas.height*900/canvas.width)))
    out = os.path.join(OUT, "82_01_封面_订单转制造单.png")
    canvas.save(out)
    print("生成:", out, canvas.size)


def prep_order_xls_img():
    """订单 Excel 截图：遮 PO 号、BRAND 列（NAKASONE）、剪贴板红点。"""
    im = Image.open(ORDER_XLS_IMG).convert("RGB")
    im = redact(im, [
        (0.415, 0.010, 0.590, 0.080),   # (PO-GF260925)
        (0.778, 0.125, 0.862, 0.935),   # BRAND 列 NAKASONE
        (0.135, 0.120, 0.180, 0.170),   # 截图红点标记
    ])
    return im


def make_article():
    # 上：订单 Excel 截图（德哥提供，脱敏）；下：技能生成的制造表渲染图
    o = prep_order_xls_img()
    t = render_table(scale=1.0, max_group=4)
    GAP = 26
    TARGET_W = 900
    o = o.resize((TARGET_W, int(o.height*TARGET_W/o.width)))
    if t.width > TARGET_W:
        t = t.resize((TARGET_W, int(t.height*TARGET_W/t.width)))

    f_lab = font(24, True)
    ARROW_H = 100
    H = GAP + 40 + o.height + ARROW_H + 40 + t.height + 40 + GAP
    W = TARGET_W + GAP*2
    canvas = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(canvas)
    y = GAP
    canvas.paste(o, ((W-o.width)//2, y)); y += o.height
    center_text(d, W, "客户订单（原始单据 · 已脱敏）", y+6, f_lab, C_HEAD_TX); y += 40
    d.text((W//2-26, y+8), "↓", font=font(50, True), fill=C_MAIN)
    center_text(d, W, "WorkBuddy 技能：识别厂家 → 查规则 → 填表 → 九项自检", y+62, font(18), "#6B7280")
    y += ARROW_H
    canvas.paste(t, ((W-t.width)//2, y)); y += t.height
    center_text(d, W, "内部制造表（技能生成 · 已脱敏）", y+6, f_lab, C_HEAD_TX)
    canvas = canvas.resize((900, int(canvas.height*900/canvas.width)))
    out = os.path.join(OUT, "82_02_从订单到制造表.png")
    canvas.save(out)
    print("生成:", out, canvas.size)


if __name__ == "__main__":
    make_cover()
    make_article()
