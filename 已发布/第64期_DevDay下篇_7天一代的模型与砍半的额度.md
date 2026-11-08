# 7 天迭代一次模型，500 美元一个月，额度还砍半：DevDay 下篇

> 上篇讲它变成了"同事"，这篇讲这笔账：更便宜的模型、更贵的速度、更少的额度。

上篇我们讲了 dots 和 ChatGPT Space —— OpenAI 想把 AI 从"开一个新对话"变成"一份持续的工作关系"。

这一篇讲同场发布的另一半：模型、价格、额度，以及开发者侧的那一堆更新。这部分离你的钱包更近。

![配图01｜封面｜账单](images/第64期/64_01_封面_越来越薄的账单.png)

## 一、GPT-6.1 Sol：7 天就换代 <!-- SOL -->

先说最意外的。

距离 GPT-6 Sol 发布只过了 ==7 天==，OpenAI 就端出了 GPT-6.1 Sol。这也是它历史上模型迭代最快的一次 —— 背景很直接：Claude Opus 5.5 那一周把压力顶满了。

**价格**（每百万 token）：

- 输入 2 美元、输出 10 美元，和上一代持平，==约为 Astra 的五分之一==
- 缓存输入 0.10 美元，==比上一代再降一半==

缓存这一项对智能体很关键：多步工作流会反复读取上下文，命中缓存便宜一半，实际账单会明显变薄。

**能力**，官方的说法是"以五分之一的价格，接近 Astra 的水平"。几个可查的数字：

- 软件工程评测 DeepSWE v1.1：==反超 Astra 一个百分点==，单任务成本 0.65 美元，Astra 要 4.43 美元
- 电脑操作 OSWorld 2.0：比 6 Sol 高 7%，离 Astra 只差 2.1%，==成本约为 Astra 的七分之一==
- 业务流程 AutomationBench（中等推理）：比 Opus 5.5 高 2.2%，成本约其三分之一
- 平均下来，每项任务成本约 5.47 美元，Opus 5.5 是 23.21 美元，Astra 是 23.80 美元

**谁能用**：已向 Plus、Pro、Business、Enterprise 和 Edu 推送，API 同步开放，但==目前只在 ChatGPT Work 和 Codex 里能用==，普通聊天暂时还用不到。

一句提醒：评测分数不等于你手上的体验。==真正该看的是"每件事多少钱"==，这个数字这一轮确实又下了一个台阶。

## 二、UltraFast：快是要加钱的 <!-- FAST -->

GPT-6 Astra 迎来了 UltraFast 模式：API 端约 ==6 倍输出速度==，Codex 里能做到 8 倍速、每秒约 300 个 token。GPT-6.1 Sol 稍后也会支持。

代价是价格：据 The Decoder 报道，UltraFast 的 API 价约为标准价的 6 倍 —— 对应 Astra 就是每百万 token ==输入 60 美元、输出 300 美元==。原来的 Fast 模式大致是"2 倍价格换 2.5 倍速度"。

翻译成人话：==速度是可以买的，而且很贵==。对多数人来说，默认的那一档通常就够了。

## 三、Pro 500 与那场额度争议 <!-- PRO -->

这是发布后争议最大的一条。

**新增 Pro 500**：月费 ==500 美元==，额度是 Plus 的 25 倍，独占 UltraFast 模式。Pro 会员从此分成 100、200、500 三档，每档都包含一只免费的 dot。

**Pro 200 重新开放**了此前暂停近三周的订阅，但随之而来的是坏消息：

- Pro 100 额度：Plus 的 ==5 倍==
- Pro 200 额度：从 20 倍降到 ==10 倍==
- 存量用户的双倍额度，==10 月 29 日失效==
- 唯一的补偿：取消了 5 小时使用限制

社区里的反对声不小，最形象的说法是：=="这就像运营商说 5G 更快了，所以我把你的流量砍一半"==。官方的解释是模型会继续降价，额度虽然少了，能干的活反而更多 —— 逻辑上说得通，观感上很难服众。

更可能的真实原因是方向变了：OpenAI 在往企业服务倾斜，过去那种"量大从优"地补贴个人订阅，自然难以为继。

![配图02｜额度](images/第64期/64_02_额度_砍半.png)

## 四、Decisions API：让模型只做选择题 <!-- DECISION -->

这是全场看起来最小、但我个人最感兴趣的一条。

做法很简单：开发者先预设几个选项，把材料丢进去，Decisions API 用定制版的 GPT-6 Luna ==快速做分类、路由，或者决定智能体的下一步==，而不是生成一大段文字。

效果：官方案例里 ==150 毫秒==出结果，而通过 API 调标准 GPT-6 Luna 要 1.6 秒，快约 10 倍。Luna 原本的图像理解、多语言和安全能力都还在。

为什么值得单独说？两周前的 9 月 16 日，一家叫 TypeSafeAI 的公司发布了专用判断模型 Jev，核心主张就是"很多自动化根本不需要模型写答案，只需要它快速做决定"。我们当时也聊过。结果两周后，OpenAI 在讲模型的时候顺手掏了几分钟，把同样的能力加给了 Luna。

这就是小公司的处境：==你教育完市场，大厂随手就补上了==。反过来说，也说明"让便宜的模型做判断、让贵的模型做推理"这个思路，已经被验证是对的。

## 五、开发者侧：Codex 全面上云 <!-- CODEX -->

**Codex Cloud** 这次补上了最关键的一层 —— ==可复用开发环境==。你可以提前把代码仓库、依赖、工具、环境变量配好，之后的任务直接基于这套环境启动，不用每次重装。每个任务仍有独立 workspace，任务状态最长可恢复 7 天。云端 Codex 现在也能用插件和 Computer Use。

顺带一句：山姆·奥特曼开场还揶揄了"用 Codex 不敢合上笔记本盖子"这件事 —— 从此可以了。

**Codex Security Cloud**：从"帮我审一下这个仓库"变成常驻安全智能体，支持自动去重、定时扫描和新的管理界面。这个能力今年 3 月就预览上线并开源，==已扫过 3000 多万个 commit、3 万多个代码库==。

其余还有：Agents API 把 Computer Use 也装了进去；Codex CLI 开放了双向语音对话。

## 六、生态三件事 <!-- ECO -->

**① 带着你的订阅去第三方。** 以后用 ChatGPT 账号登录 Notion、GitLab、HubSpot、Vercel 这类应用，可以直接消耗你 ChatGPT 套餐里的额度。对开发者是大利好：API 成本不用自己掏了。

**② 插件越来越像 App。** 开发者可以把编辑器、Dashboard、表单、整个工作区直接嵌进 ChatGPT 和 Codex（现场演示了 Figma 和 Adobe），插件还能在对话里被自动发现。审核流程也更像正规开发平台了。苹果那套 App Store 的野心，一直都在。

**③ OpenAI Marketplace（Beta）**。首发 30 多家合作伙伴，玩法是：企业把已经承诺给 OpenAI 的采购额度，拿一部分去买合作伙伴的软件。本质上是把自己当企业分发平台。这个模式 Claude 先发了，OpenAI 跟进。

![配图03｜生态](images/第64期/64_03_生态_一个账号牵着所有应用.png)

## 七、怎么看这场会 <!-- VIEW -->

发布会的最后有个彩蛋：奥特曼说大家又要疯狂烧 Codex 额度了，于是送了一张"重置卡"。

但整场看下来，更值得记的是一句话：

> OpenAI 正在把 ChatGPT 做成一种 SaaS 服务。

它有 ==12 亿周活==，消费者心智几乎无人能敌；但据路透社披露，Anthropic 那边 30 多万家企业和商业客户贡献了约 80% 的收入 —— ==真正稳定、高价值的收入在企业侧==。所以你会看到 dots 有 Specialist 版本、Space 有团队任务、Marketplace 面向企业采购。

还有一个判断我认同：==没有任何一个模型能在能力上领先竞品超过半年==。既然如此，护城河就不在模型本身，而在项目、智能体、权限体系和工作流这些"难以迁移"的东西上。

这跟我们这两年讲的一条线是一致的：能力会越来越便宜，==真正稀缺的是"你敢把什么交给它"==。

## 最后

DevDay 这两篇就到这里。

接下来假期里还有几篇：AI 自己跑出去了（越界事件全貌与应对）、给 AI 画围栏（Docker 那份开放标准）、以及 10 月 5 日那篇我特别想写的 —— ==dots、豆包、CodeBuddy/WorkBuddy 这几类"AI 同事"到底有什么不一样，放在我们讲过的"七层"里看，各自是在哪一层发力==。

明天见。

---

*本文事实依据：OpenAI DevDay 2026 发布会实录与 OpenAI 官方定价/文档，多家媒体现场报道（爱范儿、量子位、数字生命卡兹克、The Decoder 等）交叉比对。价格、额度与开通范围可能调整，以 OpenAI 官方最新公告为准，核查时间：2026 年 9 月 30 日。*

## 配图方案与提示词（内部参考，不进正文） <!-- IMGSPEC -->

### 0. 图位与采用方案

| 图位 | 正文位置 | 这一张要讲清的一件事 | 最终采用 |
|---|---|---|---|
| 配图01 封面 | 导语之后 | 这篇讲的是「一笔账」：更便宜的模型、更贵的速度、更少的额度 | 本地浏览器生图（Chrome 登录态 → 豆包），已去平台角标 |
| 配图02 额度 | 第三章末（Pro 500 争议之后） | 额度砍半：速度在涨、容量在降 | 同上 |
| 配图03 生态 | 第六章末（生态三件事之后） | 一个账号牵着所有应用：订阅可以带出去花 | 同上 |

- 三张均为竖版 `1080×1440`（3:4），存于 `images/第64期/`
- 生成方式：`_gen64.py`（复用 `NationDay/scripts/generate_browser.py` 的浏览器引擎，Chrome 登录态副本；出图后经 `watermark.py` 清角标）
- 提示词结构：**主体段 + 风格段 + 负面段** 拼接即用；风格段与负面段三张共用，只换主体段

---

### 1. 统一视觉（全系列共用，逐张不重复）

**画布与构图**
- 竖版 3:4，1080×1440；安全边距 96px，主体不越界
- 主体占画面 45%–60%，**留白 ≥35%**（宁可空，不可挤）
- 三层结构，必须能分辨层次：① 背景几何 → ② 白色卡片 → ③ 焦点元素
- 三分法定位主体，避开正中心铁律；一幅只讲一件事

**色彩（取自排版 CSS，不得自行增色）**
- 纸底 `#FAF8F5`｜卡片 `#FFFFFF`｜浅红底 `#FEF2F2`｜浅红描边 `#FEE2E2`
- 焦点红 `#DC2626` —— **全图只允许出现一处**；墨线 `#1C1917`；分隔灰 `#E5E7EB`
- 禁止第三种彩色，禁止彩虹渐变

**材质与光**
- 哑光、扁平、无立体感；不要高光、不要金属、不要玻璃拟态
- 卡片投影只用 `rgba(220,38,38,0.15)`，偏移 y=8、模糊 24
- 允许极轻的红色柔晕仅出现在焦点元素周围，不透明度 ≤15%

**几何语言**
- 圆角矩形卡片 12–20px 圆角｜细实线 1–2px｜虚线只用于表达「空缺／待填」，不做装饰

**风格段（英文，逐张复用）：**
> Flat editorial vector illustration, vertical 3:4 canvas 1080x1440, warm off-white paper background #FAF8F5, matte flat finish, thin ink line work #1C1917, soft panel fill #FEF2F2 with 1px #FEE2E2 outline, rounded-corner card geometry with 12-20px radius, subtle red-tinted card shadow rgba(220,38,38,0.15), exactly one vermilion accent #DC2626, three distinguishable layers (background geometry, white card, focal element), generous negative space over 35 percent, quiet geometric composition.

**负面段（每一张都要带）：**
> no text, no letters, no numbers, no watermark, no logo, no real human faces, no photorealism, no 3D render, no gradient glare, no rainbow palette, no visual clutter, no bevel, no metallic, no glassmorphism.

---

### 2. 配图01｜封面｜越来越薄的账单

**承载的正文信息**：「这篇讲这笔账：更便宜的模型、更贵的速度、更少的额度」／「这部分离你的钱包更近」

**画面构成（三层）**
- 主体层（55%）：中央一张竖立的长账单卡（白色圆角卡），卡内自上而下五条横条，**长度依次递减** —— 账单在变薄
- 焦点层（唯一红）：最下面那条最短的横条用正红，其余横条为浅红灰
- 背景层：左上一条细灰向下折线（价格在往下走）；右下角一枚灰色硬币轮廓
- 留白 ≥35%，卡片不顶满画布

**主体段（拼在风格段之前）：**
> A tall white receipt card standing in the center with five stacked horizontal bars whose lengths decrease from top to bottom, the shortest bottom bar being the only vermilion element; a thin grey downward trend polyline at the upper left; one grey coin outline at the lower right; generous empty paper space around the card.

**易错点**：不要画成「金币堆在变少」（俗套）；账单上不许出现任何文字、数字、货币符号；横条只用**长度**差异表达递减，颜色差异只允许出现在最后一条；向下折线要细、要灰，不能抢焦点。

---

### 3. 配图02｜额度｜砍半

**承载的正文信息**：「Pro 200 额度：从 20 倍降到 10 倍」／「这就像运营商说 5G 更快了，所以我把你的流量砍一半」

**画面构成（三层）**
- 主体层（55%）：中央一个竖立的容器卡（白色圆角卡）—— **下半部填充，上半部留空**
- 焦点层（唯一红）：容器下半部的填充块为正红（剩下的那一半）
- 对照层：上半部用灰色虚线勾出空轮廓；中线处一道淡横切线（被切掉的那一刀）
- 背景层：右侧一条细灰向上箭头（速度在涨，与容量下降形成反差）
- 留白 ≥35%

**主体段（拼在风格段之前）：**
> A tall white vertical container card in the center, its lower half filled with a single vermilion block while the upper half stays an empty dashed grey outline; a thin grey upward speed arrow on the right side; a faint horizontal cut line across the container midpoint; generous empty paper space.

**易错点**：不要画成「电池」（会读成电量）；不要画成「半杯水」（过于具象）；红色填充**只能有一块**，别把上半部也描红；向上箭头要细、要灰，不能变成第二焦点。

---

### 4. 配图03｜生态｜一个账号牵着所有应用

**承载的正文信息**：「用 ChatGPT 账号登录 Notion、GitLab、HubSpot、Vercel 这类应用，可以直接消耗你 ChatGPT 套餐里的额度」／「插件越来越像 App」／「OpenAI Marketplace」

**画面构成（三层）**
- 主体层（50%）：中央一张白色圆角方卡（代表账号/订阅），卡面中心一枚墨黑圆点
- 辐射层：六枚较小的灰色圆角形均匀环绕，每一枚由一条细直线连回中心卡
- 焦点层（唯一红）：其中一枚小卡用正红，其余为灰
- 留白 ≥35%，连接线要细，不能织成网

**主体段（拼在风格段之前）：**
> A white rounded square card in the center with one ink-black dot at its middle; six smaller grey rounded shapes arranged around it at even angles, each joined to the center card by a thin straight line; exactly one of the smaller shapes rendered in vermilion; generous empty paper space.

**易错点**：不要画成「蜘蛛网／齿轮」（线多必翻车，六条封顶）；小卡不许带任何可辨识的品牌形状或图标；中心卡不要画成钱包、信用卡这类具象物。

---

### 5. 生成后自检（不通过就重生成，别将就）

1. 红色是否**只有一处**？两处红 → 焦点散了，重生成
2. 画面里有没有任何文字、字母、数字、水印、logo？（有 → 重生成）
3. 留白是否 ≥35%？（挤 → 重生成）
4. 尺寸是否 1080×1440，主体是否都在 96px 安全边距内？
5. 退后三步看：不读文字，能不能说出这张图在讲什么？说不出 → 主体不够明确

**生成参数**：比例 3:4、目标 1080×1440、一次出 4 张挑 1；重生成时只改「主体段」，风格段与负面段保持不变 —— 这样三张图的调子才统一。平台角标出图后自动清除（`watermark.py`）。

---

### 6. 说明

- 本区块由「旧的 Q 版卡通提示词」整体重写：旧版三个毛病是**画面与正文脱钩、每张只有一句话、还逐张复制长后缀**
- 新版每张先写「承载的正文信息」（引正文原句），再给「三层构图 + 占比 + 焦点位置 + 易错点」，可直接照着画
- 实际出图走本地浏览器（Chrome 登录态 → 豆包），未使用 API 生成
