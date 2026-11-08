from PIL import Image, ImageDraw, ImageFont
import os

OUT = r"d:\Users\Work\Trae\DoGongZongHao\images\pub\大学AI\AI成了主角.png"
FONT_CN = r"C:\Windows\Fonts\msyh.ttc"
FONT_CN_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_EN = r"C:\Windows\Fonts\msyh.ttc"

# 8 所学校
schools = [
    ("北京大学", "Peking University", "北大", "PKU"),
    ("清华大学", "Tsinghua University", "清华", "THU"),
    ("复旦大学", "Fudan University", "复旦", "FDU"),
    ("上海交通大学", "Shanghai Jiao Tong", "上交", "SJTU"),
    ("武汉大学", "Wuhan University", "武大", "WHU"),
    ("中国科学技术大学", "Univ. of Sci. & Tech.", "中科大", "USTC"),
    ("重庆大学", "Chongqing University", "重大", "CQU"),
    ("哈尔滨工业大学", "Harbin Inst. of Tech.", "哈工大", "HIT"),
]

W, H = 1536, 1024
BG = "#F8FAFF"
PRIMARY = "#2563EB"
ACCENT = "#06B6D4"
TEXT_DARK = "#111827"
TEXT_MUTED = "#6B7280"

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# 可选：顶部一点渐变装饰条
d.rectangle([0, 0, W, 10], fill=PRIMARY)

# 标题
try:
    f_title = ImageFont.truetype(FONT_CN_BOLD, 42)
except:
    f_title = ImageFont.truetype(FONT_CN, 42)
f_sub = ImageFont.truetype(FONT_CN, 24)
f_abbr = ImageFont.truetype(FONT_CN_BOLD, 48)
f_en = ImageFont.truetype(FONT_EN, 20)

# 标题文字
y_title = 60
title = "8 所 985 高校校长致辞中的 AI"
bbox = d.textbbox((0, 0), title, font=f_title)
d.text(((W - (bbox[2]-bbox[0])) // 2, y_title), title, font=f_title, fill=PRIMARY)

sub = "五所学校把 AI 写进了 2026 级开学典礼"
bbox2 = d.textbbox((0, 0), sub, font=f_sub)
d.text(((W - (bbox2[2]-bbox2[0])) // 2, y_title + 60), sub, font=f_sub, fill=TEXT_MUTED)

# 卡片区域
start_y = 220
card_w, card_h = 320, 320
cols = 4
rows = 2
gap_x = 32
gap_y = 32
total_w = cols * card_w + (cols - 1) * gap_x
start_x = (W - total_w) // 2

# 调色板：4 种卡片底色循环
bg_colors = ["#FFFFFF", "#EEF2FF", "#F0FDF4", "#FAF5FF"]
border_colors = ["#E5E7EB", "#BFDBFE", "#A7F3D0", "#E9D5FF"]

for i, (cn, en, abbr, code) in enumerate(schools):
    col = i % cols
    row = i // cols
    x = start_x + col * (card_w + gap_x)
    y = start_y + row * (card_h + gap_y)
    
    # 卡片背景
    d.rounded_rectangle([x, y, x + card_w, y + card_h], radius=18,
                        fill=bg_colors[i % len(bg_colors)],
                        outline=border_colors[i % len(border_colors)], width=2)
    
    # 圆形徽章
    cx, cy = x + card_w // 2, y + 90
    r = 56
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PRIMARY)
    
    # 徽章内首字母/简称
    bbox3 = d.textbbox((0, 0), code, font=f_abbr)
    d.text((cx - (bbox3[2]-bbox3[0])//2, cy - (bbox3[3]-bbox3[1])//2 - 6),
           code, font=f_abbr, fill="white")
    
    # 中文校名
    bbox4 = d.textbbox((0, 0), cn, font=f_sub)
    d.text((cx - (bbox4[2]-bbox4[0])//2, y + 170), cn, font=f_sub, fill=TEXT_DARK)
    
    # 英文
    bbox5 = d.textbbox((0, 0), en, font=f_en)
    d.text((cx - (bbox5[2]-bbox5[0])//2, y + 215), en, font=f_en, fill=TEXT_MUTED)

# 底部说明
f_note = ImageFont.truetype(FONT_CN, 18)
note = "* 校名简称与英文代码仅供示意，图中不出现正式校徽"
bbox6 = d.textbbox((0, 0), note, font=f_note)
d.text(((W - (bbox6[2]-bbox6[0])) // 2, H - 50), note, font=f_note, fill="#9CA3AF")

img.save(OUT, "PNG")
print(f"Saved: {OUT}")
