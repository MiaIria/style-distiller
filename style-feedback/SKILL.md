---
name: style-feedback
description: "对 AI 生成的草稿打分 + 批注，反向校准风格档案。让 Skill 记住'这次哪些像你哪些不像'，下次生成更准。Use when user says '/style-feedback', '打分', '给个评价', '这篇写得怎么样', '采纳/不满意'."
argument-hint: "[草稿ID] [评分: 1-10] [采纳部分] [不满意部分]"
version: "0.1.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# /style-feedback — 给生成结果打分

> 对 AI 写的草稿打分/批注，反向校准档案，让下次更准。

---

## 触发

当用户说 `/style-feedback`、或表达"打分"、"这篇写得怎么样"、"采纳 / 不满意"时，路由到这里。

---

## 0️⃣ 第一步：先读协同规则

```
Read ~/.claude/skills/style-lib/prompts/coordinate.md
```

了解 style-feedback 与其他 4 个 skill（feed/write/reject/review）的协同触发条件。

## 1️⃣ 第二步：读主流程

```
Read ~/.claude/skills/style-lib/prompts/feedback.md
```

按 feedback.md 中的流程完整执行。

## 🤝 第三步：协同工作（强制）

执行完主流程后，**必须**根据 coordinate.md 的"入口 D：style-feedback"触发矩阵：

| 触发条件 | 必须动作 |
|---------|---------|
| 评分 ≥ 9 | **自动归档**：copy 草稿到 samples/positive/ 作为"AI 生成的标杆样本" |
| 评分 ≤ 3 | **触发回退**：自动备份当前 profile + 提示"/style-review 找问题" |
| 评分首次出现 | 提示"/style-review 看变化" |
| 用户纠错档案本身 | 跳 feedback.md 场景 B + 提示"/style-write 验证纠错" |
| 用户撤回样本 | 差分回滚 + 提示"/style-review 确认" |

**反馈末尾必须带**：
```
💡 下一步建议：
  - [A] /style-write 再写一篇看效果
  - [B] /style-review 看档案变化
  - [C] 继续 /style-feedback 打分更多草稿
```

---

## 第二步：与用户的对话模板

收到 `/style-feedback` 但信息不全时：

```
📊 给草稿打分，让档案越用越准

请告诉我 4 件事：

1️⃣ 草稿（必填）
   - 草稿 ID（如 drafts/2026-06-02_001_xxx.md）
   - 或简单说"最近那篇"

2️⃣ 评分（必填）
   - 1-10 分
   - 9-10 = 几乎完美（标杆样本）
   - 7-8 = 大部分像
   - 4-6 = 部分像
   - 1-3 = 几乎不像（触发回退）

3️⃣ 采纳部分（可选）
   - 哪些特征/句子喜欢
   - 例："开头场景"、"自嘲口吻"

4️⃣ 不满意部分（可选）
   - 哪些不喜欢
   - 例："结尾太正"、"用了油腻词"
```

---

## 输出格式

按 feedback.md 的反馈格式：

```
📊 反馈已记录！

📝 草稿 #001（生成于 {时间}）
⭐ 评分：{N}/10

✅ 采纳：{采纳内容}
❌ 不满意：{不满意内容}

📈 档案变化：
  - {维度}：{特征} {+/- 0.1} 权重
  - ...

💡 建议：
  - {进化建议}

下次 /style-write 会更准。
```

---

## 共享库引用

- 主流程：`~/.claude/skills/style-lib/prompts/feedback.md`
- 完整文档：`~/.claude/skills/style-lib/README.md`
