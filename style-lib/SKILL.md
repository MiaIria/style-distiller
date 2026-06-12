---
name: style-lib
description: "Style Distiller 共享库 - 5 个公开 skill（style-feed/style-write/style-reject/style-feedback/style-review）共用的 prompts/ 文档和初始化逻辑。本 skill 不暴露在 / 菜单，由其他 5 个 skill 引用。Read ~/.claude/skills/style-lib/prompts/{feed|write|reject|feedback|review|init|cold_start|extract}.md"
argument-hint: ""
version: "0.1.0"
user-invocable: false
allowed-tools: Read
---

# Style Distiller · 共享库

> 5 个公开 skill（style-feed / style-write / style-reject / style-feedback / style-review）共用的提示词库。
> 本 skill 不暴露在用户的 / 菜单中，只作为内部引用。

---

## 内容清单

```
~/.claude/skills/style-lib/
├── README.md                    完整使用说明
└── prompts/
    ├── extract.md               动作级提取方法论（核心）
    ├── feed.md                  /style-feed 主流程
    ├── write.md                 /style-write 主流程
    ├── reject.md                /style-reject 主流程
    ├── feedback.md              /style-feedback 主流程
    ├── review.md                /style-review 主流程
    ├── init.md                  首次初始化流程
    └── cold_start.md            冷启动引导
```

---

## 数据存储位置

```
~/.claude/styles/                个人风格档案（与 skill 分离）
├── weights.json
├── history.md
├── profile/                     8 份风格画像
├── samples/positive/
├── samples/negative/
├── drafts/
└── backups/
```

---

## 设计原则

1. **一个 skill 一个职责**：5 个公开 skill 各自薄，逻辑共享
2. **数据与逻辑分离**：风格档案在 `~/.claude/styles/`，prompts 在 `~/.claude/skills/style-lib/`
3. **每个公开 skill 都引用本库**：用 `Read ~/.claude/skills/style-lib/prompts/{name}.md` 加载具体流程
4. **本 skill 不暴露给用户**：`user-invocable: false`
