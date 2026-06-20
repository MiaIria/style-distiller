# Style Distiller · 写作风格蒸馏器

> 用 5 个 Claude Code Skill 训练一个「像你写作」的 AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-blue)](https://github.com/MiaIria/style-distiller)
[![Platform](https://img.shields.io/badge/platform-Claude%20Code-purple)](https://claude.ai/code)

---

## 🎯 这是什么

你可能遇到过这些问题：

- 让 AI "帮我写一篇小红书" → 写出来是模板味儿
- 让 AI "用我的风格写" → 它根本不认识你
- 选"小红书体"/"知乎体"模板 → 你不想变成一个模板

**Style Distiller 不替你写，它学你怎么写。**

它维护一份"你的文字人格档案"，每次你：

| 操作 | 指令 | 效果 |
|------|------|------|
| 刷到一篇好文 | `/style-feed` | 蒸馏出可迁移的风格特征，更新档案 |
| 看到讨厌的写法 | `/style-reject` | 写入禁忌区，下次自动避开 |
| 让 AI 写一篇 | `/style-write` | 按你的档案生成，自动验证风格还原度 |
| 对结果打分 | `/style-feedback` | 反向校准档案权重，让下次更准 |
| 想看档案全貌 | `/style-review` | 汇总展示 + 进化建议 |

档案就更新一次，你的 AI 就更懂你一点。

---

## 📦 安装（2 分钟）

### 前提条件

- 已安装 [Claude Code](https://claude.ai/code)（CLI 或 VS Code / JetBrains 扩展）
- Git

> Claude Code 的 skills 目录默认为 `~/.claude/skills/`，以下命令均按此路径。如果你自定义了 skills 路径，请替换为你的实际路径。

### 方法一：Git Clone（推荐）

<details open>
<summary><b>macOS / Linux</b></summary>

```bash
git clone https://github.com/MiaIria/style-distiller.git ~/.claude/skills/
```

</details>

<details>
<summary><b>Windows</b></summary>

**Git Bash：**

```bash
git clone https://github.com/MiaIria/style-distiller.git ~/.claude/skills/
```

**PowerShell：**

```powershell
git clone https://github.com/MiaIria/style-distiller.git $env:USERPROFILE\.claude\skills\
```

</details>

### 方法二：手动下载

1. 下载本仓库 [ZIP](https://github.com/MiaIria/style-distiller/archive/refs/heads/main.zip) 并解压
2. 将解压后文件夹内的 6 个 `style-*` 目录复制到 Claude Code 的 skills 目录

<details open>
<summary><b>macOS / Linux</b></summary>

```bash
# 假设解压到了 ~/Downloads/style-distiller/
cp -r ~/Downloads/style-distiller/style-* ~/.claude/skills/
```

</details>

<details>
<summary><b>Windows</b></summary>

**PowerShell：**

```powershell
# 假设解压到了 C:\Users\<你的用户名>\Downloads\style-distiller\
Copy-Item -Recurse $env:USERPROFILE\Downloads\style-distiller\style-* $env:USERPROFILE\.claude\skills\
```

**文件资源管理器：**

直接将 6 个 `style-*` 文件夹拖入 `C:\Users\<你的用户名>\.claude\skills\` 即可。

</details>

### 创建数据目录

<details open>
<summary><b>macOS / Linux</b></summary>

```bash
mkdir -p ~/.claude/styles/
```

</details>

<details>
<summary><b>Windows</b></summary>

**PowerShell / CMD：**

```powershell
# PowerShell
New-Item -ItemType Directory -Force -Path $env:USERPROFILE\.claude\styles
```

```cmd
:: CMD
mkdir %USERPROFILE%\.claude\styles
```

</details>

> 💡 数据目录在首次使用 `/style-feed` 或 `/style-write` 时会自动初始化，也可手动创建。

### 验证安装

在 Claude Code 中输入 `/`，你应该能看到 5 个新指令：

```
/style-feed      把好文章喂给 style-distiller 档案
/style-write     用你的个人风格写一篇短文
/style-reject    把你反感的文章喂给 style-distiller 档案
/style-feedback  对 AI 生成的草稿打分 + 批注
/style-review    审视你的个人写作风格档案全貌
```

---

## 🚀 快速开始（5 分钟）

### 第一次使用

直接输入：

```
/style-write 主题: 周末不想起床 长度: 300 平台: 小红书
```

系统检测到档案为空，会进入**冷启动引导**——3 个选择题（1 分钟），然后自动试写。

### 喂入第一篇自我样本

```
/style-feed
[粘贴你自己写的一篇短文]
维度: 综合
备注: 这篇是我最近最满意的一篇
```

> 💡 1 篇自我样本权重 = 1.2x，相当于 3 篇外部样本，状态会从 🔴 → 🟠

### 喂入第一篇外部样本

```
/style-feed
[粘贴你喜欢的一篇短文]
维度: 开头
备注: "开头那个反问直接把我钉住了"
```

### 解锁完整能力

- 累计到 10 篇 → 🟡 学习期（比较像你了）
- 累计到 30 篇 → 🟢 成熟期（高度还原你的风格）

---

## 📊 状态等级

| 状态 | 样本量 | 能力 |
|------|--------|------|
| 🔴 冷启动 | 0-2 | 通用基线 + 3 题引导 |
| 🟠 萌芽 | 3-9 | 风格初形，可能不太准 |
| 🟡 学习 | 10-29 | 比较像你了 |
| 🟢 成熟 | ≥ 30 | 高度还原你的风格 |

---

## 📚 5 个核心指令

| 指令 | 何时用 | 输入 |
|------|--------|------|
| `/style-feed` | 刷到喜欢的文章 | 原文 + 维度 + 备注 |
| `/style-reject` | 看到讨厌的文章 | 原文 + 反感原因 |
| `/style-write` | 想写一篇文章 | 主题 + 长度 + 平台 + 调性 |
| `/style-feedback` | AI 写完了 | 草稿 ID + 评分 + 采纳项 |
| `/style-review` | 想看档案全貌 | （无，直接运行）|

### 协同机制

这 5 个 Skill 不是孤岛——它们通过协同规则互联：

- `/style-feed` 完成 → 提示 `/style-write` 看效果
- `/style-write` 完成 → **强制**提示 `/style-feedback` 打分
- `/style-feedback` 评分 ≥ 9 → 自动归档为标杆样本，下次写入优先检索
- `/style-feedback` 评分 ≤ 3 → 触发回退，提示 `/style-review` 找问题
- `/style-reject` 高严重度 → **强制**提示 `/style-write` 验证

---

## 📂 目录结构

### 工具层（本仓库内容）

```
style-distiller/
├── style-feed/SKILL.md              ← /style-feed 入口
├── style-write/SKILL.md             ← /style-write 入口（含 5 道护城河）
├── style-reject/SKILL.md            ← /style-reject 入口
├── style-feedback/SKILL.md          ← /style-feedback 入口
├── style-review/SKILL.md            ← /style-review 入口
├── references/                      ← 方法论说明（面试/维护用）
│   ├── action-level-extraction.md
│   ├── quality-guardrails.md
│   ├── retrieval-strategy.md
│   ├── verification-rubric.md
│   └── feedback-loop.md
├── scripts/                         ← 确定性辅助脚本
│   ├── profile_stats.py             ← 统计档案状态
│   ├── retrieve_samples.py          ← 按主题/维度/时间召回样本
│   ├── verify_draft.py              ← 检查草稿禁用词和长度
│   └── export_profile.py            ← 导出风格档案
└── style-lib/                       ← 共享库（内部引用，不暴露在 / 菜单）
    ├── SKILL.md
    ├── README.md                    ← 完整使用说明
    └── prompts/                     ← 11 个提示词文件
        ├── coordinate.md            ← 5 skill 协同大脑
        ├── extract.md               ← 动作级提取方法论（核心）
        ├── retrieval.md             ← 多路召回策略
        ├── verify.md                ← 7 维自动验证
        ├── feed.md / write.md / reject.md / feedback.md / review.md
        ├── init.md / cold_start.md
```

### 数据层（你的个人档案，不在仓库中）

```
~/.claude/styles/                    ← 仅存在于你的本地
├── weights.json                     ← 维度权重 + 状态机
├── history.md                       ← 进化日志
├── profile/                         ← 8 份风格画像
│   ├── hook.md / rhythm.md / voice.md / verve.md
│   ├── closing.md / vocabulary.md / format.md / persona.md
├── samples/positive/                ← 你喜欢的文章
├── samples/negative/                ← 你反感的文章
├── drafts/                          ← AI 生成的草稿
└── backups/                         ← 最近 5 个档案备份
```

### scripts/ 的定位

`scripts/` 不替代 `style-lib/prompts/` 的核心流程，只把重复、可检查的步骤脚本化：

- `/style-review` 前可运行 `profile_stats.py` 快速查看档案状态
- `/style-write` 前可运行 `retrieve_samples.py` 辅助选择相关样本
- 草稿生成后可运行 `verify_draft.py` 做基础违规扫描
- 需要展示或备份档案时可运行 `export_profile.py`

### references/ 的定位

`references/` 不是运行时 prompt，而是对设计方法论的拆解：动作级提取、样本检索、质量护栏、生成验证和反馈闭环。它适合用于维护、复盘和面试展示。

---

## 🧠 工作原理

Style Distiller 不能真改模型参数，它用 4 大机制模拟"训练"：

```
┌────────────────────────────────────────────┐
│  1. 上下文工程：把档案塞进每次生成的 prompt   │
│  2. 检索增强：从样本库找最相关的参考          │
│  3. 规则蒸馏：把样本特征翻译成"动作级"指令    │
│  4. 反馈循环：你的打分反向更新档案权重        │
└────────────────────────────────────────────┘
```

**核心创新：动作级提取**

不说"文笔细腻"这种空话，而是提取 AI 能直接执行的具体动作：

- ❌ "文笔细腻" → ✅ "80% 句子在 25 字以内，偏好用名词作结"
- ❌ "有深度" → ✅ "先讲反常识现象，再引出洞察；不讲大道理"
- ❌ "开头抓人" → ✅ "67% 用对话开场，33% 用场景锚定"

---

## 🛡️ 5 道质量保证护城河

**承诺：训练 50 篇不会白费。**

| # | 护城河 | 解决什么 |
|---|--------|---------|
| 1 | **检索要准** | 50 个样本里挑 3-5 个最相关的（主题 + 维度 + 时效 多路召回）|
| 2 | **档案翻译要硬** | 软描述 → 🚨🟡🟢 三层硬约束 |
| 3 | **Prompt 组装要全** | 嵌入样本完整原文 + 7 维特征签名，不只是摘要 |
| 4 | **生成后自动验证** | 7 维硬约束核对 + 反样本扫描 + 样本特征还原核对 |
| 5 | **偏离自动修复** | 偏离 10-25% 自动改，>50% 自动重写（最多 2 次）|

---

## 🎯 7 个风格维度

| 维度 | 问什么 |
|------|--------|
| **钩子 hook** | 开头 1-2 句怎么抓人 |
| **节奏 rhythm** | 句长、断行、停顿 |
| **口气 voice** | 像什么人在说话 |
| **金句 verve** | 喜欢什么样的"亮句" |
| **收尾 closing** | 怎么结束有回味 |
| **词汇 vocabulary** | 常用词 / 禁用词 |
| **格式 format** | 排版 / emoji / 标点 |
| **人格 persona** | 综合画像（从 7 维蒸馏）|

---

## 💡 写作场景

当前重点优化了**短文场景**：

- 小红书（300-800 字）
- 即刻（300-800 字）
- 朋友圈随笔（100-300 字）
- 微博（100-300 字）

长文场景（1500+ 字）可用但不是最优。后续会扩展。

---

## 📈 进化路径建议

### 第 1 周：种子期
- 冷启动引导（3 分钟）
- `/style-feed` 2-3 篇你最满意的自我文章
- 试 `/style-write` 1-2 篇，看效果

### 第 1 个月：积累期
- 每天刷到好文顺手 `/style-feed`（累计 10-15 篇）
- 偶尔 `/style-reject` 标记你不喜欢的写法
- 档案从 🟠 → 🟡

### 第 3 个月：稳定期
- 累计 30+ 样本，档案 🟢 成熟
- `/style-write` 几乎都"像你"
- 用 `/style-feedback` 做微调

---

## ❓ FAQ

**Q：会被 AI 写得像模板吗？**
A：不会。我们故意避免了"排比 + 升华 + 喊口号"这类模板化写法，档案反而偏好反类型写法。生成后还有反样本扫描兜底。

**Q：我的档案会被别人看到吗？**
A：不会。所有数据只在本地 `~/.claude/styles/`，不上传。本仓库只有工具代码，没有用户数据。

**Q：可以多人共享一份档案吗？**
A：可以。把 `~/.claude/styles/` 整个文件夹复制给朋友，他会得到一份"你的风格"副本，之后各自独立演化。

**Q：可以重置档案吗？**
A：可以。`/style-review` → 选择"重新初始化"会清空所有数据并重建。

**Q：能蒸馏其他语言吗？**
A：当前设计针对**简体中文短文**。其他语言可用但未优化。

---

## 📜 版本

- **v0.1.0**（2026-06-02）：MVP 首发
  - 5 个公开 Skill：`/style-feed` `/style-write` `/style-reject` `/style-feedback` `/style-review`
  - 7 维 + persona 共 8 份画像
  - 冷启动 3 题引导
  - 5 道质量保证护城河
  - 5 Skill 协同机制
  - 实时档案更新 + 时间衰减权重

---

## 📄 License

MIT © [MiaIria](https://github.com/MiaIria)
