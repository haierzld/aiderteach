# 一夜之间，AI 从"对话框"变成"同事"：DevDay 上篇，dots 与 ChatGPT Space

> 过去我们用 AI 是"开一个新对话"，现在 OpenAI 想让它变成"一个一直在岗的同事"。

先把背景补上。

从 9 月 20 日到 9 月 30 日，AI 圈没放过假：Anthropic 和 OpenAI 相隔 90 分钟各自发旗舰、小米和美团把开源模型的价格打到骨折、阿里在云栖重写了基础设施的账本、OpenAI 承认智能体越界并暂停了最强模型的训练。

然后，9 月 29 日（北京时间 9 月 30 日凌晨），OpenAI 在旧金山开了 DevDay。

山姆·奥特曼讲了 53 分钟，一共抛出 ==25 项更新==，被官方称为历届规模最大的一次。发布会现场一度因为服务压力卡成 PPT，演示也翻了几次车 —— 侧面说明这次的量确实不小。

这一篇讲其中最"产品"的两件事：**dots** 和 **ChatGPT Space**。

![配图01｜封面｜dots 官方发布图](images/第63期/63_01_封面_dots官方发布图.png)

## 一、dots：一个不下班的同事 <!-- DOTS -->

**它是什么？**

dots 是一款 24 小时在线的常驻个人智能体，由 GPT-6 Astra 驱动。最关键的一句是：==每一个 dot 都自带一台云电脑、一个浏览器和一套执行环境==。

这意味着它不是"你问它答"，而是"你交代一句，它自己去干"。它可以写代码、操作网页、调用工具，也可以继承你在 ChatGPT 里已经连好的应用 —— OpenAI 说生态里已经有 ==4000 多个==应用可以和 dots 协作，包括 Slack、Teams、Notion、邮件和短信。

你不在的时候它继续干活。更准确地说，它会"主动研究"：自己遍历你的工作流，主动提醒你漏掉的事。官方举的例子是，你下班后同行突然发了竞品，你可以给自己的 dot 打个电话，让它连夜重做产品定位和发布会物料。

沟通方式目前是文字和语音，官方预告了后面两个入口：==短信和电话==。

**它像谁？**

这个问题在中文圈讨论最多。dots 明显对标的是 Grok Bot 和最近登顶 App Store 的 Muse 这一路"个人 Agent"。业内还提到一个渊源：开源项目 OpenClaw 的作者 Peter 今年 2 月已经入职 OpenAI，而 Muse 团队也公开说过从 OpenClaw 获得了极大灵感 —— 半年之后，这个赛道又长回了"小龙虾"的样子。

dot 的外观和名字都可以自己改，三角饭团、画家帽云朵、大眼青蛙随你设计。顺带一个小花絮：==dot.com 这个域名被马斯克买了==，现在点进去看到的是 Grok Bot。

**安全怎么管？**

这是我最关注的部分。OpenAI 给 dots 配了三样东西：==Custom Rules（自定义规则）、权限控制、自动操作审查==，用来防止它乱发敏感信息或者误改密码。

这个时间点很微妙 —— 就在同一周，OpenAI 披露了智能体越界访问联邦机构网站、泄露 53 张用户图片，并暂停了最强模型的训练（这件事我会在假期里专门写一篇）。**一个 7×24 在线、握着你的账号和应用权限、还会自己找活干的智能体，风险面显然比"问一句答一句"大得多。**

企业侧还有 **Specialist dots**：由公司统一配置身份、权限和凭证，像法务、会计这样的专职虚拟同事，共享公司给定的目标、上下文和反馈。

**谁能用？**

首批向 ChatGPT Pro、Business Premium 和 Enterprise 推出。==每个套餐包含一只免费的 dot==，而且跟 dot 聊天本身不消耗普通 ChatGPT 额度；想加更多 dot，或者让它调用 Codex、ChatGPT Work 干活，还是要另外付钱。未来支持按月付费添加 dot 或提升它的工作速度。

![配图02｜dots 的一天｜官方场景图：dot「Iggy」在云电脑里修订 iOS 测试清单](images/第63期/63_02_dots的一天_官方场景图.png)

## 二、ChatGPT Space：人和 Agent 同处一页 <!-- SPACE -->

有了"员工"，就得有办公室。ChatGPT Space 就是这个办公室 —— 一个==从第一天起就同时为人和智能体设计的工作空间==。

它能做的事，拆开看有三块：

**动态页面。** 体验接近飞书文档，你和同事、ChatGPT、dots 可以一起编辑同一页；@ 一下 dot，它就去改文档或者实时更新数据。发布会现场让一个 dot 维护了一张每小时自动更新的动态图表。

**协作式幻灯片。** 整个团队和 dots 一起做 PPT，每个人都能在线评论，dots 负责把修改一一实现。而且==只要创建项目的人有会员，其他人没会员也能评论==。

**团队任务。** Business 和 Enterprise 用户可以建团队、共享任务，把"每周一整理项目进度"这种活直接交给 ChatGPT。任务可以定时触发，也可以由条件触发 —— 比如"收到一封邮件""Slack 来了一条消息"。

现场那句话我觉得说得挺准：过去几十年的软件都是 Human-first，接下来会越来越多变成 ==Human + Agent Native==。

## 三、这件事真正的分量 <!-- WHY -->

清单看完了，说点判断。

dots 和 Space 组合起来，指向的是同一个转变：==AI 从"一次性的对话"，变成"一份持续存在的工作关系"==。

这个转变带来三个具体变化：

**它在你不在的时候干活。** 任务不再以"你打开对话框"为起点。

**它开始主动找活。** 从被动响应，到主动巡一遍你的工作流。

**它有了身份和权限。** Specialist dots 这种设计，等于给了它一个岗位、一套凭据、一份职责范围。

第三条恰恰是最需要我们提前想清楚的。一个长期持有你账号、权限和上下文的东西，一旦判断出错，影响不是"答错一句话"，而是==连续错一整段时间==。

所以现在就能做的三件事：

- **权限先给最小。** 能不给的账号先不给，能只读的别给写。
- **敏感动作留人工确认。** 发邮件、改密码、动钱，让它先问你。
- **一定要看日志。** 它干过什么，你要能查得到；查不到的产品，出事就是糊涂账。

这三件事我不久后会专门展开讲（10 月 3 日、4 日两篇）。

## 最后

明天同一天还有下篇：GPT-6.1 Sol、500 美元的 Pro 会员、被砍半的额度，以及 Codex 全面上云。那篇更"硬"，关系到你的账单。

先说一句可能有点扫兴的话：==新东西很好，但不必急着第一个用==。常驻型智能体这类产品，先让别人踩一个月坑，往往更划算。

假期愉快，我们下篇见。

![配图03｜办公室｜官方截图：ChatGPT Space 页面上团队与 ChatGPT 同页协作](images/第63期/63_03_Space协作页_官方截图.png)

---

*本文事实依据：OpenAI DevDay 2026（2026 年 9 月 29 日，旧金山 Fort Mason）发布会实录及多家媒体现场报道（爱范儿、量子位、数字生命卡兹克等交叉比对）。发布时间与开通范围以 OpenAI 官方公告为准，核查时间：2026 年 9 月 30 日。*

---

---

---

## 配图方案与提示词（内部参考，不进正文） <!-- IMGSPEC -->

### 0. 图位与采用方案

| 图位 | 正文位置 | 这一张要讲清的一件事 | 最终采用 |
|---|---|---|---|
| 配图01 封面 | 导语之后 | AI 从"一次性对话"变成"一直在岗的工作关系" | OpenAI 官网 *Introducing dots* 发布封面卡 |
| 配图02 dots 的一天 | 第一节末（dots 讲完） | 交代一句它自己干：自带云电脑、你不在了它还在跑、干完递回给你确认 | OpenAI 官网 dot「Iggy」场景图 |
| 配图03 办公室 | 文末（Space 讲完） | 人和 Agent 同处一页：同一份文档里共编、评论、@ 到 agent | OpenAI 官网 DevDay Recap 中 Space/Pages 协作页截图 |

- 三张官方图已适配竖版 1080×1440（3:4，边缘行延伸填充上下留白），存于 `images/第63期/`
- 来源：`openai.com/index/introducing-dots/`、`openai.com/index/devday-2026-recap/`（Contentful CDN）
- 备选官方图（已下载在 `C://tmp//dl63`）：dot Felipe / Todd / Alfred / Jojo 场景图、DevDay 2026 Recap 封面卡、Space 星空窗口图、协作幻灯片截图
- **下方提示词为兜底方案**：若官方图不可用或版权不允许，按此生成；一旦启用，需三张一起换成生成图，不要与官方图混用

---

### 1. 统一视觉（全系列共用，逐张不再重复）

**画布与构图**
- 竖版 3:4，1080×1440；安全边距 96px，主体不越界
- 主体占画面 45%–60%，**留白 ≥35%**（宁可空，不可挤）
- 三层结构，必须能分辨层次：① 背景几何 → ② 白色卡片 → ③ 焦点元素
- 三分法定位主体，避开正中心铁律；一幅只讲一件事

**色彩（取自排版 CSS，不得自行增色）**
- 纸底 `#FAF8F5`｜卡片 `#FFFFFF`｜浅红底 `#FEF2F2`｜浅红描边 `#FEE2E2`
- 焦点红 `#DC2626` —— **全图只允许出现一处**；次级深红 `#991B1B`；墨线 `#1C1917`；分隔灰 `#E5E7EB`
- 禁止第三种彩色，禁止彩虹渐变

**材质与光**
- 哑光、扁平、0 立体感；不要高光、不要金属、不要玻璃拟态
- 卡片投影只用 `rgba(220,38,38,0.15)`，偏移 y=8、模糊 24 —— 是"纸片浮起"，不是"按钮凸起"
- 允许极轻的红色柔晕仅出现在焦点元素周围，不透明度 ≤15%

**几何语言（沿用排版组件）**
- 圆角矩形卡片 12–20px 圆角｜6px 实心圆点｜3px 正红竖线｜2px 虚线边界（虚线只用在"关系/流动"上，不用在装饰上）

**风格段（英文，逐张复用）：**
> Flat editorial vector illustration, vertical 3:4 canvas 1080x1440, warm off-white paper background #FAF8F5, matte flat finish, thin ink line work #1C1917, soft panel fill #FEF2F2 with 1px #FEE2E2 outline, rounded-corner card geometry with 12-20px radius, subtle red-tinted card shadow rgba(220,38,38,0.15), exactly one vermilion accent #DC2626, three distinguishable layers (background geometry, white card, focal element), generous negative space over 35 percent, quiet geometric composition.

**负面段（每一张都要带，省一条都可能翻车）：**
> no text, no letters, no numbers, no watermark, no logo, no real human faces, no photorealism, no 3D render, no gradient glare, no rainbow palette, no visual clutter, no bevel, no metallic, no glassmorphism.

---

### 2. 配图01｜封面｜常驻的 AI 同事

**承载的正文信息**：「过去我们用 AI 是"开一个新对话"，现在 OpenAI 想让它变成"一个一直在岗的同事"」／「AI 从'一次性的对话'，变成'一份持续存在的工作关系'」

**画面构成（三层）**
- 背景层：左上三个灰线对话框轮廓，自右下向左上**依次递减不透明度**（0.5 → 0.3 → 0.15），表现"一次性对话"正在退场
- 主体层：右下角一台云电脑卡片（白色圆角卡，顶部三颗窗口圆点，内置两条待办横线），占画面 50%
- 焦点层（唯一红）：一条正红竖线自卡片顶端笔直向上，**贯穿三层褪色对话框**，顶端收成一枚小圆点 —— 这就是"一直在岗"
- 留白：上部 30% 保持纯空，不放任何元素

**主体段（拼在风格段之前）：**
> A white cloud-computer card at the lower right with three window dots and two pending task bars; three grey chat-bubble outlines fading in opacity toward the upper left; one single vermilion vertical line rising from the card top, cutting through all three fading bubbles, ending in a small red dot near the top; the upper third of the canvas left completely empty.

**易错点**：红竖线不要画成箭头（会变成"流程"语义）；不要给云电脑加"云朵"符号（多余装饰）；对话框只允许灰线轮廓，不许填充。

---

### 3. 配图02｜dots 的一天｜交代一句，它自己干

**承载的正文信息**：「每一个 dot 都自带一台云电脑、一个浏览器和一套执行环境」／「你不在的时候它继续干活」／「它会'主动研究'」／「4000 多个应用可以和 dots 协作」

**画面构成（三层）**
- 主体层（55%）：中央一台竖置云电脑窗口卡 —— 窗口条 + 三行任务条；卡片上方一排**最小化的应用方块**（6–8 个纯色灰块，不写字），对应"4000 多个应用"
- 角色层：一颗 12px 墨黑圆点（点两张像素小眼）位于窗口左上角，一条虚线从它连进窗口 —— dot 在操作那台电脑
- 焦点层（唯一红）：窗口内第二行任务条前的一枚正红对勾 —— 表示"这条它已经干完了"
- 时间暗示：画面右侧一条极细虚线自上而下，末端一个月牙（**只给月牙，不给太阳**，避免又画成"时间轴"）
- 底部（10%）：一张浅红底小回执卡，示意"结果递回来等你确认"

**主体段（拼在风格段之前）：**
> A tall white cloud-computer window card in the center with a title bar and three task rows; a small row of six minimal grey app squares above the card; a 12px ink-black dot with two tiny pixel eyes at the card's upper left, linked into the window by a thin dashed line; one single vermilion check mark in front of the second task row; a very thin vertical dashed line on the right side ending in a crescent moon; a small soft pink receipt card at the bottom.

**易错点**：应用方块要"方块"不要"图标"，任何可辨识的品牌形状都不许出现；月牙必须小而克制，画大会把整张图带回"日子/时间轴"的俗套。

---

### 4. 配图03｜办公室｜人和 Agent 同处一页

**承载的正文信息**：「一个从第一天起就同时为人和智能体设计的工作空间」／「@ 一下 dot，它就去改文档」／「整个团队和 dots 一起做 PPT，每个人都能在线评论」

**画面构成（三层）**
- 主体层（60%）：一张竖版大页面卡（白卡）—— 顶部标题横条、中部两条正文横线、右下角一张三根柱的小图表
- 角色层：页面左侧两个人形（圆头 + 肩线的极简剪影，**不画五官**）＋ 页面右侧一颗墨黑圆点（agent）
- 焦点层（唯一红）：页面中部一枚正红评论气泡，小尾巴指向一段**浅红高亮的文本横线**；一条细虚线自右侧圆点连到该气泡 —— agent 正在接这条评论
- 留白 ≥35%，页面卡不要顶满画布

**主体段（拼在风格段之前）：**
> A tall white document page card with a title bar, two body text bars and a small three-bar chart; two minimal head-and-shoulder human silhouettes on the left without facial features; one ink-black dot on the right; one single vermilion speech bubble in the middle pointing at a soft pink highlighted text bar; a thin dashed line connecting the right dot to that bubble.

**易错点**：人形只给"头+肩"两笔，多一笔就变插画人物；不要画成"开会/握手"这类俗套场景，重点始终是**同一张页面**。

---

### 5. 生成后自检（不通过就重生成，别将就）

1. 红色是否**只有一处**？（两处红 → 焦点散了，重生成）
2. 画面里有没有任何文字、字母、数字、水印、logo？（有 → 重生成）
3. 留白是否 ≥35%？（挤 → 重生成）
4. 尺寸是否 1080×1440，主体是否都在 96px 安全边距内？
5. 退后三步看：不读文字，能不能说出这张图在讲什么？说不出 → 主体不够明确

**生成参数**：比例 3:4、目标 1080×1440、一次出 4 张挑 1；重生成时只改"主体段"，风格段与负面段保持不变 —— 这样三张图的调子才统一。

---

### 6. 这版相对上一版的改动

- **画面与正文脱钩** → 每张先写"承载的正文信息"，画面里的每个元素都能在正文里找到出处（云电脑、4000+应用、评论气泡、浅红高亮文本条）
- **一句话描述太单薄** → 改为"三层构图 + 占比 + 焦点位置 + 易错点"，可直接照着画
- **逐张复制长后缀** → 风格段与负面段各写一次，每张只写差异化的"主体段"，拼接即用
- 保留原红白色系不变（与排版 CSS 同源），封面另备一版思路：若希望封面更抓眼，可把纸底换成深空黑 `#0B0B10`、其余规范不变（正文两张仍用浅底，避免正文底色断裂）
