from PIL import Image, ImageDraw, ImageFont
import os, re, urllib.request, urllib.error, ssl, tempfile
from urllib.parse import urljoin, urlparse

OUT = r"d:\Users\Work\Trae\DoGongZongHao\images\pub\大学AI\AI成了主角.png"
FONT_CN = r"C:\Windows\Fonts\msyh.ttc"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"

schools = [
    ("北京大学", "PKU", "https://www.pku.edu.cn/"),
    ("清华大学", "THU", "https://www.tsinghua.edu.cn/"),
    ("复旦大学", "FDU", "https://www.fudan.edu.cn/"),
    ("上海交通大学", "SJTU", "https://www.sjtu.edu.cn/"),
    ("武汉大学", "WHU", "https://www.whu.edu.cn/"),
    ("中国科学技术大学", "USTC", "https://www.ustc.edu.cn/"),
    ("重庆大学", "CQU", "https://www.cqu.edu.cn/"),
    ("哈尔滨工业大学", "HIT", "https://www.hit.edu.cn/"),
]

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def fetch_text(url):
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            return r.read().decode("utf-8", "ignore")
    except Exception as e:
        print(f"  fetch text failed: {e}")
        return ""

def fetch_bytes(url):
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            return r.read()
    except Exception as e:
        print(f"  fetch bytes failed: {e}")
        return b""

def guess_logo_url(base_url, html):
    # 1. img tags near logo-like words
    for m in re.finditer(r'<img[^>]*>', html, re.I):
        tag = m.group(0)
        if re.search(r'logo|校徽|标识|校标| emblem |school', tag, re.I):
            src = re.search(r'src=["\']([^"\']+)["\']', tag)
            if src:
                return urljoin(base_url, src.group(1))
    # 2. any img src with logo in path
    for src in re.findall(r'src=["\']([^"\']*logo[^"\']*)["\']', html, re.I):
        return urljoin(base_url, src)
    # 3. css background-image with logo
    m = re.search(r'background(?:-image)?\s*:\s*[^;]*url\(["\']?([^"\')]+)["\']?\)[^;]*logo', html, re.I)
    if m:
        return urljoin(base_url, m.group(1))
    # 4. favicon as fallback
    m = re.search(r'<link[^>]*rel=["\']?(?:shortcut )?icon["\']?[^>]*href=["\']([^"\']+)["\']', html, re.I)
    if m:
        return urljoin(base_url, m.group(1))
    return ""

def download_logo(school, abbr, url):
    print(f"Fetching {school} ...")
    html = fetch_text(url)
    if not html:
        return None
    logo_url = guess_logo_url(url, html)
    if not logo_url:
        print(f"  no logo url found, fallback to placeholder")
        return None
    print(f"  logo url: {logo_url}")
    data = fetch_bytes(logo_url)
    if not data:
        return None
    # try open image
    try:
        ext = os.path.splitext(urlparse(logo_url).path)[1].lower() or ".png"
        if ext not in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"):
            ext = ".png"
        fd, tmp = tempfile.mkstemp(suffix=ext)
        os.close(fd)
        with open(tmp, "wb") as f:
            f.write(data)
        if ext == ".svg":
            # 需要 cairosvg 或 svglib，不一定有，直接放弃
            os.unlink(tmp)
            return None
        img = Image.open(tmp).convert("RGBA")
        os.unlink(tmp)
        # filter tiny images (favicon usually 16x16)
        if max(img.size) < 32:
            print(f"  too small ({img.size}), fallback")
            return None
        return img
    except Exception as e:
        print(f"  open image failed: {e}")
        return None

def make_placeholder(abbr, cn=None):
    size = 200
    img = Image.new("RGBA", (size, size), (255,255,255,0))
    d = ImageDraw.Draw(img)
    r = size // 2
    d.ellipse([0, 0, size, size], fill="#2563EB")
    try:
        font_bold = ImageFont.truetype(FONT_BOLD, 60)
        font_cn = ImageFont.truetype(FONT_BOLD, 64)
    except:
        font_bold = ImageFont.truetype(FONT_CN, 60)
        font_cn = ImageFont.truetype(FONT_CN, 64)
    text = cn if cn else abbr
    font = font_cn if any(ord(c) > 127 for c in text) else font_bold
    bbox = d.textbbox((0,0), text, font=font)
    d.text(((size-(bbox[2]-bbox[0]))//2, (size-(bbox[3]-bbox[1]))//2 - 8), text, font=font, fill="white")
    return img

W, H = 1536, 1024
BG = "#F8FAFF"
PRIMARY = "#2563EB"
TEXT_DARK = "#111827"
TEXT_MUTED = "#6B7280"

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# top bar
d.rectangle([0, 0, W, 10], fill=PRIMARY)

f_title = ImageFont.truetype(FONT_BOLD, 42)
f_sub = ImageFont.truetype(FONT_CN, 24)
f_note = ImageFont.truetype(FONT_CN, 18)

title = "8 所 985 高校校长致辞中的 AI"
bbox = d.textbbox((0,0), title, font=f_title)
d.text(((W-(bbox[2]-bbox[0]))//2, 55), title, font=f_title, fill=PRIMARY)
sub = "五所学校把 AI 写进了 2026 级开学典礼"
bbox2 = d.textbbox((0,0), sub, font=f_sub)
d.text(((W-(bbox2[2]-bbox2[0]))//2, 120), sub, font=f_sub, fill=TEXT_MUTED)

start_y = 200
card_w, card_h = 330, 350
cols, rows = 4, 2
gap_x, gap_y = 28, 28
total_w = cols*card_w + (cols-1)*gap_x
start_x = (W-total_w)//2

bg_colors = ["#FFFFFF", "#EEF2FF", "#FAF5FF", "#F0FDF4"]
border_colors = ["#E5E7EB", "#BFDBFE", "#E9D5FF", "#A7F3D0"]

for i, (cn, abbr, url) in enumerate(schools):
    col = i % cols
    row = i // cols
    x = start_x + col*(card_w+gap_x)
    y = start_y + row*(card_h+gap_y)
    # card
    d.rounded_rectangle([x, y, x+card_w, y+card_h], radius=18,
                        fill=bg_colors[i%4], outline=border_colors[i%4], width=2)
    cx = x + card_w//2
    
    logo = download_logo(cn, abbr, url)
    if logo:
        # scale to fit inside 180x180, keep aspect
        logo.thumbnail((180, 180), Image.Resampling.LANCZOS)
        lw, lh = logo.size
        lx = cx - lw//2
        ly = y + 60
        # paste on white bg to avoid transparency issue
        back = Image.new("RGBA", (lw, lh), (255,255,255,255))
        back.paste(logo, (0,0), logo)
        img.paste(back.convert("RGB"), (lx, ly))
        logo_source = "官网"
    else:
        ph = make_placeholder(abbr, cn)
        ph.thumbnail((160,160), Image.Resampling.LANCZOS)
        img.paste(ph.convert("RGB"), (cx-80, y+60))
        logo_source = "占位"
    
    # school name
    bbox3 = d.textbbox((0,0), cn, font=f_sub)
    d.text((cx-(bbox3[2]-bbox3[0])//2, y+250), cn, font=f_sub, fill=TEXT_DARK)
    print(f"  -> used {logo_source}")

note = "* 真实 Logo 来自各校官网首页，抓取失败的用英文代码占位"
bbox4 = d.textbbox((0,0), note, font=f_note)
d.text(((W-(bbox4[2]-bbox4[0]))//2, H-45), note, font=f_note, fill="#9CA3AF")

img.save(OUT, "PNG")
print(f"Saved: {OUT}")
