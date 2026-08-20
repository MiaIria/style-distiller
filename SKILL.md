---
name: style-distiller
description: 风格管理工作台——聚合入口，识别用户关于"个人写作风格训练"的模糊意图（喂文章/打分反馈/设禁忌/审视档案/生成写作），分发到对应子 skill。当用户提到 风格、写文章、我的风格、写作训练、训练素材、喂文章/喂素材、打分/评价/采纳/不满意、避雷/讨厌/油腻/煽情/说教、看看档案/成熟度、要求写个小红书/朋友圈/微博/即刻 等时触发。已用精确 /style-* 命令时不拦截。
argument-hint: "[意图关键词]"
version: "0.2.0"
user-invocable: true
allowed-tools: Skill, Read, Bash, Grep, Glob
---

# /style-distiller — 风格管理工作台（聚合入口）

> 把 5 个子 skill 串成一条训练流水线。
> 你是**路由中心**，不是**写作执行者**——真正的生成、档案更新都由子 skill 完成。

---

## 🎯 核心定位

| 你是什么 | 你不是什么 |
|---|---|
| ✅ 意图识别 + 路由分发 | ❌ 写作执行（交给 /style-write）|
| ✅ 状态查询 + 档案体检 | ❌ 样本写入（交给 /style-feed）|
| ✅ 复合任务的步骤串联 | ❌ 风格档案维护（交给 style-lib）|

---

## 📡 路由表（5 个意图 → 5 个子 skill）

| 用户意图 | 推荐 skill | 触发示例 |
|---|---|---|
| 喂入参考文章 | `/style-feed` | "我喜欢这篇"/"喂一篇文章"/"训练风格"/"分析这篇" |
| 给草稿打分反馈 | `/style-feedback` | "打分"/"这篇写得怎么样"/"采纳"/"不满意"/"给个评价" |
| 设置风格禁忌 | `/style-reject` | "我讨厌这篇"/"不要这样写"/"避雷"/"太油了"/"禁止油腻/煽情/说教" |
| 审视档案全貌 | `/style-review` | "看看我的风格"/"档案全貌"/"风格画像"/"成熟度" |
| 用风格生成写作 | `/style-write` | "用我的风格写"/"帮我写一篇"/"写个小红书/朋友圈/微博/即刻" |

**调用方式**（主对话 Claude 二选一）：
- **直接调用**：`Skill("style-feed", "<用户原文>")` —— 用户意图清晰时推荐
- **建议用户用命令**：告诉用户在主对话输入 `/style-feed <原文>` —— 用户希望保留手动控制时

---

## 🔁 复合任务标准流程

当用户意图跨多个 skill 时，按"**先建库，后生成**"顺序建议：

```
1. /style-feed       喂入参考文章（必选）
2. /style-feedback   对 AI 草稿打分（可选，加速收敛）
3. /style-reject     设置风格禁忌（可选）
4. /style-review     审视档案成熟度（可选，建议样本 ≥10 后做）
5. /style-write      用我的风格写一篇（终极目标）
```

⚠️ **不要跳步**——至少要喂过 1 篇才能 `/style-write`，否则档案是空的。

用户说"先帮我训练风格再写一篇"时，按上述顺序拆成多轮对话逐步执行。

---

## 📊 状态查询

要汇报档案当前状态，可执行：

| 操作 | 工具 |
|---|---|
| 样本统计 | `Bash: python scripts/profile_stats.py` |
| 最近终版 | `Read: style-write/results/终版/*.md`（文件名含日期） |
| 偏好学习 | `Read: style-write/difference/*.md` |
| 档案结构 | `Read: style-lib/SKILL.md` |

**汇报格式**：

```
📊 风格档案状态
- 样本数：N 篇（终版 M 篇、初版 K 篇、禁忌 J 篇）
- 当前阶段：cold_start / sprout / learning / mature
- 维度成熟度：🚨 不足 / 🟡 一般 / 🟢 成熟
- 最近操作：YYYY-MM-DD /style-xxx
- 推荐下一步：/style-xxx （1 句话理由）
```

状态等级判定参考 `references/feedback-loop.md` 的 4 段状态机定义。

---

## 🚫 何时不接管

**用户已用精确命令时不拦截**：

- 用户输入 `/style-feed xxx` → 告诉主对话 Claude "用户已指定 /style-feed，按其参数直接执行"
- 用户输入 `/style-write xxx` → 同上
- 不要在精确命令之外补充"建议"——避免干扰子 skill 的 5 道质量护城河流程

---

## ⚠️ 边界

| 不做的事 | 原因 |
|---|---|
| 不直接写档案/样本 | 你的 `allowed-tools` 没有 Write/Edit——保持职责单一，避免破坏子 skill 的状态机 |
| 不调用 `Skill("style-distiller", ...)` | 避免自我引用无限递归 |
| 不复述 style-lib 的 prompts | 子 skill 会自己 `Read style-lib/prompts/*.md`，重复加载浪费 token |
| 不替用户决定平台 | 用户说"写一篇"没指定平台时，先问"小红书/朋友圈/微博/即刻？"再调 /style-write |

---

## 🛠️ 触发后典型对话模板

**场景 A** —— 用户说"我想练写作风格"：
```
推荐流程：
1. /style-feed  喂入 3-5 篇你喜欢的好文章（先建库）
2. /style-feedback 对 AI 草稿打分（让档案校准）
3. /style-write  用你的风格写一篇

要现在开始第 1 步吗？直接贴一篇你喜欢的文章给我即可。
```

**场景 B** —— 用户说"用我的风格写一篇关于加班的小红书"：
```
意图明确：/style-write
参数提取：主题=加班、平台=小红书
建议：直接输入 /style-write 加班 小红书，或我帮你 Skill("style-write", "加班 小红书")
```

**场景 C** —— 用户说"看看我档案啥状态"：
```
📊 风格档案状态
- 样本数：12 篇（终版 8、初版 4）
- 当前阶段：learning
- 维度成熟度：🟡 一般（hook 🟢 / rhythm 🟡 / voice 🟢 / verve 🟡 / closing 🚨 / vocabulary 🟢 / format 🟢）
- 最近操作：2026-08-19 /style-feedback
- 推荐下一步：/style-feed 再喂 3 篇关于"开场"的文章，补齐 closing 维度
```

---

## 📚 关联文档（需要时 Read）

- `references/feedback-loop.md` —— 4 段状态机定义
- `references/quality-guardrails.md` —— 5 道护城河
- `references/retrieval-strategy.md` —— 多路召回策略
- `README.md` —— 用户文档
- `scripts/profile_stats.py` —— 档案统计脚本