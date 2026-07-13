# breaking-coding-chaos

**breaking-coding-chaos（BCC）** 是一套 **人在环路（human-in-the-loop）的双环控制面 Agent Skill**：在用 coding agent 落地 idea 时，帮你掌控**进度**与**技术细节**，分步交付、不丢主线。

**适用于所有 agents。** 标准 Agent Skills 目录（`SKILL.md`），可装到 Claude Code、Codex、Grok、Cursor、OpenCode、Hermes、OpenClaw，以及任何支持同一 skill 格式的运行时。

[English](../README.md) | [简体中文](./README.zh-CN.md) | [繁體中文](./README.zh-TW.md)

动机说明、How it works 架构图与致谢表见 **[英文 README](../README.md)**（banner + architecture + Pipeline by act）。

**前提：** 需要一个**还算完善的 idea**（做什么、怎么算做成）。本 skill 帮你 **1:1 实现** 并掌控进度/细节，**不是**从零空想产品；没有 idea 就无法诚实开码。

**为何需要：** Agent 易失忆与幻觉；全局模糊记忆（如 mem0 / agentmemory）更适合长期回忆，却可能稀释高难度实现时的注意力。BCC 用双环控制面：throughline 管全局落盘，plan-spar 管当前 PLAN 对齐与对抗审，clean-cut 最小实现并强制回写。

1. **bcc-throughline** — 全局三文件（`plans`/`progress`/`findings`）  
2. **bcc-plan-spar** — **必须在 throughline 之后**；维护**唯一** `PLAN.md`（每片就地更新，不靠多 PLAN 切片文件）  
3. **bcc-clean-cut** — 最小实现 + 验证 + **强制回写** throughline  

**命名：** slash 用 `bcc-`；聊天可用 `bcc:`。  
**结构：** 仅 **1 主 + 3 子** skill，无额外 slash。状态/下一步内嵌在主 skill。  
**安装：** `.\install.ps1`（默认只装 Grok，避免 Codex 等臃肿）。

---

## Skills（仅 4 个）

| Skill | 职责 |
|-------|------|
| `bcc-breaking-coding-chaos` | **主**：Mode A 串流程 **或** 短状态+建议 |
| `bcc-throughline` | 全局三文件 |
| `bcc-plan-spar` | throughline 之后；唯一 PLAN |
| `bcc-clean-cut` | 写码 + 强制回写 |

```text
bcc-throughline → plan-spar（APPROVE）→ bcc-clean-cut → 回写 throughline
```

**命名：** plan-spar = 搞计划；clean-cut = 干净下刀写码（对应 ponytail）。

**`bcc-breaking-coding-chaos` 不是必经入口**——可以直接 `/bcc-throughline` 起步。见下方两种用法。

---

## 两种使用方向

同一套四个 skill、同一套产物文件；差别在于**谁驱动步骤顺序**。

### 方向 A — Agent 自己串（编排）

**适合：** 第一次用 BCC、目标较大、不想记命令顺序。

**入口：** `/bcc-breaking-coding-chaos`（或：「用 BCC 做某某」）

```text
你 → /bcc-breaking-coding-chaos
      → throughline（大地图 / 进度 / 调整）
      → plan-spar（对齐 → 锁 PLAN → 自动 review）
      → 你 APPROVE 再写
      → bcc-clean-cut（最小实现 + 验证 + 回写）
      → throughline（看进度；下一片或停）
```

你仍要回答对齐问题、最终点头；**不必**自己决定下一步该调哪个 skill。

### 方向 B — 用户自己控制（手动）

**适合：** 已熟悉套件、只要查进度、或每一步都想显式下指令。

**入口：** **`/bcc-throughline` 即可**，**不需要**先调 `/bcc-breaking-coding-chaos`。

```text
1. /bcc-throughline           ← 大规划到哪了？建/改 cockpit
2. /bcc-plan-spar <这一片>    ← 对齐、锁 PLAN、自动 review
3. 你：APPROVE implement
4. /bcc-clean-cut             ← 写码 + 验证
5. /bcc-throughline           ← 再看进度、调优先级
6. 回到 2 …
```

| 只想… | 调用 |
|--------|------|
| 看进度 / 改阶段 | 只 `/bcc-throughline` |
| 锁下一片简报 | `/bcc-plan-spar …` |
| PLAN 已点头，开写 | `/bcc-clean-cut` |

### 怎么选

| | **A · Agent 串** | **B · 你控制** |
|--|------------------|----------------|
| 入口 | `/bcc-breaking-coding-chaos` | `/bcc-throughline`（或任意单 skill） |
| 顺序 | Agent 推双环 | 你逐步点 skill |
| 共同点 | 人闸后再 clean-cut；产物在磁盘上 | 相同 |

可混用：开局用 A，后面切片用 B。

---

## 完整示例：多切片 + HITL 介入点

用一个**全局**场景理解工作流（方向 B 逐步调用）：规划 **4** 个 RL 教学案例，本轮只交付 **2** 个；另外两个留在 throughline 地图上。

### 时间线（技能顺序）

```text
bcc-throughline       →  画 4 例地图；本轮只做 01+02
bcc-plan-spar 01      →  锁 PLAN → 自动 review → 你 APPROVE 开写
bcc-clean-cut 01      →  实现 + 验证 → 回写 throughline
bcc-plan-spar 02      →  锁 PLAN → 自动 review（可能 REVISE）→ 你 APPROVE
bcc-clean-cut 02      →  实现 + 验证 → 回写
bcc-throughline       →  01/02 完成；03/04 仍为 pending
```

### HITL 介入表示例（你真正要点头的地方）

自动 review 的 `VERDICT: REVISE / APPROVED` 是 **agent/审阅方**，不是你。  
**你的闸**主要是下表（agent 自改 PLAN 的 REVISE 不算人闸）。

| # | 阶段 | 类型 | 你的决定（示例） |
|---|------|------|------------------|
| 0 | bcc-throughline | 课程/大范围 | 批准 4 例地图；本轮只做 **01+02** |
| 1 | bcc-plan-spar 01 Phase 1 | 锁 PLAN | **LOCK PLAN NOW**（或继续问 / 停） |
| 2 | bcc-plan-spar 01 审完 | 实现闸 | **APPROVE IMPLEMENT** → `bcc-clean-cut`（或改 PLAN / 停） |
| 3 | bcc-plan-spar 02 Phase 1 | 锁 PLAN | **LOCK PLAN NOW** |
| 4 | bcc-plan-spar 02 自动审 | agent REVISE | *非人闸* — builder 改 PLAN（如补安全步数上限） |
| 5 | bcc-plan-spar 02 审完 | 实现闸 | **APPROVE IMPLEMENT** → `bcc-clean-cut` |

**记法：**

| 角色 | 常见动作 |
|------|----------|
| **你** | 定大地图 · 每片锁 PLAN · 是否开写 · 在 throughline 上改优先级 |
| **Agent** | 对齐提问 · 写产物 · 自动 review · REVISE 后改 PLAN · 你点头后 bcc-clean-cut · 回写进度 |

`bcc-clean-cut` **默认无人闸**（除非验证失败要升级问人）。

可选：项目里维护 `HITL_INTERVENTIONS.md` 用同款表做审计。

---

## 示例（短）

**方向 A：** `/bcc-breaking-coding-chaos` 做 Anki CLI → agent 串 throughline → plan-spar → 你 APPROVE → bcc-clean-cut。

**方向 B：** 你依次 `/bcc-throughline` → `/bcc-plan-spar` → APPROVE → `/bcc-clean-cut` → 再 `/bcc-throughline`。

| 你说 | 技能 / 方向 |
|------|-------------|
| 用 BCC 跑我的原型 | A → breaking-coding-chaos |
| 我们到哪了？ | B → throughline |
| plan-spar：支付回调 | B → plan-spar |
| 按 PLAN 实现 | B → bcc-clean-cut |

---

## 适合谁

| 身份 | 为什么用 BCC |
|------|----------------|
| **工程师 / Tech Lead**（生产系统、多模块交付） | 长会话里仍能看见取舍与「做到哪了」 |
| **独立开发者 / 创始人**（用 agent 写产品） | idea 分步落地，避免每轮聊天被 agent 推倒重写 |
| **科研 / 高年级学生**（方法复现、实验、论文级代码） | 硬约束与验收标准落在文件里，不靠模糊记忆 |
| **大仓 / 从零仓库维护者** | 全局地图 + 一次只啃一片；`/clear` 后不易丢线 |
| **已在用 Claude / Codex / Cursor 等的人** | 同一套四个 skill，跨 agent 同一工作流 |

## 适合哪些场景

| 场景 | 适合度 |
|------|--------|
| 多步 / 多周、能拆成若干自然子任务的 endeavor | **很适合** — throughline 管进度条；每片 plan-spar → clean-cut |
| 高难度单片：隐蔽 bug、迁移、必须贴合 brief 的实验 | **很适合** — 锁 PLAN、加压 review、你 APPROVE 再最小实现 |
| `/clear`、压缩上下文、或换 agent 后继续干 | **很适合** — 进度在磁盘文件上 |
| 一句话 vibe、随手脚本 | **不太需要** — 直接聊即可 |
| 还没有具体 idea（只想「随便做个酷的」） | **不适用** — BCC 实现 idea，不替你空想产品 |

---

## 快速开始

仅 **四个** skill：`bcc-breaking-coding-chaos` · `bcc-throughline` · `bcc-plan-spar` · `bcc-clean-cut`。

以 **Claude Code** 与 **Codex** 为主；其他 agent 见文末。

### Claude Code（主）

```bash
# macOS / Linux — 用户级
cp -R skills/bcc-breaking-coding-chaos skills/bcc-throughline \
      skills/bcc-plan-spar skills/bcc-clean-cut ~/.claude/skills/
```

```powershell
# Windows
.\install.ps1 -Dest "$env:USERPROFILE\.claude\skills"
```

| 范围 | 路径 |
|------|------|
| 用户 | `~/.claude/skills/<name>/` |
| 项目 | `.claude/skills/<name>/`（同上四个文件夹拷进仓库） |

新开 Claude Code 会话 → 输入 `/` 确认四个 `bcc-*` → 试 `/bcc-throughline`。  
详情：[claude.md](../docs/install/claude.md)

### Codex（主）

默认**不**装进 Codex（避免技能列表膨胀）；需要时：

```bash
cp -R skills/bcc-breaking-coding-chaos skills/bcc-throughline \
      skills/bcc-plan-spar skills/bcc-clean-cut ~/.codex/skills/
# 常一并：
cp -R … ~/.agents/skills/
```

```powershell
.\install.ps1 -Dest "$env:USERPROFILE\.codex\skills"
.\install.ps1 -Dest "$env:USERPROFILE\.agents\skills"
```

重启 Codex / 新线程 → 技能列表应只有这四个 BCC。  
详情：[codex.md](../docs/install/codex.md)

### 其他（辅）

```powershell
.\install.ps1 -AllAgents
```

```bash
./install.sh --all-agents
```

| Agent | 路径 | 文档 |
|-------|------|------|
| Grok | `~/.grok/skills/` | 默认 `install.ps1` |
| Cursor | `~/.cursor/skills/` | [cursor.md](../docs/install/cursor.md) |
| 其他 | 见矩阵 | [docs/install](../docs/install/README.md) · [INSTALL_FOR_AGENTS.md](../INSTALL_FOR_AGENTS.md) |



## Star History

上下排布的全宽版块见 **[英文 README · Star History](../README.md#star-history)**。图中曲线是**仓库内静态示意**，不是未发布时的实时 star；公开后 GitHub 才记 star，实时曲线点 Live curve。

---

## Contributing

欢迎贡献。请：Fork → 建 feature 分支 → 提 PR。完整说明见 **[英文 README · Contributing](../README.md#contributing)**。

---

License: MIT。