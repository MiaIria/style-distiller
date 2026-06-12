---
name: style-reject
description: "把你反感的文章/写法喂给 style-distiller 档案，形成'禁忌区'。Skill 会提取反特征（油腻/煽情/说教/套路化...）写入 persona 禁忌清单，生成时自动避开。Use when user says '/style-reject', '这篇我讨厌', '不要这样写', '这个写法太油了', '避雷'."
argument-hint: "[粘贴文章] [反感原因]"
version: "0.1.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# /style-reject — 喂入反样本（避雷）

> 把你反感的写法标记成"禁忌区"，AI 以后会主动避开。

---

## 触发

当用户说 `/style-reject`、或表达"讨厌"、"反感"、"太油"、"避雷"、"不要这样写"时，路由到这里。

---

## 0️⃣ 第一步：先读协同规则

```
Read ~/.claude/skills/style-lib/prompts/coordinate.md
```

了解 style-reject 与其他 4 个 skill（feed/write/feedback/review）的协同触发条件。

## 1️⃣ 第二步：读主流程

```
Read ~/.claude/skills/style-lib/prompts/reject.md
```

按 reject.md 中的流程完整执行。

## 🤝 第三步：协同工作（强制）

执行完主流程后，**必须**根据 coordinate.md 的"入口 B：style-reject"触发矩阵：

| 触发条件 | 必须动作 |
|---------|---------|
| 反特征严重度 high | **强制**提示"立即 /style-write 验证禁忌区" |
| 反样本累计到 5 | 提示"/style-review 看看" |
| 反样本和正样本冲突 | 提示"档案分裂，建议 /style-review 决断" |
| 用户反感的样本之前 /style-feed 过 | 提示"撤回 / 重新评估？" |

**反馈末尾必须带**：
```
💡 下一步建议：
  - [A] /style-write 验证禁忌区生效
  - [B] 继续 /style-reject 标更多反例
  - [C] /style-review 看档案全貌
```

---

## 第二步：与用户的对话模板

收到 `/style-reject` 但用户没贴文章时：

```
🚫 把反感的写法标记成"禁忌区"

请告诉我 2 件事：

1️⃣ 文章/片段（必填）
   - 粘贴让你反感的文章 / 一段
   - 或贴一个 URL
   - 或直接说"我讨厌 [某种写法]"

2️⃣ 反感原因（强烈建议 ⭐）
   - "词汇油腻 / 强行煽情 / 套路化 / 说教..."
   - 或具体句子："最后一段的'让我们一起...'我看到就划走"

也可以直接贴文章 + 一句"我讨厌这个"，我帮你分析。
```

---

## 输出格式

按 reject.md 的反馈格式：

```
🚫 反样本已记录！

📝 ID：{id}
📂 入库：samples/negative/
⚠️ 严重度：{high/medium/low}

📋 检测到的反特征：
  - 词汇油腻：{列举}
  - 鸡汤说教：{描述}
  - 强行升华收尾

🛡️ 写入禁忌区：
  → persona.md 禁忌清单 +3 条
  → vocabulary.md 忌讳词 +2 个
  → closing.md 反特征 +1 条

✅ 下次 /style-write 会自动避开这些写法。
```

---

## 共享库引用

- 主流程：`~/.claude/skills/style-lib/prompts/reject.md`
- 提取方法论：`~/.claude/skills/style-lib/prompts/extract.md`
- 完整文档：`~/.claude/skills/style-lib/README.md`
