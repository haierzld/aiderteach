# aiderteach

aiderteach 公众号（AI 资讯）的文章与配图公开归档。每期通常包含 Markdown 正文、可直接粘贴进公众号编辑器的排版 HTML，以及 `images/第N期/` 下的配图。

## 目录

- 根目录：`第140期` 起的最新文章，以及两份选题规划
- `已发布/`：1–139 期历史文章（md + 排版 html + 预览 html）
- `images/第N期/`：各期配图
- `scripts/`：排版校验、草稿发布等工具
- `docs/`：选题规划

## 本地使用

1. 把 `config/config.example.ini` 复制为 `config/config.ini`，填入自己的公众号 `AppID` / `AppSecret`，并在公众号后台把本机出口 IP 加入白名单。
2. 发布草稿：

```bash
python scripts/publish_draft.py --html "<排版HTML>" --title "<标题>" --digest "<摘要>"
```

`config/config.ini` 已被 `.gitignore` 排除，不会入库。

## 说明

- 文章为原创内容，转载请注明出处；文中引用的新闻配图版权归原作者与机构，仅作报道配图使用。
- 排版 HTML 中的图片使用仓库内相对路径，本地预览时请保持目录结构。
