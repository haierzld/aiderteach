# -*- coding: utf-8 -*-
"""把排版好的 HTML 发布到公众号草稿箱。

用法：
    python publish_draft.py --html 第59期_Jev到底是什么_排版_小智科技(xiaozhi-tech).html

可选：
    --cover  封面图路径（默认取正文第一张本地图）
    --title  标题（默认从 HTML 封面卡提取）
    --digest 摘要（默认取副标题）
    --author 作者（默认 小智）

前置：config/config.ini 填好 AppID/AppSecret，且本机公网 IP 已加入公众号后台 IP 白名单。
仅用标准库，无需安装第三方包。
"""
import argparse
import configparser
import json
import mimetypes
import os
import re
import urllib.request
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = os.path.join(ROOT, "config", "config.ini")
API = "https://api.weixin.qq.com/cgi-bin"


# ---------------- 基础请求 ----------------
def get(url):
    with urllib.request.urlopen(url, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def post_json(url, obj):
    data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def multipart_post(url, file_field, file_path):
    boundary = "----CbFormBoundary" + uuid.uuid4().hex
    filename = os.path.basename(file_path)
    ctype = mimetypes.guess_type(filename)[0] or "image/png"
    with open(file_path, "rb") as f:
        content = f.read()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{file_field}"; filename="{filename}"\r\n'
        f"Content-Type: {ctype}\r\n\r\n"
    ).encode("utf-8") + content + f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def die(msg, res=None):
    print("❌ " + msg)
    if res is not None:
        print("   接口返回:", json.dumps(res, ensure_ascii=False))
    raise SystemExit(1)


# ---------------- 微信接口 ----------------
def get_token(appid, secret):
    res = get(f"{API}/token?grant_type=client_credential&appid={appid}&secret={secret}")
    if "access_token" not in res:
        if res.get("errcode") == 40164:
            die("本机 IP 不在公众号白名单。把上面 errmsg 里的 IP 加到 "
                "公众号后台 → 设置与开发 → 基本配置 → IP白名单，再重跑。", res)
        die("获取 access_token 失败", res)
    return res["access_token"]


def upload_content_image(token, path):
    """正文内图片 → 返回可在正文使用的微信图床 URL"""
    res = multipart_post(f"{API}/media/uploadimg?access_token={token}", "media", path)
    url = res.get("url")
    if not url:
        die(f"正文图片上传失败: {os.path.basename(path)}", res)
    return url.replace("http://", "https://")


def upload_thumb(token, path):
    """封面 → 永久素材，返回 thumb_media_id"""
    res = multipart_post(
        f"{API}/material/add_material?access_token={token}&type=image", "media", path)
    mid = res.get("media_id")
    if not mid:
        die(f"封面上传失败: {os.path.basename(path)}", res)
    return mid


def add_draft(token, article):
    res = post_json(f"{API}/draft/add?access_token={token}", {"articles": [article]})
    if "media_id" not in res:
        if res.get("errcode") == 48001:
            die("接口未授权：草稿箱/素材接口需要已微信认证的公众号，未认证订阅号没有该权限。", res)
        die("新建草稿失败", res)
    return res["media_id"]


# ---------------- 主流程 ----------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--cover", default=None)
    ap.add_argument("--title", default=None)
    ap.add_argument("--digest", default=None)
    ap.add_argument("--author", default="小智")
    ap.add_argument("--update", default=None,
                    help="已有草稿 media_id：传了则更新该草稿而不是新建")
    args = ap.parse_args()

    cfg = configparser.ConfigParser()
    cfg.read(CFG, encoding="utf-8")
    appid = cfg["公众号"]["AppID"].strip()
    secret = cfg["公众号"]["AppSecret"].strip()
    print(f"公众号：{cfg['公众号'].get('公众号', '')}  AppID：{appid}")

    html_path = args.html if os.path.isabs(args.html) else os.path.join(ROOT, args.html)
    with open(html_path, encoding="utf-8") as f:
        html = f.read()

    # 默认标题/摘要：从封面卡提取
    if not args.title:
        m = re.search(r'<h1[^>]*>.*?<span leaf="">(.*?)</span>', html, re.S)
        args.title = (m.group(1) if m else os.path.splitext(os.path.basename(html_path))[0])
    if not args.digest:
        m = re.search(r'font-size:14px;color:(?:rgba\(255,255,255,0\.75\)|#6B7280)[^>]*>.*?<span leaf="">(.*?)</span>',
                      html, re.S)
        args.digest = (m.group(1) if m else args.title)[:120]

    token = get_token(appid, secret)
    print("✅ access_token 获取成功")

    # 正文里的本地图片 → 上传图床并替换
    srcs = re.findall(r'<img[^>]+src="([^"]+)"', html)
    local = [s for s in srcs if not s.startswith(("http://", "https://"))]
    existing = [s for s in local
                if os.path.exists(s if os.path.isabs(s) else os.path.join(ROOT, s))]
    for s in local:
        p = s if os.path.isabs(s) else os.path.join(ROOT, s)
        if not os.path.exists(p):
            print(f"⚠️  图片不存在，跳过: {s}")
            continue
        url = upload_content_image(token, p)
        html = html.replace(f'src="{s}"', f'src="{url}"')
        print(f"🖼 已上传: {os.path.basename(p)} → {url[:60]}...")
    if not local:
        print("ℹ️  正文无本地图片（已有微信图床链接的原样保留）")

    # 封面：--cover 优先 → 否则取正文第一张本地图 → 都没有才回退内置默认图
    if args.cover:
        cover = args.cover
    elif existing:
        cover = existing[0]
        print(f"🖼 封面默认取正文第一张图: {os.path.basename(cover)}")
    else:
        cover = os.path.join("images", "pub", "59_01_不说话只判断.png")
        print("⚠️  正文无本地图片，封面回退到内置默认图")
    cover_path = cover if os.path.isabs(cover) else os.path.join(ROOT, cover)
    thumb = upload_thumb(token, cover_path)
    print(f"🖼 封面已上传: {os.path.basename(cover_path)}")

    article = {
        "title": args.title,
        "author": args.author,
        "digest": args.digest,
        "content": html,
        "content_source_url": "",
        "thumb_media_id": thumb,
        "need_open_comment": 1,
        "only_fans_can_comment": 0,
        "article_type": "news",
    }
    if args.update:
        res2 = post_json(f"{API}/draft/update?access_token={token}",
                         {"media_id": args.update, "index": 0, "articles": article})
        if res2.get("errcode") not in (0, None):
            die("更新草稿失败", res2)
        media_id = args.update
        print("✅ 草稿已更新（覆盖原稿）")
    else:
        media_id = add_draft(token, article)
    print("✅ 草稿已创建")
    print(f"   标题: {args.title}")
    print(f"   摘要: {args.digest}")
    print(f"   草稿 media_id: {media_id}")
    print("   下一步：公众号后台 → 草稿箱 → 打开检查排版 → 群发")


if __name__ == "__main__":
    main()
