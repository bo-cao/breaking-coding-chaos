# breaking-coding-chaos

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-4-informational)](../skills)
[![Agents](https://img.shields.io/badge/agents-Grok%20%7C%20Claude%20%7C%20Codex%20%7C%20Cursor%20%7C%20OpenCode%20%7C%20Hermes%20%7C%20OpenClaw-success)](../docs/install/README.md)

<p align="center">
  <img src="../assets/banner.jpg" alt="breaking-coding-chaos — dual-loop human-in-the-loop coding with agents" width="100%" />
</p>

**breaking-coding-chaos（BCC）** 是一套面向 coding agent 的 **人在环路（human-in-the-loop）双环控制面 skill 套件**：在 agent 帮你落地 idea 时，你仍能掌控**进度**与**技术细节**——不丢主线。

**适用于所有 agents。** 标准 Agent Skills 目录（`SKILL.md`）——一次安装，可用于 Claude Code、Codex、Grok、Cursor、OpenCode、Hermes、OpenClaw，以及任何支持同一 skill 格式的运行时。

[English](../README.md) | [简体中文](./README.zh-CN.md) | [繁體中文](./README.zh-TW.md)

[快速开始](#快速开始)

> **先有 idea。** 带上一个**还算具体的想法**（做什么、怎样算做成）。  
> BCC 帮你 **1:1 实现** 并掌控进度与细节——**不是**从零空想产品。  
> 没有真实 idea，就没有诚实可写的代码。

---

## 为什么需要控制面

Agent 编程很强——但往往在**最需要精度**的时刻不可靠。

当工作需要**细粒度设计**、**显式取舍**、**可审计进度**时，会话常会变成：

- **记忆崩塌** — `/clear`、压缩或长工具链之后，目标与约束蒸发；agent 重复踩坑、重复问架构。  
- **幻觉式笃定** — 用“看起来合理”填洞：错 API、幽灵模块、碰不到真因的“修复”。  
- **注意力摊薄** — 塞入的“有用全局上下文”越多，越难把模型**全部**注意力放在眼前那一个难题上。

### 长期记忆工具不是同一类问题

业界有大量 **agent 记忆** 产品与库——例如 [mem0](https://github.com/mem0ai/mem0)、[agentmemory](https://github.com/rohitg00/agentmemory)。它们擅长**跨会话召回**、检索与身份/偏好延续。这很有价值。

高强度实现问的是另一类问题。软记忆问“上个月我们定了啥？”；硬实现问“**这一小时**精确写什么、如何证明？” 更多上下文可能帮闲聊；在关键路径上却常**稀释**注意力。连续性工具优化“记得住”；工程控制优化**契约**——清单、验收、以及此刻允许改动的边界。

工作一变难——隐蔽并发 bug、忠实论文的实验、多模块迁移——模糊全局记忆会变成**税**：agent 什么都半记得，什么都不全拥有。你需要**控制面**：整段 endeavor 的持久笔记、**当前**硬切片的一份活简报、写码前加压、再写**最小正确 diff**，并把进度回写到你看得见的地方。

那就是 **breaking-coding-chaos（BCC）**。

---

## 这些想法从哪里来

Agentic coding 已有若干被验证的模式：**磁盘上的上下文**、**写码前对齐**、**最小 diff**。BCC 是把这些线索收成一条双环的 **人在环路控制面**——不是克隆任一项目，也不是下列作者对 BCC 的官方背书。

<p align="center">
  <img src="../assets/prior-art-compose.png" alt="Separate ideas for context, align, and cut — composed into one control loop" width="920" />
</p>

**相关人物与项目：**

- **[Manus](https://manus.im)** — AI agent 公司；其 [context engineering 文章](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) 推广把**文件系统当作持久 agent 上下文**（聊天是 RAM，磁盘是笔记本）。公司与方法曾获广泛行业关注。  
- **[planning-with-files](https://github.com/OthmanAdi/planning-with-files)**（[Othman Adi](https://github.com/OthmanAdi) 等）— 高采用率开源 skill，落地 Manus 式 **plan / progress / findings**，使多步工作在 `/clear` 与上下文丢失后仍可恢复。  
- **[Matt Pocock](https://github.com/mattpocock)** — TypeScript 教育者（[Total TypeScript](https://www.totaltypescript.com/)）；曾任 [XState](https://stately.ai/) 核心成员、[Vercel](https://vercel.com/) Developer Advocate。其开源 [skills](https://github.com/mattpocock/skills)（grill / domain-modeling 风格）强调**写码前的硬问题、共享语言与 ADR**。  
- **[ponytail](https://github.com/DietrichGebert/ponytail)**（[Dietrich Gebert](https://github.com/DietrichGebert)）— 广泛使用的开源 skill，编码“懒”高级工程师的 **YAGNI 阶梯**：最小能工作的改动，停止过度建设。  

<p align="center">
  <strong><em>不是又一层记忆——而是人在环路的控制面。</em></strong>
</p>

<p align="center">
  <em>
  看见整段 endeavor。一次只咬一个硬切片。<br />
  双环、硬顺序：地图 → 对计划加压 → 最小下刀。<br />
  每片一份活简报。进度必须回写。错误步骤不能抢跑。
  </em>
</p>

---

## 工作原理

<p align="center">
  <img src="../assets/architecture.png" alt="Ship your idea with agents — throughline progress, plan-spar one sub-task, clean-cut ships it" width="100%" />
</p>

<p align="center">
  <em>双环。人闸。每片一份活计划。</em>
</p>

**Throughline** 在上层：覆盖你映射的全部子任务的**项目进度条**（A → B → C → D；不是固定模板）。  
其下 **plan-spar** 与 **clean-cut** 协作**当前这一片**——锁住活简报、你 APPROVE、最小交付、回写；进度条前进，下一片再来同一对技能。

### 产物

- **全局（仅 throughline）** — `plans.md`、`progress.md`、`findings.md`：endeavor 到哪了、发生过什么、学到了什么？  
- **当前写码** — 一份活 `PLAN.md`（每 hardpoint 就地更新）：*现在*写什么、如何验证？  
- **支撑** — `CONTEXT.md` 与 `docs/adr/*`：领域用语与难逆决策。  
- **会话（可选）** — `.bcc/session.json`：跨聊天 APPROVE + plan hash，供 clean-cut 预检。

### 流水线（按幕）

0. **地图**（`bcc-throughline`）— 目标、阶段、hardpoint 图；状态与重排优先级。你批准或改地图。  
1. **简报**（`bcc-plan-spar`）— 短问答；锁住唯一活计划（按需 CONTEXT / ADR）。  
2. **加压**（`bcc-plan-spar`）— 对抗式 review（self / subagent / 可选 CLI）；修订计划。你 **APPROVE implement**、修改或停止。  
3. **交付**（`bcc-clean-cut`）— 最小 diff、对照计划验证、**强制回写** throughline。

几条关键规则：

- 自动 review 的 `VERDICT: APPROVED` **≠** 允许写码——只有你的实现闸才算。  
- **一份**活计划文件，不是一堆切片 plan；endeavor 历史在 throughline。  
- **plan-spar 必须在 throughline 之后**（硬预检）。  
- 没有回写的 clean-cut **不算完成**。

### 仅四个 skill

- **`bcc-breaking-coding-chaos`** — 主入口：Mode A 串流程，或短状态 + 下一步。  
- **`bcc-throughline`** — 全局驾驶舱。  
- **`bcc-plan-spar`** — 对齐并 review 当前计划。  
- **`bcc-clean-cut`** — 最小实现 + 回写。

Slash id 用 `bcc-…`。聊天可用 `bcc:…`（各 skill 的 `argument-hint`）。

### 两种用法

| | **Mode A — Agent 串** | **Mode B — 你控制** |
|--|----------------------|---------------------|
| **入口** | `/bcc-breaking-coding-chaos` | `/bcc-throughline` |
| **顺序** | 薄编排器按序加载子 skill | 你**按硬顺序**逐步调用 |
| **适合** | 首次使用、大目标 | 查状态、精细控制 |

同一套四个 skill、同一套文件。可混用。

**Mode B 顺序（必须）：** 始终 **throughline → plan-spar →（你 APPROVE）→ clean-cut → 回写 throughline**。  
你决定*何时*调用，但**不能**跳过地图、在 throughline 前 plan-spar、或在未 APPROVE 时写码。一片交付后回到 throughline，再对下一片 plan-spar。

### 如何调用

不必每次手写整套双环仪式。按宿主能力选择：

1. **显式 call skill**（推荐）— slash 或 skills UI，如 `/bcc-throughline`、`/bcc-plan-spar`、`/bcc-clean-cut`、`/bcc-breaking-coding-chaos`。  
2. **自然语言** — 许多 agent 会在 prompt **匹配 skill 描述**时自动加载，如「跑 throughline」「plan-spar 这一片」「clean-cut 实现计划」。  

**前提：** agent 必须**能索引 skill 且允许调用**。自动路由弱、关闭或未安装时，请**自己点名 skill**（slash / UI /「用 skill bcc-…」）。不要假设每个聊天宿主都会在没有 skill 的情况下发明双环。

---

## 适合谁

BCC 面向需要 agent 在**硬约束下真正做完事**的人——不只是生成“看起来像”的代码。同一双环对不同角色各有用处：

- **研究人员与学生** — 把协议、超参与验收钉进活简报；多周论文/仓库进度落盘；一次一片可验证实验或流水线。  
- **工程师与 Tech Lead** — 长会话里看见取舍与“做到哪了”；一份当前简报，避免三套并行实现。  
- **独立开发者与创始人** — 把具体产品 idea 拆成可审计子任务；阻止 agent 每轮重写产品。  
- **仓库维护者** — 全局地图 + 一次一个硬切片；压缩/失忆/换工具后更少空转。  
- **多 agent 用户**（Claude / Codex / Cursor / …）— 同一四 skill、同一双环，跨运行时一套控制面。

**很适合：** 多步/多周工作；高风险切片（bug、迁移、必须贴 brief 的实验）；`/clear` 或换 agent 后继续。  
**弱/用错：** 一句话 vibe、随手脚本、或还没有具体 idea——BCC 实现 idea，不替你空想产品。

---

## 完整示例：多切片 + 人在环路

规划 **4** 个 case；本会话只交付 **2** 个。

```text
bcc-throughline          →  映射 01–04；本会话只交付 01+02
bcc-plan-spar 01         →  锁 PLAN → review → 你批准实现
bcc-clean-cut 01         →  写码 + 验证 → 回写
bcc-plan-spar 02         →  锁 PLAN → review（可能 REVISE）→ 你批准
bcc-clean-cut 02         →  写码 + 验证 → 回写
bcc-throughline          →  01/02 完成；03/04 仍待办
```

你掌握闸门：地图范围、锁 PLAN、实现 APPROVE、重排优先级。  
Agent 负责提问、产物、review、APPROVE 后下刀与回写。

---

## 快速开始

仅 **四个** skill（不多一个）：  
`bcc-breaking-coding-chaos` · `bcc-throughline` · `bcc-plan-spar` · `bcc-clean-cut`

以 **Claude Code** 与 **Codex** 为主；其他 agent 见后。

### Claude Code（主）

**1. 用户级 skill**（推荐）：

```bash
# 仓库根目录 — macOS / Linux
cp -R skills/bcc-breaking-coding-chaos \
      skills/bcc-throughline \
      skills/bcc-plan-spar \
      skills/bcc-clean-cut \
      ~/.claude/skills/
```

```powershell
# Windows
.\install.ps1 -Dest "$env:USERPROFILE\.claude\skills"
```

**2. 或项目级 skill**（团队/仓库内）：`.claude/skills/<name>/SKILL.md` — 同样四个文件夹。

用户级路径：`~/.claude/skills/<name>/SKILL.md`。

**3. 使用**

1. 打开**新** Claude Code 会话（启动时重新索引 skill）。  
2. 输入 `/` — 确认四个 `bcc-*`。  
3. 试 `/bcc-throughline` 或 `/bcc-breaking-coding-chaos`。

完整说明：[claude.md](../docs/install/claude.md)。  
仓库公开后：`npx skills add JC/breaking-coding-chaos -y`。

### Codex（主）

Codex 为**可选安装**（保持全局 skill 列表精简）。

```bash
# 仓库根目录 — macOS / Linux
cp -R skills/bcc-breaking-coding-chaos \
      skills/bcc-throughline \
      skills/bcc-plan-spar \
      skills/bcc-clean-cut \
      ~/.codex/skills/

# 许多 Codex 环境也会读：
cp -R skills/bcc-breaking-coding-chaos \
      skills/bcc-throughline \
      skills/bcc-plan-spar \
      skills/bcc-clean-cut \
      ~/.agents/skills/
```

```powershell
# Windows
.\install.ps1 -Dest "$env:USERPROFILE\.codex\skills"
.\install.ps1 -Dest "$env:USERPROFILE\.agents\skills"
```

Codex 主路径：`~/.codex/skills/`。共享 agents 路径（常一并扫描）：`~/.agents/skills/`。

然后重启 Codex 或开**新线程**，确认只有这四个 BCC 文件夹，从 UI 或自然语言调用。

完整说明：[codex.md](../docs/install/codex.md)。

### 其他（辅）

```powershell
.\install.ps1 -AllAgents
```

```bash
./install.sh --all-agents
```

- **Grok** — `~/.grok/skills/` · [grok.md](../docs/install/grok.md) · `install.ps1` 默认  
- **Cursor** — `~/.cursor/skills/` · [cursor.md](../docs/install/cursor.md)  
- **OpenCode** — `~/.config/opencode/skills/` · [opencode.md](../docs/install/opencode.md)  
- **Hermes** — `~/.hermes/skills/` · [hermes.md](../docs/install/hermes.md)  
- **OpenClaw** — `~/.openclaw/skills/` · [openclaw.md](../docs/install/openclaw.md)  

粘贴块：[INSTALL_FOR_AGENTS.md](../INSTALL_FOR_AGENTS.md) · 完整矩阵：[docs/install/README.md](../docs/install/README.md)

**验证（任意 agent）：** 新会话 → 列出 skill → 仅四个 `bcc-*`。

---

## 产物

- **throughline** 拥有 `plans.md`、`progress.md`、`findings.md`  
- **plan-spar** 拥有 `CONTEXT.md` 与 `docs/adr/*`  
- **plan-spar + clean-cut** 共享一份活 `PLAN.md`  
- **可选** `.bcc/session.json` 用于 APPROVE / 预检  

---

## 评测

[![Clean pass](https://img.shields.io/badge/Clean_pass-90%25-brightgreen)](../benchmark/RESULTS.md)
[![Final pass](https://img.shields.io/badge/Final_pass-100%25-success)](../benchmark/RESULTS.md)
[![Tasks](https://img.shields.io/badge/Tasks-20-blue)](../benchmark/tasks/)

我们在 **20** 个带 **pytest oracle** 的 Python 任务上，对比了 **BCC** 与 **ad-hoc** agent 用法。

**ad-hoc** 指日常 **case by case** 驱动 agent：想到需求就写 prompt 让 agent 解决——**没有**显式分层计划（无全局进度图、无每片唯一活简报、无纪律性的实现闸）。

| Metric | **BCC** | **ad-hoc** |
|--------|---------|------------|
| **Clean pass** (first full oracle green) | **90%** (18/20) | **0%** (0/20) |
| **Final pass** (within rework budget) | **100%** (20/20) | **0%** (0/20) |
| Mean failed oracle rounds | **0.10** | **2.00** |
| Mean tokens | **2.0M** | **5.1M (~2.5×)** |

双环控制面下，agent 多数在**首次 oracle 全绿**即收口，并在预算内**完成全部任务**。Ad-hoc 短 demand（优化下一句聊天而非完整规格闭环）在**首红后仅允许一次返工**时**达不到 final green**。Ad-hoc token 约 **2.5×**，与反复 fail/fix 一致。

任务包与明细表：[`benchmark/`](../benchmark/) · 摘要：[`benchmark/RESULTS.md`](../benchmark/RESULTS.md)。

> **PS.** 本评测中，**人在环路决策（含实现 APPROVE）由 agent 子代理**按固定策略执行，而非真人坐镇。结果反映的是 **BCC 工作流 + 自动闸策略**。

---

## 致谢

本 skill 套件**参考了**下列项目中的相关思想（以自有 skill 名重新封装）。我们与下列作者/组织**无隶属关系**——感谢先前工作。

- [planning-with-files](https://github.com/OthmanAdi/planning-with-files) — Manus 式持久 markdown 规划（throughline）
- [Manus context engineering](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) — 文件系统作为持久 agent 上下文
- [Matt Pocock skills](https://github.com/mattpocock/skills) — grill / grill-with-docs 与领域建模（plan-spar）
- [ponytail](https://github.com/DietrichGebert/ponytail) — YAGNI / 最小实现阶梯（clean-cut）

---

## Star History

<p align="center">
  <sub>SIGNAL</sub><br />
  <strong>若 BCC 帮你交付过 — 请点一颗 star</strong><br />
  <sub>不是虚荣指标——是给下一个需要控制面的人留的面包屑。</sub>
</p>

<p align="center">
  <img src="../assets/star-history.svg" alt="Star trajectory (illustrative until the repo is public)" width="100%" />
</p>

<p align="center">
  <sub>此曲线为仓库内<strong>静态示意</strong>——非实时 GitHub 数据。公开后 star 由 GitHub 记录；实时数字见下方链接。</sub>
</p>

<p align="center">
  <a href="https://github.com/JC/breaking-coding-chaos"><strong>★&nbsp; Star this repo</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/JC/breaking-coding-chaos/stargazers">Stargazers</a>
  &nbsp;·&nbsp;
  <a href="https://www.star-history.com/#JC/breaking-coding-chaos&Date">Live curve</a>
</p>

---

## 贡献

欢迎贡献：

1. **Fork** 本仓库  
2. **创建 feature 分支**（`git checkout -b feature/your-change`）  
3. **提交**清晰说明  
4. 向 `master` 开 **pull request**  

改 skill 行为时：保持套件精简（**仅四个 skill**）、throughline → plan-spar → clean-cut 顺序与人闸，并在用户可见文案变更时同步 EN + 简中 + 繁中文档。

---

## 许可

MIT — 见 [LICENSE](../LICENSE)。

Copyright (c) 2026 JC.
