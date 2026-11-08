# -*- coding: utf-8 -*-
"""国庆祝福海报：公众号 3:4 竖版（1080×1440），文字避开人物头部，无黑色投影。"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import urllib.request

SRC = r"d:\Users\Work\Trae\DoGongZongHao\Bright_modern_tech_style_Natio_2026-09-28T12-26-15.png"
OUT = r"d:\Users\Work\Trae\DoGongZongHao\images\国庆快乐_爱德数智_海报_3x4.png"
QR_URL = "https://mmbiz.qpic.cn/sz_mmbiz_jpg/zeT1IrhsLLib9UkBbgKv2A7jfpyv4T5O3uAscIOuib1wHH4NibKALu7iaeSER3aC9jgFPZPgvHib0LWgYd5hhs5KjEvIcRia2aua48aUibYFNvibf2g/0?wx_fmt=jpeg&from=appmsg"

BOLD = "C:/Windows/Fonts/msyhbd.ttc"
REG = "C:/Windows/Fonts/msyh.ttc"

W, H = 1080, 1440               # 公众号贴图标准 3:4
RED = (185, 28, 28)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)
LIGHT = (255, 255, 255)
BLUE = (37, 99, 235)
BLUE_DEEP = (30, 64, 175)
INK = (31, 41, 55)

# ---------- 插画满幅铺底（居中裁切）----------
img = Image.open(SRC).convert("RGB")
scale = max(W / img.width, H / img.height)
nw, nh = round(img.width * scale), round(img.height * scale)
img = img.resize((nw, nh), Image.LANCZOS)
left, top_off = (nw - W) // 2, (nh - H) // 2
canvas = img.crop((left, top_off, left + W, top_off + H))

# ---------- 上下浅色渐变遮罩 ----------
shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shade)
TOP_H, BOT_H = 260, 520
for y in range(TOP_H):
    a = int(200 * (1 - y / TOP_H) ** 1.2)
    sd.line([(0, y), (W, y)], fill=LIGHT + (a,))
for i, y in enumerate(range(H - BOT_H, H)):
    a = int(215 * (i / BOT_H) ** 1.5)
    sd.line([(0, y), (W, y)], fill=LIGHT + (a,))
canvas = Image.alpha_composite(canvas.convert("RGBA"), shade).convert("RGB")

d = ImageDraw.Draw(canvas)


def center(text, y, font, fill, anchor="mm"):
    d.text((W / 2, y), text, font=font, fill=fill, anchor=anchor)


def tracked(text, y, font, fill, gap=12, sw=3, sf=WHITE):
    widths = [d.textlength(ch, font=font) for ch in text]
    total = sum(widths) + gap * (len(text) - 1)
    x = (W - total) / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=font, fill=fill, anchor="lm",
               stroke_width=sw, stroke_fill=sf)
        x += w + gap


f_en = ImageFont.truetype(REG, 28)
f_title = ImageFont.truetype(BOLD, 96)
f_sub = ImageFont.truetype(REG, 38)
f_line = ImageFont.truetype(REG, 32)
f_sign = ImageFont.truetype(REG, 28)

# ---------- 顶部只放节日主标题，避开人物头部 ----------
tracked("NATIONAL DAY · 2026", 70, f_en, BLUE, sw=3)
# 主标题：红字 + 金色细边，无黑色投影
d.text((W / 2, 155), "国庆快乐", font=f_title, fill=RED, anchor="mm",
       stroke_width=6, stroke_fill=GOLD)

# 金色分隔线
line_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ld = ImageDraw.Draw(line_layer)
for i in range(150):
    t = 1 - i / 150
    x = W / 2 - 150 + i * 2
    ld.line([(x, 230), (x + 2, 230)], fill=GOLD + (int(225 * t),))
canvas = Image.alpha_composite(canvas.convert("RGBA"), line_layer).convert("RGB")
d = ImageDraw.Draw(canvas)

# ---------- 底部放副标题、祝福语、二维码 ----------
# 副标题：深蓝字 + 白色细边
d.text((W / 2, 900), "盛世华诞 · 智启新程", font=f_sub, fill=BLUE_DEEP, anchor="mm",
       stroke_width=3, stroke_fill=WHITE)

center("愿你的每一次输出，都照亮一方山河", 980, f_line, INK)
center("与国同庆 · 智创未来", 1028, f_line, INK)

# 二维码（底部居中）
qr_data = urllib.request.urlopen(QR_URL, timeout=20).read()
qr = Image.open(BytesIO(qr_data)).convert("RGB").resize((140, 140), Image.LANCZOS)
qr_box = Image.new("RGB", (154, 154), WHITE)
qr_box.paste(qr, (7, 7))
qmask = Image.new("L", (154, 154), 0)
ImageDraw.Draw(qmask).rounded_rectangle([0, 0, 154, 154], radius=16, fill=255)
canvas.paste(qr_box, ((W - 154) // 2, H - 280), qmask)

center("—— 爱德数智 · 扫码关注", H - 70, f_sign, RED)

canvas.save(OUT, quality=95)
print("saved:", OUT, canvas.size)
