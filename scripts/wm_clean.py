# -*- coding: utf-8 -*-
"""豆包「AI 生成」角标水印清除（沿用 NationDay/scripts/watermark.py 的 inpaint 思路）。

针对豆包水印做的适配：
1. 位置固定：右下角一条带。实测（按图高 H 归一化）
     横版 3008x1280：字高≈0.022H，串宽≈0.13H，y 在 H-0.048H ~ H-0.018H
     竖版 1728x2304：同上
   区域取 x∈[W-0.185W, W-0.015W]、y∈[H-0.055H, H-0.010H]。
2. 检测：豆包角标是「暗于背景」的浅灰字（NationDay 原版只找亮于背景的字，会漏检），
   这里用「局部中值背景差分」+「区域中位差分」两种候选取并集，
   能把极淡的字（只有 3~5 灰度差）以及压在主体上的字都找出来；
   再按「文字尺寸」过滤连通块，主体大色块不会被误判。
3. 修复：cv2.inpaint（TELEA + NS 二次修复）用邻域像素重建，
   只动水印笔画，背景纹理与主体完全保留，不会像填白那样留下白斑。

用法：
  python wm_clean.py <图片路径> [输出路径]        # 不传输出路径则生成 *_clean.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np

# ---- 水印区域（相对比例 x1,y1,x2,y2），右下角一条带 ----
# 实测豆包角标会向上/向右略有浮动，这里直接覆盖到底边和最右边缘，
# 宽度仍控制在水印串附近，避免大面积误伤主体。
WM_BOX = (0.815, 0.930, 0.995, 1.000)

LO1, HI1 = 5, 70     # 局部中值背景差分阈值
LO2, HI2 = 3, 60     # 区域中位差分阈值
MIN_AREA = 20        # 连通块最小面积
MAX_AREA_RATIO = 0.15   # 连通块面积占区域比例上限（超过视为主体）
MAX_H_RATIO = 0.80      # 连通块高度占区域比例上限


def _box(shape):
    """水印区像素坐标 x1,y1,x2,y2。"""
    H, W = shape
    return (int(WM_BOX[0] * W), int(WM_BOX[1] * H),
            min(W, int(WM_BOX[2] * W)), min(H, int(WM_BOX[3] * H)))


def _keep_blocks(m: np.ndarray, reg_h: int, limit_ratio: float) -> np.ndarray:
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = np.zeros_like(m)
    limit = m.size * limit_ratio
    for i in range(1, n):
        area = stats[i, 4]
        h = stats[i, 3]
        if MIN_AREA <= area <= limit and h <= reg_h * MAX_H_RATIO:
            keep[lab == i] = 255
    return keep


def _stroke_mask(gray: np.ndarray) -> np.ndarray:
    H, W = gray.shape
    x1, y1, x2, y2 = _box(gray.shape)
    reg = gray[y1:y2, x1:x2]
    if reg.size == 0:
        return np.zeros_like(gray)
    rh, rw = reg.shape

    # 1) 局部中值背景：核取 1.6 倍字高（≈0.035H），小字被抹平而主体保留
    k = int(round(0.035 * H)) | 1
    k = max(9, min(41, k))
    bgm = cv2.medianBlur(reg, k)
    d1 = np.abs(reg.astype(np.int16) - bgm.astype(np.int16))
    m1 = (((d1 > LO1) & (d1 < HI1))).astype(np.uint8) * 255

    # 2) 区域中位差分：应对极淡（3~5 灰度差）的字
    med = float(np.median(reg))
    d2 = np.abs(reg.astype(np.int16) - med)
    m2 = (((d2 > LO2) & (d2 < HI2))).astype(np.uint8) * 255

    m = cv2.bitwise_or(_keep_blocks(m1, rh, MAX_AREA_RATIO),
                       _keep_blocks(m2, rh, MAX_AREA_RATIO))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8), iterations=1)
    full = np.zeros_like(gray)
    full[y1:y2, x1:x2] = m
    return full


def _project_mask(gray: np.ndarray) -> np.ndarray:
    """列投影法：把水印字串按列分组，只生成竖条 mask，不碰左右边框/主体。"""
    H, W = gray.shape
    x1, y1, x2, y2 = _box(gray.shape)
    reg = gray[y1:y2, x1:x2]
    if reg.size == 0:
        return np.zeros_like(gray)
    k = max(5, min(21, int(round(0.025 * H)) | 1))
    bgm = cv2.medianBlur(reg, k)
    d = np.abs(reg.astype(np.int16) - bgm.astype(np.int16))
    proj = d.sum(axis=0).astype(np.float32)
    # 只看右侧 2/3，避开左边可能的主体/边框
    from_pos = proj.shape[0] // 3
    p2 = proj[from_pos:]
    med = float(np.median(p2))
    th = max(med * 1.8, med + 10)      # 阈值要低：淡字列峰值只比中位数高一点
    cols = np.where(p2 > th)[0] + from_pos
    if len(cols) < 3:
        return np.zeros_like(gray)
    # 合并连续列
    groups = []
    cur = [cols[0]]
    for c in cols[1:]:
        if c - cur[-1] <= 3:
            cur.append(c)
        else:
            groups.append(cur); cur = [c]
    groups.append(cur)
    m = np.zeros_like(reg)
    rw = reg.shape[1]
    max_cw = int(0.55 * rw)       # 超过一半宽视为主体，不处理
    for g in groups:
        c0, c1 = min(g), max(g)
        cw = c1 - c0 + 1
        if cw > max_cw:
            continue
        c0 = max(0, c0 - 2)
        c1 = min(rw - 1, c1 + 2)
        m[:, c0:c1 + 1] = 255
    full = np.zeros_like(gray)
    full[y1:y2, x1:x2] = m
    return full


def _bbox_mask(gray: np.ndarray) -> np.ndarray:
    """按实测几何推算的精确水印 bbox（检测失败时的兜底）。
    缩窄到只覆盖最右侧「生成」两字一带，避免碰到边框/主体。
    """
    H, W = gray.shape
    x1 = max(0, int(W - 0.020 * W - 0.100 * H))
    x2 = min(W, int(W - 0.010 * W))
    y1 = max(0, int(H - 0.045 * H))
    y2 = min(H, int(H - 0.018 * H))
    full = np.zeros_like(gray)
    full[y1:y2, x1:x2] = 255
    return full


def build_mask(gray: np.ndarray) -> tuple[np.ndarray, str]:
    """生成水印 mask，并返回处理方式：block=整块重建 / stroke=只修笔画。

    判断依据：用大核局部中值把小字抹平后，看水印带里还剩多少「大尺度结构」。
    结构很少 ⇒ 水印带是纯背景（绝大多数情况），直接整块 inpaint 最干净：
      inpaint 会用真实底色重建，而不是填白，所以任何底色都不会留白斑。
    结构较多 ⇒ 水印压在主体上，退化成只修笔画块，避免糊掉主体。
    """
    H, W = gray.shape
    x1, y1, x2, y2 = _box(gray.shape)
    reg = gray[y1:y2, x1:x2]
    if reg.size == 0:
        return np.zeros_like(gray), "none"

    k_big = max(15, min(41, int(round(0.03 * H)) | 1))
    bgm = cv2.medianBlur(reg, k_big)
    d_big = np.abs(reg.astype(np.int16) - bgm.astype(np.int16))
    struct = float((d_big > 8).mean())

    if struct < 0.08:                       # 水印带基本是纯背景
        full = np.zeros_like(gray)
        full[y1:y2, x1:x2] = 255
        return full, "block"

    m = _stroke_mask(gray)                  # 水印压在主体上：只修笔画
    return m, "stroke"


def clean_array(img: np.ndarray, pad: int = 3) -> tuple[np.ndarray, int, str]:
    out = img.copy()
    final_hits, final_mode = 0, "none"
    for it in range(3):
        gray = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
        mask, mode = build_mask(gray)
        hits = int((mask > 0).sum())
        if mode == "stroke" and hits < 300:   # 笔画没检出来：改用列投影
            mask, mode = _project_mask(gray), "project"
            hits = int((mask > 0).sum())
            if hits < 50:                     # 投影也没找到：用最窄的 bbox 兜底
                mask, mode = _bbox_mask(gray), "bbox"
                hits = int((mask > 0).sum())
        if not hits:
            break
        final_hits, final_mode = hits, mode
        if mode == "block":
            # 直接拿上方纯背景条带向下覆盖整条水印带，再用邻域羽化过渡。
            # 样本条带取水印区上方 0.10H 处，确保远离向上浮动的字影。
            H = out.shape[0]
            x1, y1, x2, y2 = _box(gray.shape)
            band = y2 - y1
            ref_h = max(band, int(0.10 * H))
            y0 = max(0, y1 - ref_h)
            bg = out[y0:y1, x1:x2].copy()
            if bg.size:
                bg = cv2.GaussianBlur(bg, (7, 7), 0)
                bg = np.median(bg, axis=0).astype(np.uint8)   # (W, 3)
                fill = np.tile(bg[None, :, :], (y2 - y1, 1, 1))  # (H, W, 3)
                feather = min(5, y1 - y0, y2 - y1)
                if feather > 1:
                    for r in range(feather):
                        alpha = r / feather
                        out[y1 + r, x1:x2] = (
                            alpha * out[y1 + r, x1:x2].astype(np.float32)
                            + (1 - alpha) * fill[r].astype(np.float32)
                        ).astype(np.uint8)
                    out[y1 + feather:y2, x1:x2] = fill[feather:]
                else:
                    out[y1:y2, x1:x2] = fill
            break

        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=pad)
        out = cv2.inpaint(out, mask, 8, cv2.INPAINT_TELEA)
        out = cv2.inpaint(out, mask, 5, cv2.INPAINT_NS)   # 二次修复去残留
    return out, final_hits, final_mode


def clean_file(src: str, dst: str | None = None, pad: int = 3) -> str:
    img = cv2.imdecode(np.fromfile(src, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(src)
    out, hits, mode = clean_array(img, pad=pad)
    dst = dst or str(Path(src).with_name(Path(src).stem + "_clean" + Path(src).suffix))
    cv2.imencode(Path(dst).suffix, out)[1].tofile(dst)
    print(f"{Path(src).name}: [{mode}] 命中 {hits} 像素 -> {Path(dst).name}")
    return dst


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        raise SystemExit(1)
    clean_file(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
