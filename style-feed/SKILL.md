---
name: style-feed
description: "把好文章喂给 style-distiller 档案，训练你的个人写作风格。粘贴你喜欢的文章 + 一句'为什么戳中我'，Skill 会自动蒸馏出可迁移的风格特征。Use when user says '/style-feed', '喂入文章', '喂一篇文章', '我喜欢这篇文章', '训练我的风格', or shares an article they like and wants to feed it to the style system."
argument-hint: "[粘贴文章] [维度] [备注]"
version: "0.1.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# /style-feed — 喂入正样本

> 把你喜欢的文章/段落喂给个人风格档案，AI 会自动蒸馏出"动作级"风格特征。

---

## 触发

当用户说 `/style-feed`、或粘贴一篇文章说"我喜欢"、"喂入"、"训练"时，路由到这里。

---

## 0️⃣ 第一步：先读协同规则

```
Read ~/.claude/skills/style-lib/prompts/coordinate.md
```

了解 style-feed 与其他 4 个 skill（write/reject/feedback/review）的协同触发条件。

## 1️⃣ 第二步：读主流程

```
Read ~/.claude/skills/style-lib/prompts/feed.md
```

按 feed.md 中的流程完整执行。

## 🤝 第三步：协同工作（强制）

执行完主流程后，**必须**根据 coordinate.md 的"入口 A：style-feed"触发矩阵，检查并执行以下条件触发：

| 触发条件 | 必须动作 |
|---------|---------|
| 🔴 冷启动首次 | 跳 cold_start.md 引导 |
| 状态跨越阈值 | 输出🎉 + 提示"现在 /style-write 看效果" |
| 档案某维度强冲突 | 进入"风格分流"模式，询问用户 |
| 累计到 10/30 样本 | 提示"建议 /style-review 看看" |
| 发现弱维度 | 提示"接下来 /style-feed 重点补该维度" |
| 备注含"自己写的" | 标 source: self，权重 ×1.2 |

**反馈末尾必须带**：
```
💡 下一步建议：
  - [A] /style-write 看新风格效果
  - [B] 继续 /style-feed 补样本
  - [C] /style-review 看档案全貌
```

---

## 第二步：检查初始化状态

进任何 /style-* 流程前，先读：
```
Read ~/.claude/styles/weights.json
```

如果 `current_state: cold_start` 且正样本 < 3：
- **首次喂入**走 `${CLAUDE_SKILL_DIR}/../../style-lib/prompts/cold_start.md` 的引导
- 已引导过则继续走主流程

---

## 第三步：与用户的对话模板

收到 `/style-feed` 但用户没贴文章时：

```
📝 我准备好吸收新样本了！

请告诉我 3 件事（最少 1 件）：

1️⃣ 原文（必填）
   - 直接粘贴文章 / 一段 / 一句
   - 或贴一个 URL
   - 或说"[我自己写的]"然后贴你的文章

2️⃣ 维度（可选）
   - 开头 / 表达方式 / 内容 / 收尾 / 综合
   - 不确定就标"综合"

3️⃣ 备注（强烈建议 ⭐）
   - "开头那个反问把我钉住了"
   - "最后一句让我想了一晚上"
   - 一句话即可

也可以直接贴文章，我帮你猜。
```

---

## 反馈给用户的格式

按 feed.md Step 7 的格式输出。核心 3 行：
```
✅ 样本已吸收！ID: {id}
📊 档案变化：{维度 +1 / 占比从 X% → Y%}
💡 下一步：{进化建议}
```

---

## 共享库引用

- 主流程：`~/.claude/skills/style-lib/prompts/feed.md`
- 提取方法论：`~/.claude/skills/style-lib/prompts/extract.md`
- 冷启动：`~/.claude/skills/style-lib/prompts/cold_start.md`
- 初始化：`~/.claude/skills/style-lib/prompts/init.md`
- 完整文档：`~/.claude/skills/style-lib/README.md`
