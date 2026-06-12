# 5 个 Skill 的协同规则（核心文件）

> **任何 /style-* 流程执行时，必须先 Read 本文件了解与其他 4 个 skill 的协同关系。**
> 本文件是 style-feed / style-write / style-reject / style-feedback / style-review 5 个 skill 的"协同大脑"。

---

## 协同的 3 个层面

### 1. 数据层协同（已天然存在）

所有 5 个 skill 共享同一份档案 `~/.claude/styles/`：
- weights.json（状态机）
- profile/*.md（8 份画像）
- samples/positive/ + samples/negative/（样本库）
- drafts/（草稿）
- history.md（进化日志）

**任何 skill 的写入都会被其他 4 个读取**——数据天然同步。

### 2. 流程层协同（本文件定义）

每个 skill 在执行时要检查"是否需要触发其他 skill 的工作"。规则见下方矩阵。

### 3. 体验层协同（每个 skill 的反馈中）

每个 skill 的反馈末尾都要带"下一步建议"，引导用户到最相关的其他 skill。

---

## 协同触发矩阵

### 入口 A：style-feed（喂入正样本）

**主任务**：解析文章 → 提取风格 → 写入样本 + 更新档案

**必须做的事**：
1. Read `~/.claude/styles/weights.json` 判断状态
2. Write 样本到 `samples/positive/`
3. Edit 8 份 profile 差分更新
4. Edit weights.json +1
5. Append history.md

**条件触发**：

| 触发条件 | 协同动作 |
|---------|---------|
| 🔴 冷启动（0-2 样本）首次 | 跳 `prompts/cold_start.md` 引导 |
| 状态跨越阈值（🔴→🟠 / 🟠→🟡 / 🟡→🟢） | 输出🎉庆祝 + 提示"现在 /style-write 看效果" |
| 与现有档案某维度**强冲突** | 进入"风格分流"模式，询问用户是"保留旧档案"还是"用新样本替换" |
| 样本累计到 10 / 30 | 提示"档案成熟度提升，建议 /style-review 看看" |
| 提取时发现弱维度 | 提示"该维度样本不足，建议接下来 /style-feed 重点补该维度" |
| 用户备注引用了"自己写的" | 标 source: self，权重 ×1.2 |

**反馈末尾**：
```
💡 下一步建议：
  - [A] 试 /style-write 看新风格是否生效
  - [B] 继续 /style-feed 补样本
  - [C] /style-review 看档案全貌
```

---

### 入口 B：style-reject（喂入反样本）

**主任务**：提取反特征 → 写入禁忌区

**必须做的事**：
1. Read 现有 8 份 profile 找反特征对应位置
2. Write 反样本到 `samples/negative/`
3. Edit 各 profile 的"反特征"段
4. Edit persona.md 禁忌区
5. Edit weights.json 反样本 +1

**条件触发**：

| 触发条件 | 协同动作 |
|---------|---------|
| 反特征严重度 high | 提示"立即 /style-write 验证禁忌区是否生效" |
| 反样本累计到 5 | 提示"禁忌区成熟，/style-review 看看" |
| 反样本和正样本在同一维度冲突 | 提示"档案出现内部分裂，建议 /style-review 决断" |
| 用户反感的样本之前 /style-feed 过 | 提示"这个样本之前是喜欢的，是否要撤回 / 重新评估？" |

**反馈末尾**：
```
💡 下一步建议：
  - [A] /style-write 验证禁忌区生效
  - [B] 继续 /style-reject 标更多反例
  - [C] /style-review 看档案全貌
```

---

### 入口 C：style-write（生成文章）

**主任务**：加载档案 → 检索样本 → 组装 prompt → 生成草稿

**必须做的事**：
1. Read weights.json 判断状态
2. Read 8 份 profile
3. Bash 列出 samples/positive/ + samples/negative/ 选相关样本
4. Read 选中的 3-5 个样本
5. 组装风格 prompt
6. 生成草稿
7. Write 草稿到 `drafts/{date}_{N}_{slug}.md`

**条件触发**：

| 触发条件 | 协同动作 |
|---------|---------|
| 🔴 冷启动 | 跳 `prompts/cold_start.md` |
| 主题相关正样本 < 3 | 提示"该主题档案覆盖不足，建议先 /style-feed 几篇相关主题" |
| 主题档案完全空白 | 提示"档案里没有该主题样本，生成会偏通用" |
| 风格置信度 < 0.3 | 提示"档案不成熟，建议先 /style-feed 10 篇" |
| 草稿生成成功 | **强制**：提示"/style-feedback 打分，反向校准档案" |
| 草稿生成成功 + 评分可期待 | 提示"要不要 /style-reject 几个你最近反感的写法？"（构建反例库） |

**反馈末尾**：
```
💡 下一步建议：
  - [A] /style-feedback 打分（强烈推荐）
  - [B] 让 AI 重新生成（加调性要求）
  - [C] 手动修改后存档
```

---

### 入口 D：style-feedback（打分校准）

**主任务**：解析评分 → 反向校准档案权重

**必须做的事**：
1. Read 草稿文件（含元数据、风格报告）
2. 解析评分 + 采纳/不满意
3. Edit 对应 profile 调整权重
4. Append history.md

**条件触发**：

| 触发条件 | 协同动作 |
|---------|---------|
| 评分 ≥ 9 | **自动归档**：把本次草稿 copy 到 `samples/positive/`，作为"AI 生成的标杆样本"，下次 write 时优先检索 |
| 评分 ≤ 3 | **触发回退**：自动备份当前 profile 到 `backups/` + 提示"建议 /style-review 找问题" |
| 评分首次出现 | 提示"档案刚刚被反向校准了，建议 /style-review 看变化" |
| 用户纠错档案本身 | 跳到 feedback.md 的"场景 B"流程 + 提示"是否要 /style-write 验证纠错效果" |
| 用户撤回样本 | 差分回滚 8 份 profile + 提示"档案已回滚，建议 /style-review 确认" |

**反馈末尾**：
```
💡 下一步建议：
  - [A] /style-write 再写一篇看效果
  - [B] /style-review 看档案变化
  - [C] 继续 /style-feedback 打分更多草稿
```

---

### 入口 E：style-review（档案审视）

**主任务**：汇总展示档案全貌

**必须做的事**：
1. Read weights.json + 8 份 profile + history.md
2. Bash 统计样本/草稿/备份数
3. 汇总输出

**条件触发**：

| 触发条件 | 协同动作 |
|---------|---------|
| 状态 🔴 冷启动 | 提示"样本太少，先 /style-feed 3-5 篇" |
| 状态 🟠 萌芽 | 末尾建议"继续 /style-feed 到 10 篇解锁 🟡" |
| 状态 🟡 学习 | 末尾建议"试 /style-write 看实际效果" |
| 状态 🟢 成熟 | 末尾建议"持续使用 + 定期 review" |
| 某维度 ▱ > 5 | 提示"该维度样本不足，建议 /style-feed 标 {该维度}" |
| 反样本 < 3 | 提示"建议 /style-reject 标几个你反感的写法" |
| 档案 30 天未审视 | Append history.md 月度审视 |
| 用户要求导出 | 生成 export 文件 + 提示"备份到哪" |

**反馈末尾**：
```
💡 下一步建议（基于档案状态智能推荐）：
  - [A] {基于当前状态的最优下一步}
  - [B] {第二推荐}
  - [C] {第三推荐}
```

---

## 全局协同规则

### 规则 1：写后必读

**任何 skill 写入 profile/ 之后**，都应该假设"档案变了"，在反馈中提示用户"可以 /style-review 看看变化"或"可以 /style-write 验证效果"。

### 规则 2：读后必反思

**任何 skill 从档案读出数据时**，都要检查档案是否"健康"：
- 样本量足够吗？
- 维度分布均匀吗？
- 反样本是否覆盖了主要维度？
- 是否有明显冲突？

不健康时要主动提示用户。

### 规则 3：跨流程的"档案一致性"

**所有 skill 必须使用 Read weights.json 拿到的是同一份状态**。不要在内存中缓存超过 1 个流程的状态。如果连续执行多个 skill，每次都重新读 weights.json。

### 规则 4：失败优雅降级

**如果某个 skill 失败**（如读不到档案、写不进去），其他 4 个 skill 必须能继续工作——不能因为某个 skill 挂了导致全局瘫痪。

### 规则 5：协同提示 ≠ 强制跳转

**协同触发是用"建议"的形式呈现给用户**，让用户决定是否执行，不是自动跳转到其他 skill。

例外：冷启动引导（cold_start）和风格分流等场景，可以**直接执行**而不询问用户。

---

## 协同工作的 3 个典型场景

### 场景 1：训练-生成-反馈循环（最常见）

```
用户: /style-feed
  → [feed] 写入样本
  → 反馈："档案状态 🟠 萌芽，建议 /style-write 看效果"

用户: /style-write
  → [write] 加载档案 + 生成
  → 反馈："生成完成，请 /style-feedback 打分"

用户: /style-feedback
  → [feedback] 反向校准
  → 反馈："档案已校准，建议再 /style-write 看效果"
```

### 场景 2：发现弱维度专项补

```
用户: /style-review
  → [review] 发现 closing 维度 ▱▱▱▱▱▱▱▱▱▱（样本少）
  → 反馈："closing 维度样本不足，建议 /style-feed 时标'收尾'维度"

用户: /style-feed [3 篇标 closing]
  → [feed] closing 维度 +3
  → 反馈："closing 维度已补足，建议 /style-write 收尾相关主题"
```

### 场景 3：发现反特征后立即验证

```
用户: /style-reject [1 篇油腻文章]
  → [reject] 写入禁忌区
  → 反馈："已加入禁忌区，建议 /style-write 验证"

用户: /style-write
  → [write] 加载档案（含新禁忌区）+ 生成
  → 输出：刻意避开"油腻"写法
  → 反馈："本次生成已避开 {N} 个禁忌词，满意的话 /style-feedback 打分"
```

---

## 检查清单（每次执行 /style-* 时）

- [ ] Read weights.json → 知道当前状态
- [ ] Read coordinate.md（本文件）→ 知道协同规则
- [ ] 执行主流程
- [ ] 触发条件检查（按矩阵）
- [ ] 输出末尾必带"下一步建议"（指向其他 skill）
- [ ] 写操作后更新 history.md

---

## 写在最后

5 个 skill 是一台机器的 5 个齿轮：

```
  ┌─ feed ─┐   ┌─ reject ─┐
  │ 输入端  │   │ 反向输入 │
  └────┬───┘   └─────┬────┘
       │             │
       ▼             ▼
       ┌─ profile 档案（共享）─┐
       │   ~/.claude/styles/   │
       └──────────┬─────────────┘
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
   ┌─write─┐  ┌─review─┐  ┌─feedback─┐
   │  加工  │  │  体检  │  │   校准    │
   └───────┘  └────────┘  └───────────┘
       │          │          │
       └──────────┴──────────┘
                  │
                  ▼
           你的文章（drafts/）
```

**任何齿轮不转，其他齿轮都受影响**。所以每个 skill 执行时必须**先想"我要不要触发其他齿轮"**。
