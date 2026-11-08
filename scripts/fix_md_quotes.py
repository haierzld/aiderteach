# -*- coding: utf-8 -*-
"""把指定 MD 里的半角直引号成对替换为中文弯引号。"""
import glob
import sys

for p in glob.glob("第6*期*.md"):
    src = open(p, encoding="utf-8").read()
    if '"' not in src:
        continue
    out, flag = [], True
    for ch in src:
        if ch == '"':
            out.append("\u201c" if flag else "\u201d")
            flag = not flag
        else:
            out.append(ch)
    open(p, "w", encoding="utf-8").write("".join(out))
    print("修正引号:", p)
