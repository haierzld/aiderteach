# -*- coding: utf-8 -*-
"""读 MD 里的「配图提示词」→ 用 NationDay 的本地浏览器能力出图 → 清角标 → 裁切 → 压图。

用法：
  python gen_gzh_img.py --issues 66-71 --dry-run     # 只看任务，不出图
  python gen_gzh_img.py --only 66 --limit 1          # 先试跑第 66 期第 1 张（封面）
  python gen_gzh_img.py --issues 66-71               # 全量

前置：本机 Chrome / Edge 已登录豆包（或千问 / 即梦），运行前请完全退出该浏览器。
提示词直接取 MD 原文，不改写；只在提交时追加一句画面比例。
"""
import argparse
import re
import sys
import time
from pathlib import Path

ND = Path(r"D:\Users\Work\Trae\NationDay\scripts")
ROOT = Path(r"d:\Users\Work\Trae\DoGongZongHao")
sys.path.insert(0, str(ND))

import generate_browser as gb  # noqa: E402
from PIL import Image  # noqa: E402

# 平台会在右下角压「豆包 AI 生成」水印（见 wm_clean.py：
# 水印区约 x∈[W-0.185W, W-0.015W]、y∈[H-0.055H, H-0.010H]）。
# 只要求「紧贴底边的一条极窄带」保持纯白即可 —— 不能说成右下角一大块，
# 否则对 2.35:1 的超宽封面，AI 会为了避让而把主体缩得很小。
SAFE_BELT_235 = ("；纯白 #FFFFFF 背景，禁止渐变、灰色底、阴影层次与纹理"
                 "；主体必须大而饱满地占满 2.35:1 超宽画幅，不要缩小主体"
                 "；仅画面最底部一条约 5% 高的极窄带保持纯白空置，"
                 "不放任何元素、线条、边框、阴影")
SAFE_BELT_34 = ("；纯白 #FFFFFF 背景，禁止渐变、灰色底、阴影层次与纹理"
                "；主体必须大而饱满地占满 3:4 画幅，不要缩小主体"
                "；仅画面最底部一条约 4% 高的极窄带保持纯白空置，"
                "不放任何元素、线条、边框、阴影")

# 图1 = 封面（2.35:1 宽幅），图2/3 = 正文（3:4 竖版）
SPEC = {
    1: {"ratio": "16:9", "crop": "2.35:1", "long": 900,
        "hint": "；画面为 2.35:1 超宽横幅构图，不要任何文字" + SAFE_BELT_235},
    2: {"ratio": "3:4", "crop": "3:4", "long": 1200,
        "hint": "；画面为 3:4 竖版构图，不要任何文字" + SAFE_BELT_34},
    3: {"ratio": "3:4", "crop": "3:4", "long": 1200,
        "hint": "；画面为 3:4 竖版构图，不要任何文字" + SAFE_BELT_34},
}


def extract(md_path):
    """提取 MD 里「配图提示词（3幅，供小编生成）」下的图1/图2/图3 原文。"""
    txt = md_path.read_text(encoding="utf-8")
    m = re.search(r"##\s*配图提示词[^\n]*\n+(.*?)(?=\n##\s|\Z)", txt, re.S)
    if not m:
        return []
    tasks = []
    for mm in re.finditer(r"\*\*图(\d)（([^）]+)）\*\*：(.+)", m.group(1)):
        idx = int(mm.group(1))
        name = mm.group(2).split("，")[0].strip()
        name = re.sub(r'[：:/*?"<>|\\]', "_", name)
        prompt = mm.group(3).strip().rstrip("。")
        tasks.append({"idx": idx, "name": name, "prompt": prompt})
    return tasks


def build_tasks(issues):
    out = []
    for md in sorted(ROOT.glob("第*_*.md")):
        m = re.match(r"第(\d+)期", md.name)
        if not m or int(m.group(1)) not in issues:
            continue
        shots = extract(md)
        if not shots:
            print("跳过（无配图提示词）:", md.name)
            continue
        no = m.group(1)
        outdir = "images/第%s期" % no
        for s in shots:
            sp = SPEC[s["idx"]]
            out.append({
                "no": no,
                "src_md": md.name,
                "name": s["name"],
                "prompt": s["prompt"] + sp["hint"],
                "ratio": sp["ratio"],
                "crop": sp["crop"],
                "long": sp["long"],
                "out": "%s/%s_0%d_%s.jpg" % (outdir, no, s["idx"], s["name"]),
            })
    return out


def wait_new(page, known, timeout, target_wh):
    """按目标宽高比（w/h）挑新出现的图。"""
    time.sleep(4)
    deadline = time.time() + timeout
    best, best_at = None, 0.0
    while time.time() < deadline:
        for im in gb._collect_imgs(page):
            src = im.get("src") or ""
            if not src or src in known or src.startswith("data:"):
                continue
            wh = im["w"] / max(im["h"], 1)
            if abs(wh - target_wh) <= 0.15:
                known.add(src)
                return im
            if best is None or abs(wh - target_wh) < abs(best["w"] / max(best["h"], 1) - target_wh):
                best, best_at = im, time.time()
        if best is not None and time.time() - best_at >= 15:
            known.add(best["src"])
            return best
        time.sleep(2)
    if best:
        known.add(best["src"])
    return best


def _remove_watermark(path):
    """清平台角标：inpaint 用邻域重建，底色是什么就补什么（不填白、不留白斑）。"""
    try:
        import cv2
        import numpy as np
        import wm_clean
        arr = cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), cv2.IMREAD_COLOR)
        if arr is None:
            return
        out, hits, mode = wm_clean.clean_array(arr)
        cv2.imencode(".png", out)[1].tofile(str(path))
        print("  去水印[%s]：%d 像素" % (mode, hits))
    except Exception as e:
        print("  去水印失败：%s" % e)


def post_process(src_path, out_path, crop, long_edge):
    _remove_watermark(src_path)                   # 清平台角标水印
    img = Image.open(src_path).convert("RGB")
    tw, th = crop.split(":")
    target = float(tw) / float(th)
    w, h = img.size
    if w / h > target:
        nw = int(h * target)
        img = img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / target)
        img = img.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    w, h = img.size
    scale = long_edge / max(w, h)
    if scale < 1:
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    out = ROOT / out_path
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "JPEG", quality=88, optimize=True)
    print("  成品：%s  %dx%d" % (out_path, img.size[0], img.size[1]))
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--issues", default="66-71")
    ap.add_argument("--only", type=int, default=None)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--platform", default="doubao")
    ap.add_argument("--browser", default="Chrome")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--skip-existing", action="store_true", help="已存在的成品图跳过不重出")
    args = ap.parse_args()

    if args.only:
        issues = [args.only]
    else:
        a, b = args.issues.split("-")
        issues = list(range(int(a), int(b) + 1))

    tasks = build_tasks(issues)
    if args.skip_existing:
        tasks = [t for t in tasks if not (ROOT / t["out"]).exists()]
    if args.limit:
        tasks = tasks[:args.limit]
    if not tasks:
        print("没有可生成的任务。")
        return
    print("共 %d 张：\n" % len(tasks))
    for t in tasks:
        print("  [%s 图%s] %s → %s (%s)" % (t["no"], t["idx"] if "idx" in t else "",
                                            t["name"], t["out"], t["crop"]))
    if args.dry_run:
        return

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("缺少 playwright：pip install playwright")
        return

    platform = gb.PLATFORMS.get(args.platform) or gb.PLATFORMS.get(args.platform.lower())
    browsers = gb.detect_browsers()
    if not browsers:
        print("未检测到本地 Chrome / Edge。")
        return
    br = next((b for b in browsers if args.browser.lower() in b["name"].lower()), browsers[0])
    print("\n使用浏览器：%s" % br["name"])
    profile = gb._copy_profile(br["user_data_dir"], gb.profile_cache_dir(br))

    tmp_dir = ROOT / "_img_tmp"
    tmp_dir.mkdir(exist_ok=True)
    done = []

    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(
            user_data_dir=profile,
            executable_path=br["exe"],
            headless=False,
            args=["--disable-blink-features=AutomationControlled", "--no-first-run",
                  "--no-default-browser-check"],
            viewport={"width": 1280, "height": 900},
        )
        try:
            for i, t in enumerate(tasks, 1):
                print("\n(%d/%d) 第%s期 · %s" % (i, len(tasks), t["no"], t["name"]))
                target_wh = float(t["crop"].split(":")[0]) / float(t["crop"].split(":")[1])
                page = ctx.new_page()
                page.goto(platform["url"], wait_until="domcontentloaded", timeout=120000)
                time.sleep(6)
                gb._dismiss_overlays(page)
                page = gb._enter_image_mode(ctx, page, platform)
                gb._set_ratio(page, t["ratio"])
                box = gb._find_input(page, platform["inputs"])
                if box is None:
                    print("  未定位到输入框（多半未登录）。请在窗口里登录后回车继续…")
                    input()
                    page.reload(wait_until="domcontentloaded")
                    time.sleep(8)
                    page = gb._enter_image_mode(ctx, page, platform)
                    box = gb._find_input(page, platform["inputs"])
                known = set()
                try:
                    for im in page.evaluate(
                            "() => Array.from(document.images).map(i => i.currentSrc || i.src)"):
                        known.add(im)
                except Exception:
                    pass
                for im in gb._collect_imgs(page):
                    known.add(im["src"])
                if box:
                    try:
                        box.fill(t["prompt"])
                        time.sleep(1)
                        page.keyboard.press("Enter")
                        time.sleep(2)
                        gb._ensure_sent(page, box)
                        print("  已提交，等待出图…")
                    except Exception as e:
                        print("  填入失败：%s" % e)
                        box = None
                if not box:
                    gb._set_clipboard(t["prompt"])
                    print("  提示词已复制，请在窗口粘贴发送，脚本继续等待…")
                im = wait_new(page, known, args.timeout, target_wh)
                if im:
                    tmp = tmp_dir / ("t%d.png" % i)
                    if gb._save_image(ctx, page, im["src"], tmp):
                        post_process(tmp, t["out"], t["crop"], t["long"])
                        done.append(t["out"])
                    else:
                        print("  下载失败")
                else:
                    print("  等待超时，未捕获图片")
                page.close()
        finally:
            ctx.close()

    print("\n完成 %d/%d 张" % (len(done), len(tasks)))
    for d in done:
        print("  " + d)


if __name__ == "__main__":
    main()
