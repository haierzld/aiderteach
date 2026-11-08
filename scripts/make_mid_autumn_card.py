# -*- coding: utf-8 -*-
"""中秋祝福卡片最终版：插画满幅铺底，文字全部叠在画面内（1080×1920，无水印）。"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC = r"d:\Users\Work\Trae\DoGongZongHao\images\A_warm_Mid_Autumn_Festival_gre_2026-09-24T13-20-18.png"
OUT = r"d:\Users\Work\Trae\DoGongZongHao\images\中秋快乐_小智科技_最终卡片.png"

BOLD = "C:/Windows/Fonts/msyhbd.ttc"
REG = "C:/Windows/Fonts/msyh.ttc"

W, H = 1080, 1920
GOLD = (255, 217, 160)
GOLD_SOFT = (232, 200, 145)
BLUE_SOFT = (176, 210, 255)
WHITE = (242, 247, 255)
DEEP = (9, 20, 43)

# ---------- 插画满幅铺底（cover 裁剪）----------
img = Image.open(SRC).convert("RGB")
scale = max(W / img.width, H / img.height)
nw, nh = round(img.width * scale), round(img.height * scale)
img = img.resize((nw, nh), Image.LANCZOS)
left, top_off = (nw - W) // 2, (nh - H) // 2
canvas = img.crop((left, top_off, left + W, top_off + H))

# ---------- 上下深色渐变遮罩（保证文字可读）----------
shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shade)
TOP_H, BOT_H = 420, 620
for y in range(TOP_H):
    a = int(235 * (1 - y / TOP_H) ** 1.15)
    sd.line([(0, y), (W, y)], fill=DEEP + (a,))
for i, y in enumerate(range(H - BOT_H, H)):
    a = int(225 * (i / BOT_H) ** 1.6)
    sd.line([(0, y), (W, y)], fill=DEEP + (a,))
canvas = Image.alpha_composite(canvas.convert("RGBA"), shade).convert("RGB")

d = ImageDraw.Draw(canvas)


def center(text, y, font, fill, anchor="mm"):
    d.text((W / 2, y), text, font=font, fill=fill, anchor=anchor)


def center_shadow(text, y, font, fill, dx=2, dy=3):
    d.text((W / 2 + dx, y + dy), text, font=font, fill=(20, 14, 8), anchor="mm")
    d.text((W / 2, y), text, font=font, fill=fill, anchor="mm")


def tracked(text, y, font, fill, gap=10, sw=2, sf=(255, 255, 255)):
    widths = [d.textlength(ch, font=font) for ch in text]
    total = sum(widths) + gap * (len(text) - 1)
    x = (W - total) / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=font, fill=fill, anchor="lm", stroke_width=sw, stroke_fill=sf)
        x += w + gap


def halo(text, y, font, fill, sw=5, sf=(255, 255, 255), sc=(24, 16, 6), blur=14):
    """深色字 + 浅色描边 + 高斯模糊投影：亮黄底上也清晰"""
    global canvas, d
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.text((W / 2, y), text, font=font, fill=sc + (255,), anchor="mm",
            stroke_width=sw + 8, stroke_fill=sc + (255,))
    canvas = Image.alpha_composite(
        canvas.convert("RGBA"), layer.filter(ImageFilter.GaussianBlur(blur))).convert("RGB")
    d = ImageDraw.Draw(canvas)
    d.text((W / 2, y), text, font=font, fill=fill, anchor="mm",
           stroke_width=sw, stroke_fill=sf)


f_en = ImageFont.truetype(REG, 30)
f_title = ImageFont.truetype(BOLD, 104)
f_sub = ImageFont.truetype(REG, 34)
f_line = ImageFont.truetype(REG, 42)
f_sign = ImageFont.truetype(REG, 30)

# ---------- 顶部文字（叠在画面内）----------
NAVY = (12, 44, 110)          # 亮黄底上的高对比主色
DEEP_BLUE = (20, 62, 142)

tracked("MID-AUTUMN FESTIVAL", 104, f_en, DEEP_BLUE, sw=3)
halo("中秋快乐", 190, f_title, NAVY, sw=5)

line_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ld = ImageDraw.Draw(line_layer)
for i in range(160):
    t = 1 - abs(i - 80) / 80
    x = W / 2 - 160 + i * 2
    ld.line([(x, 268), (x + 2, 268)], fill=DEEP_BLUE + (int(230 * t),))
canvas = Image.alpha_composite(canvas.convert("RGBA"), line_layer).convert("RGB")
d = ImageDraw.Draw(canvas)

halo("月满中秋 · 智慧同行", 308, f_sub, DEEP_BLUE, sw=3, blur=10)

# ---------- 底部文字（叠在画面内，不额外拉高画布）----------
center_shadow("愿你的上下文里永远有光", H - 380, f_line, WHITE)
center_shadow("愿你的输出里全是温柔", H - 320, f_line, WHITE)
center("—— 小智", H - 240, f_sign, GOLD_SOFT)

canvas.save(OUT, quality=95)
print("saved:", OUT, canvas.size)
