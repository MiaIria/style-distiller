# Style Distiller

> **不是替你写，是学你怎么写。**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)]()
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

---

## 🎯 这是什么

你可能遇到过这些问题：

- 网上刷到一篇感触很深的文章，第一反应是“我也想写这样文章” → 奈何文笔不够
- 想着让 AI 写吧 → 写出来一股 AI 味
- 让 AI "仿照我的风格去写" → 结果它根本不懂你

**Style Distiller 不替你写，它学你怎么写。**

它维护一份"你的文字人格档案"，每次你：

| 你想干什么 | 用哪个 |
|---|---|
| "我喜欢这篇" / 喂入喜欢的文章 | `/style-feed` |
| 给写出来的草稿打分 | `/style-feedback` |
| 喂入你讨厌的文章 | `/style-reject` |
| 看看自己风格档案什么样 | `/style-review` |
| 用你的风格写一篇 | `/style-write` |
| **不确定该用哪个？说一句话即可** | **`/style-distiller`** ⭐ v2 聚合入口 |

> ⭐ **v2 新增**：`/style-distiller` 是聚合入口——你只需说"帮我训练风格"或"看看我档案"，它会自动识别意图并分发到对应子 skill。

---

## 📦 安装（2 分钟）

### 前提条件

- Python 3.10+（仅 `profile_stats.py` 等脚本需要，Claude Code 用户不必装）
- Claude Code（任意版本）
- 三平台都支持：Windows / macOS / Linux

### 方式 A：Git Clone（推荐）

```bash
git clone https://github.com/MiaIria/style-distiller.git
# Linux/macOS 软链：
ln -s "$(pwd)/style-distiller" ~/.claude/skills/style-distiller
# Windows PowerShell 软链：
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\style-distiller" -Target "$(Get-Location)\style-distiller"
```

### 方式 B：手动下载

从 GitHub 仓库下载 ZIP → 解压到 `~/.claude/skills/style-distiller/`。

### 数据目录

工具不需要预创建任何数据目录——首次触发 `/style-feed` 时会自动初始化：

```
~/.claude/styles/                   ← 用户档案数据（隐私本地化）
├── weights.json                    ← 档案权重与状态
├── profile/                        ← 8 份风格画像
├── samples/positive/                ← 投喂样本（/style-feed）
├── samples/negative/                ← 反样本（/style-reject）
├── drafts/                          ← ⚠️ 旧路径已废弃，新规范见下方"v2 新增使用建议"
└── backups/                         ← 自动备份
```

> ⭐ **v2 新增使用建议**：创建以下文件夹用于作品管理和 skill 自进化
>
> - **`style-write/results/初版/`** — 用于存放写出来的初始版本
> - **`style-write/results/终版/`** — 用于存放你修改后的最终版本
> - **`style-write/difference/`** — 用于存放每次初版 vs 终版的区别，作为你的个人细节偏好
>
> **📌 自动检测**：当 `/results/` 中出现与初版相同标题的"终版"文件时，skill 会检测并主动询问用户是否需要比较差异

### 验证安装

```bash
cd ~/.claude/skills/style-distiller
python scripts/profile_stats.py
```

预期输出类似：

```
profile_dir=~/.claude/styles
state=cold_start
state_basis=inferred
state_inferred=cold_start
positive_samples=0
self_written_samples=0
total_samples=0
```

---

## 📚 6 个核心指令

| 指令 | 你什么时候用 | 关键产出 |
|---|---|---|
| **`/style-distiller`** ⭐ | **不确定用哪个？说一句话** | **自动识别意图 + 分发到子 skill** |
| `/style-feed` | 刷到喜欢的好文章 | 样本 ID + 8 份 profile 差分更新 |
| `/style-feedback` | 给草稿打分 / 纠错档案 | history.md 记录 + 权重校准 |
| `/style-reject` | 看到油腻/套路化写法想避雷 | 反样本 + 禁忌区 |
| `/style-review` | 好奇自己的风格长什么样 | 完整档案审视报告（含导出/回滚）|
| `/style-write` | "用我的风格写一篇" | `results/初版/*.md`（含风格匹配度报告）|

### 协同流程：怎么把风格练出来

```
1. /style-feed          喂 3-5 篇你喜欢的好文章  或在/results中添加你写过的并且比较满意的文章       ← 必选，先建库
2. /style-feedback      对 AI 草稿打分（加速收敛）     ← 可选
3. /style-reject        标几个反例（如"小红书体"）    ← 可选
4. /style-review        看看档案成熟度                ← 建议样本 ≥10
5. /style-write         用你的风格写一篇              ← 终极目标
```

> ⭐ **v2 更新**：`/style-write` 现在包含 **深度对话挖掘**（最多问你 8 个问题确认写作意图）+ **风格匹配度报告**（生成后告诉你 7 维命中度、自动验证是否真用上你的档案）。

---

## 🔁 自主进化闭环（v2 全新）

**核心承诺：同一个毛病不犯第二次。**

Style Distiller 不只"读你喜欢的"，还"看你改的"：

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│  AI 写第一稿     │  ──────>│  你定稿（终版）   │  ──────>│  逐字对比差异    │
│ results/初版/    │  你改   │  results/终版/   │  /对比  │  difference/    │
└─────────────────┘         └─────────────────┘         └─────────────────┘
                                                                 │
                                                                 ▼
                                              ┌─────────────────────────────┐
                                              │ 下次 /style-write 自动加载    │
                                              │ 这些偏好作为"作者硬约束" 🚨   │
                                              └─────────────────────────────┘
```

### 真实例子（来自 v2 实战）

`style-write/difference/result-0819_差异对比.md` 从一次对话体草稿（2200 字）提炼出 **8 条作者偏好**：

| # | 偏好 | 升级为 |
|---|---|---|
| 1 | 口语化优先 | 🟢 软约束 |
| 2 | 陈述代替反问 | 🟡 强约束 |
| 3 | 诚实优先于确定 | 🟡 强约束 |
| 4 | 不要卖惨 | 🚨 硬约束 |
| 5 | 因果要完整 | 🟡 强约束 |
| 6 | 措辞要统一 | 🟢 软约束 |
| 7 | 短句再短一点 | 🟡 强约束 |
| 8 | 副词一层意思 | 🟢 软约束 |

下次你 `/style-write` 时，🚨 硬约束会被自动注入 prompt，永远不再写"卖惨"句式。

---

## 🧠 工作原理

### 一句话

**Style Distiller 把"风格"当作一个可观察、可存储、可检索、可验证、可纠错的"学习系统"问题，而不是 prompt 模板问题。**

### 核心创新：动作级提取（Action-level Extraction）

你说"文笔细腻"——这是模糊的。AI 不知道该做什么。

Style Distiller 把它**翻译成 AI 可直接执行的具体动作**：

| 你的描述 | 翻译后的可执行动作 |
|---|---|
| 文笔细腻 | 80% 句子在 25 字以内；偏好用名词作结 |
| 开头抓人 | 67% 用对话开场，33% 用场景锚定 |
| 有深度 | 每 300 字必有 1 处认知反差（先陈述常识再反转） |
| 不要套路 | 检测到"作为一个..."、"在这个...的时代"等开头直接重写 |
| 收尾克制 | 禁用"总之"、"愿你"、"共勉"；偏好开放问题或留白 |

> 💡 **为什么必须这样？** 形容词没法被验证，没法被检索，没法被纠错。**动作可以。**

### 4 大机制

```
┌─────────────────────────────────────────────────────┐
│              Style Distiller 工作循环                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  📥 摄入层        🧠 处理层        📤 输出层        │
│  ─────────       ─────────       ─────────         │
│  /style-feed  →  动作级提取   →  /style-write     │
│  /style-reject →  8 份 profile →  /style-review    │
│  /style-feedback → + 检索增强   →  /style-feed     │
│                                                     │
│            ↑                          │              │
│            │                          ▼              │
│        反馈权重 ←─────────────── 强制验证            │
│                                                     │
└─────────────────────────────────────────────────────┘
```

| 机制 | 解决什么 |
|---|---|
| **上下文工程** | 把"细腻"翻译成 25 字以内的硬规则 |
| **检索增强** | 50 个样本里挑 3-5 个最相关的，不是全加载 |
| **规则蒸馏** | 模糊偏好 → 🚨🟡🟢 三层硬约束 prompt |
| **反馈循环** | 你的每次打分都让档案更准 |

---

## 🛡️ 6 道质量保证护城河

Style Distiller 不只是 prompt——6 道护城河确保**风格真的被用上**而不是"穿外壳"：

| # | 护城河 | 解决什么 | v2 状态 |
|---|---|---|---|
| **0** ⭐ | **自主进化** | AI 不再"学了忘"——遍历终版 + 作者偏好，下次自动应用 | **v2 新增** |
| 1 | 检索要准 | 50 个样本里挑 3-5 个最相关的（按主题相似度 + 维度匹配 + 时效加权） | 保留 |
| 2 | 档案翻译要硬 | 软描述 → 🚨🟡🟢 三层硬约束，不靠 LLM "理解" | 保留 |
| 3 | Prompt 组装要全 | 嵌入完整原文 + 特征签名 + 作者偏好，不只是摘要 | 保留 |
| 4 | 生成后必验证 | 7 维核对 + 反样本扫描 + 样本特征还原核对 | 保留 |
| 5 | 偏离自动修复 | 偏离 10-25% 自动改，>50% 自动重写（最多 2 次） | 保留 |

> ⚠️ 6 道不是装饰。LLM 在中文短文上有**强默认偏置**（鸡汤收尾、平台模板、空洞金句、网络梗）——护城河就是为了不让这些偏置偷渡进你的"风格输出"。

---

## 🎯 7 个风格维度 + 写作场景

Style Distiller 把"风格"拆成 7 个可独立观察的维度：

| 维度 | 它管什么 | 典型偏好 |
|---|---|---|
| **hook** 钩子 | 开场 3 秒抓人 | 对话开场 / 场景锚定 / 反常识断言 |
| **rhythm** 节奏 | 句长与断点 | 80% 在 25 字内 / 名词作结 / 段落 3-5 行 |
| **voice** 口气 | 整体调性 | 冷静克制 / 温和共情 / 锋利观点 |
| **verve** 金句 | 让人想截图的话 | 认知反差 / 自嘲 / 类比 |
| **closing** 收尾 | 怎么结尾 | 开放问题 / 留白 / 行动召唤 |
| **vocabulary** 词汇 | 口头禅与禁用词 | 高频词库 + 禁用词清单 |
| **format** 格式 | 排版习惯 | 段落长度 / emoji 密度 / 引用块 |

### 典型写作场景

| 平台 | 字数范围 | 调性建议 |
|---|---|---|
| 小红书 | 300-800 字 | 故事感 + 个人体验 + emoji 适度 |
| 朋友圈 | ≤200 字 | 真实感 + 短句 + 留白 |
| 微博 | ≤140 字 | 金句密度高 + 强观点 |
| 即刻 | 100-300 字 | 思考感 + 反共识 + 简洁 |
| 公众号 | 1500-3000 字 | 深度论证 + 故事钩子 |

---

## 📊 状态等级与数据目录

### 状态判定（v2 重大更新）

**总样本数 = 投喂样本 + 自写样本（results/ 按主题去重）**

> ⭐ **v2 新规则**：自写样本也算入阶段判定。同一题目（`result-{MMDD}_{标题}`）的初版+终版**只算一篇**，优先算终版——避免重复计数。

| 状态 | 总样本数 | 含义 |
|---|---|---|
| 🔴 **冷启动** | 0-2 | 主要靠通用基线 |
| 🟠 **萌芽** | 3-9 | 风格可见但不稳定 |
| 🟡 **学习** | 10-29 | 可用风格档案 |
| 🟢 **成熟** | ≥30 | 强风格还原度 |

你的当前状态：

```bash
python scripts/profile_stats.py
```

输出会同时显示 `state_basis=weights_json`（旧字段）和 `state_inferred`（新逻辑推断），让你看到差异。

### 数据目录结构

```
┌─────────────────────────────────────────┬──────────────────────────────────────┐
│       ~/.claude/styles/                 │     ~/.claude/skills/style-distiller/ │
│       （档案数据，隐私本地）             │     （工具方法论，GitHub 同步）       │
├─────────────────────────────────────────┼──────────────────────────────────────┤
│ ├── weights.json                       │ ├── SKILL.md           ← 聚合入口     │
│ ├── profile/                           │ ├── style-feed/                       │
│ │   ├── persona.md                     │ ├── style-feedback/                   │
│ │   ├── hook.md                        │ ├── style-reject/                     │
│ │   ├── rhythm.md                      │ ├── style-review/                     │
│ │   ├── voice.md                       │ ├── style-write/                      │
│ │   ├── verve.md                       │ │   ├── results/                      │
│ │   ├── closing.md                     │ │   │   ├── 初版/    ← v2            │
│ │   ├── vocabulary.md                  │ │   │   ├── 终版/    ← v2            │
│ │   └── format.md                      │ │   │   └── difference/  ← v2        │
│ ├── samples/                           │ ├── style-lib/        ← 共享 prompt    │
│ │   ├── positive/                      │ ├── references/      ← 5 份方法论     │
│ │   └── negative/                      │ └── scripts/          ← 4 个工具脚本   │
│ ├── drafts/                            │                                     │
│ └── backups/                           │                                     │
└─────────────────────────────────────────┴──────────────────────────────────────┘
```

> ⚠️ **数据/逻辑分离的好处**：你的写作样本永远不会上传到 GitHub。本地隐私、跨设备可迁移（手动拷贝 `~/.claude/styles/`）。

---

## 🔧 工具层与 references 方法论

### scripts/ 4 个工具脚本

| 脚本 | 作用 |
|---|---|
| `profile_stats.py` ⭐ | 统计档案状态。**v2 重构**：按主题去重自写样本，输出 `weights_state` 和 `inferred_state` 让差异可见 |
| `retrieve_samples.py` | 按主题 + 维度多路召回 Top N 样本（topic×0.5 + dim×0.3 + time×0.2 加权）|
| `verify_draft.py` | 对草稿做确定性自检——统计字数 + 扫禁用词命中 |
| `export_profile.py` | 合并 8 份 profile + weights + history 为单文件 Markdown，便于分享或备份 |

### references/ 5 份方法论文档

> ⭐ **v2 新增**。这是"为什么这样设计"而非"怎么用"——面向维护者、面试讲清楚、复盘演进。

| 文档 | 解决什么问题 |
|---|---|
| `action-level-extraction.md` | 为什么必须把"形容词"翻译成"动作" |
| `quality-guardrails.md` | 5 道护栏背后的 LLM 偏置恐惧 |
| `retrieval-strategy.md` | 50 个样本里怎么挑 3-5 个最相关的 |
| `verification-rubric.md` | 为什么必须事后核对而不能信模型"声称遵循" |
| `feedback-loop.md` | 4 类反馈 + 状态机的演进逻辑 |

---

## ❓ FAQ

### Q：我已经 /style-feed 投了 7 篇，为什么 state 还是 🔴？
A：v2 之前的逻辑只数投喂样本。**v2 把自写样本（你 results/ 里的文章）也算进去**——加起来 12 篇应该是 🟡 学习。如果你的还是 🔴，说明 results/ 还没文章。跑 `python scripts/profile_stats.py` 看细分数字。

### Q：`difference/` 是什么？怎么生成？
A：v2 新增。你先 `/style-write` 在 `results/初版/` 拿到 AI 草稿 → 自己改完后挪到 `results/终版/` → 用 `/style-feedback 对比` 触发逐字对比 → 生成的偏好清单在 `difference/`。下次 `/style-write` 自动应用。

### Q：聚合入口 `/style-distiller` 跟直接 `/style-feed` 啥区别？
A：聚合入口用自然语言识别意图。你说"帮我看看档案"，它识别为 review；说"练写作风格"，它识别为 feed。直接用 `/style-feed` 等命令是精确路由——已经知道要做什么时更快。两者不冲突。

### Q：我换台电脑怎么迁移？
A：拷贝 `~/.claude/styles/` 整个目录即可。工具层（`~/.claude/skills/style-distiller/`）重新 git clone。

### Q：怎么删除档案重新开始？
A：删 `~/.claude/styles/` 整个目录。下次触发任意 skill 会自动重建。

### Q：会泄露我的文章到 GitHub 吗？
A：**不会**。`~/.claude/styles/` 是完全本地的；仓库里 `.gitignore` 已经排除 `results/` 和 `difference/` 里的实际内容，只保留 `.gitkeep` 占位。

---

## 📜 版本

### v0.2.0（2026-08-20）— 自主进化 ⭐

**重大改动**：

- 🆕 仓库根新增聚合入口 `SKILL.md`（`/style-distiller` 路由 6 个 skill）
- 🆕 自主进化闭环：`results/初版/` → `终版/` → `difference/` → 下次自动应用偏好
- 🆕 深度对话挖掘：`/style-write` Phase 1 Q1-Q8 逐层提问确认写作意图
- 🆕 阶段判定重构：投喂样本 + 自写样本合计（按主题去重、终版优先）
- 🆕 references 方法论文档体系（5 份面向维护者/面试/复盘）
- 🔧 `profile_stats.py` 重构：支持自写样本去重统计
- 🔧 护城河从 5 道扩到 6 道（加 #0 自主进化）

### v0.1.0（2026-06-12）— MVP

- 5 个核心 skill（feed / feedback / reject / review / write）
- style-lib 共享 prompt 库（11 个 prompt）
- 5 道质量护城河（检索 / 翻译 / 组装 / 验证 / 修复）
- 7 个风格维度
- references 方法论文档（初版）

---

## 📄 License

MIT — 见 [LICENSE](LICENSE) 文件。