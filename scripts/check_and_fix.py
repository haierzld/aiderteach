# -*- coding: utf-8 -*-
"""检查 62-71 各篇排版隐患，并按新规则重生成排版。"""
import io
import os
import re
import subprocess
import sys

ITEMS = [
    ("第62期_AI越狱这件小事_没人指挥它自己翻了墙.md",
     "你最担心 AI 在哪件事上自作主张？",
     "评论区聊聊，小智攒一攒，做一期「AI 权限自查清单」。"),
    ("第63期_DevDay上篇_AI从对话框变成同事_dots与ChatGPT Space.md",
     "一个 7×24 在岗的 AI 同事，你敢用吗？",
     "评论区聊聊：你最想让它替你干哪件事，又绝对不敢交给它哪件事。"),
    ("第64期_DevDay下篇_7天一代的模型与砍半的额度.md",
     "500 美元一个月的 AI 会员，你会买吗？",
     "评论区聊聊你现在的 AI 订阅是哪一档，额度够不够用。"),
    ("第65期_90分钟里两家发布_AI价格战打到了每一件事多少钱.md",
     "你手上的 AI 订阅，是真用上了，还是咬牙买的？",
     "评论区聊聊，节后我做一期「普通人到底该买哪个 AI」。"),
    ("第66期_AI自己跑出去了_OpenAI承认越界并暂停最强模型训练.md",
     "你家孩子的设备、你的手机助手，权限都清理过吗？",
     "评论区聊聊，节后做一期「AI 权限自查清单」。"),
    ("第67期_给AI画个围栏_Docker把能做什么做成了标准.md",
     "你给 AI 开的权限，有几项是它其实用不到的？",
     "评论区聊聊，小智攒一攒，节后做一期「AI 权限清单」。"),
    ("第68期_dots豆包CodeBuddy有什么不一样_用七层看一遍.md",
     "你现在主要在哪个「AI 同事」上干活？",
     "评论区说说你的用法，我攒一攒做一期「大家的 AI 分工图鉴」。"),
    ("第69期_一个AI干不完就来一群_多智能体编排是怎么回事.md",
     "你有没有手动给 AI 分过工？说说你是怎么分的。",
     "评论区聊聊，节后做一期「普通人的 AI 分工手册」。"),
    ("第70期_出游回来才发现_路上真用得上的5个AI功能.md",
     "这趟假期，你用上 AI 了吗？",
     "评论区聊聊，我攒一攒，做一期「大家用 AI 的真实清单」，好用的和翻车的都放上去。"),
    ("第71期_把AI装进手机_30B端侧模型与Apple芯片提速3倍.md",
     "你手机里装过本地 AI 吗？没网的时候用上没？",
     "评论区聊聊，节后做一期「离线也能用的 AI」。"),
]

rep = ["# 排版检查报告（62–71）\n",
       "检查项：①独占一行的 `**短句**`（旧规则会被压成 12px 灰字）②独占一行的 `*短句*`（灰题注）"
       "③`## 章节` 缺 `<!-- 标记 -->` ④超长段落（>120 字）⑤配图占位数量\n"]

for fn, ask, sub in ITEMS:
    raw = io.open(fn, encoding="utf-8").read()
    lines = raw.replace("\r\n", "\n").split("\n")
    cut = next((i for i, l in enumerate(lines) if "IMGSPEC" in l), len(lines))
    body = lines[:cut]
    bold = [(i + 1, l.strip().strip("*")) for i, l in enumerate(body)
            if re.match(r"^\*\*[^*]+\*\*$", l.strip())]
    ital = [(i + 1, l.strip().strip("*")) for i, l in enumerate(body)
            if re.match(r"^\*[^*]+\*$", l.strip())]
    nochap = [(i + 1, l.strip()) for i, l in enumerate(body)
              if l.startswith("## ") and "<!--" not in l]
    longp = [(i + 1, len(l)) for i, l in enumerate(body) if len(l.strip()) > 120]
    imgs = sum(1 for l in body if l.startswith("!["))
    r = subprocess.run([sys.executable, "md2gzh.py", fn, "--ask", ask, "--ask-sub", sub],
                       capture_output=True, text=True, encoding="utf-8")
    rep.append("\n## %s\n" % fn)
    rep.append("- 配图占位：%d 处；超长段落：%d 处\n" % (imgs, len(longp)))
    rep.append("- ①加粗短句（%d）：%s\n" % (len(bold), "、".join(t for _, t in bold) or "无"))
    rep.append("- ②斜体题注（%d）：%s\n" % (len(ital), "、".join(t for _, t in ital) or "无"))
    rep.append("- ③章节缺标记（%d）：%s\n" % (len(nochap), "、".join(t for _, t in nochap) or "无"))
    if longp:
        rep.append("- ④超长段落行号：%s\n" % "、".join("%d行(%d字)" % (n, c) for n, c in longp[:8]))
    rep.append("- 重生成：%s\n" % (r.stdout.strip().splitlines()[0] if r.stdout.strip()
                                   else r.stderr.strip()[:150]))

io.open("_排版检查报告.md", "w", encoding="utf-8").write("".join(rep))
print("报告已生成：_排版检查报告.md")
