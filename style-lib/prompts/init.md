# 初始化流程（首次运行）

> 当 `~/.claude/styles/` 目录不存在或 `weights.json` 缺失时执行。

## 触发条件

进入任何 /style-* 指令时，先检查：

```bash
test -d ~/.claude/styles && test -f ~/.claude/styles/weights.json
```

如果失败（目录或文件不存在），执行本流程。

## 步骤

### Step 1：创建目录

```bash
mkdir -p ~/.claude/styles/samples/positive
mkdir -p ~/.claude/styles/samples/negative
mkdir -p ~/.claude/styles/profile
mkdir -p ~/.claude/styles/drafts
mkdir -p ~/.claude/styles/backups
```

### Step 2：写入 8 份 profile 模板

从 `${CLAUDE_SKILL_DIR}/templates/` 复制 8 份模板到 `~/.claude/styles/profile/`：
- hook.md
- rhythm.md
- voice.md
- verve.md
- closing.md
- vocabulary.md
- format.md
- persona.md

> 如果 templates/ 缺失，则通过 Write 工具逐个创建（参考已存在的 ~/.claude/styles/profile/*.md 结构）。

### Step 3：写入 weights.json

如果不存在，写入初始 `weights.json`（参考 `${CLAUDE_SKILL_DIR}/templates/weights.json`）。

### Step 4：写入 history.md

写入：

```markdown
# 风格进化日志

## {今天日期}

- 初始化。8 份 profile 模板 + weights.json 已就位。等待首次 /style-feed 启动进化。
```

### Step 5：告知用户

```
✅ 风格档案已初始化！

📁 位置：~/.claude/styles/
📊 状态：🔴 冷启动（0 样本）

💡 下一步：随便挑一篇最近刷到的好文，/style-feed 喂给我。
   写一句"为什么吸引你"，比 1000 字原文更有用。
```

---

## 完整文件清单（初始化后应存在）

```
~/.claude/styles/
├── weights.json
├── history.md
├── profile/
│   ├── hook.md
│   ├── rhythm.md
│   ├── voice.md
│   ├── verve.md
│   ├── closing.md
│   ├── vocabulary.md
│   ├── format.md
│   └── persona.md
├── samples/
│   ├── positive/      (空)
│   └── negative/      (空)
├── drafts/            (空)
└── backups/           (空)
```
