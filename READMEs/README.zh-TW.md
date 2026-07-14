# breaking-coding-chaos

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-4-informational)](../skills)
[![Agents](https://img.shields.io/badge/agents-Grok%20%7C%20Claude%20%7C%20Codex%20%7C%20Cursor%20%7C%20OpenCode%20%7C%20Hermes%20%7C%20OpenClaw-success)](../docs/install/README.md)

<p align="center">
  <img src="../assets/banner.jpg" alt="breaking-coding-chaos — dual-loop human-in-the-loop coding with agents" width="100%" />
</p>

**breaking-coding-chaos（BCC）** 是一套面向 coding agent 的 **人在迴路（human-in-the-loop）雙環控制面 skill 套件**：在 agent 幫你落地 idea 時，你仍能掌控**進度**與**技術細節**——不丟主線。

**適用於所有 agents。** 標準 Agent Skills 目錄（`SKILL.md`）——一次安裝，可用於 Claude Code、Codex、Grok、Cursor、OpenCode、Hermes、OpenClaw，以及任何支援同一 skill 格式的執行環境。

[English](../README.md) | [简体中文](./README.zh-CN.md) | [繁體中文](./README.zh-TW.md)

[快速開始](#快速開始)

> **先有 idea。** 帶上一個**還算具體的想法**（做什麼、怎樣算做成）。  
> BCC 幫你 **1:1 實作** 並掌控進度與細節——**不是**從零空想產品。  
> 沒有真實 idea，就沒有誠實可寫的程式。

---

## 為什麼需要控制面

Agent 編程很強——但往往在**最需要精度**的時刻不可靠。

當工作需要**細粒度設計**、**顯式取捨**、**可稽核進度**時，會話常會變成：

- **記憶崩塌** — `/clear`、壓縮或長工具鏈之後，目標與約束蒸發；agent 重複踩坑、重複問架構。  
- **幻覺式篤定** — 用「看起來合理」填洞：錯 API、幽靈模組、碰不到真因的「修復」。  
- **注意力攤薄** — 塞入的「有用全域上下文」越多，越難把模型**全部**注意力放在眼前那一個難題上。

### 長期記憶工具不是同一類問題

業界有大量 **agent 記憶** 產品與庫——例如 [mem0](https://github.com/mem0ai/mem0)、[agentmemory](https://github.com/rohitg00/agentmemory)。它們擅長**跨會話召回**、檢索與身分/偏好延續。這很有價值。

高強度實作問的是另一類問題。軟記憶問「上個月我們定了什麼？」；硬實作問「**這一小時**精確寫什麼、如何證明？」 更多上下文可能幫閒聊；在關鍵路徑上卻常**稀釋**注意力。連續性工具最佳化「記得住」；工程控制最佳化**契約**——清單、驗收、以及此刻允許改動的邊界。

工作一變難——隱蔽並行 bug、忠實論文的實驗、多模組遷移——模糊全域記憶會變成**稅**：agent 什麼都半記得，什麼都不全擁有。你需要**控制面**：整段 endeavor 的持久筆記、**當前**硬切片的一份活簡報、寫碼前加壓、再寫**最小正確 diff**，並把進度回寫到你看得見的地方。

那就是 **breaking-coding-chaos（BCC）**。

---

## 這些想法從哪裡來

Agentic coding 已有若干被驗證的模式：**磁碟上的上下文**、**寫碼前對齊**、**最小 diff**。BCC 是把這些線索收成一條雙環的 **人在迴路控制面**——不是克隆任一專案，也不是下列作者對 BCC 的官方背書。

<p align="center">
  <img src="../assets/prior-art-compose.png" alt="Separate ideas for context, align, and cut — composed into one control loop" width="920" />
</p>

**相關人物與專案：**

- **[Manus](https://manus.im)** — AI agent 公司；其 [context engineering 文章](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) 推廣把**檔案系統當作持久 agent 上下文**（聊天是 RAM，磁碟是筆記本）。公司與方法曾獲廣泛產業關注。  
- **[planning-with-files](https://github.com/OthmanAdi/planning-with-files)**（[Othman Adi](https://github.com/OthmanAdi) 等）— 高採用率開源 skill，落地 Manus 式 **plan / progress / findings**，使多步工作在 `/clear` 與上下文遺失後仍可恢復。  
- **[Matt Pocock](https://github.com/mattpocock)** — TypeScript 教育者（[Total TypeScript](https://www.totaltypescript.com/)）；曾任 [XState](https://stately.ai/) 核心成員、[Vercel](https://vercel.com/) Developer Advocate。其開源 [skills](https://github.com/mattpocock/skills)（grill / domain-modeling 風格）強調**寫碼前的硬問題、共享語言與 ADR**。  
- **[ponytail](https://github.com/DietrichGebert/ponytail)**（[Dietrich Gebert](https://github.com/DietrichGebert)）— 廣泛使用的開源 skill，編碼「懶」高階工程師的 **YAGNI 階梯**：最小能工作的改動，停止過度建設。  

<p align="center">
  <strong><em>不是又一層記憶——而是人在迴路的控制面。</em></strong>
</p>

<p align="center">
  <em>
  看見整段 endeavor。一次只咬一個硬切片。<br />
  雙環、硬順序：地圖 → 對計畫加壓 → 最小下刀。<br />
  每片一份活簡報。進度必須回寫。錯誤步驟不能搶跑。
  </em>
</p>

---

## 工作原理

<p align="center">
  <img src="../assets/architecture.png" alt="Ship your idea with agents — throughline progress, plan-spar one sub-task, clean-cut ships it" width="100%" />
</p>

<p align="center">
  <em>雙環。人閘。每片一份活計畫。</em>
</p>

**Throughline** 在上層：覆蓋你對應的全部子任務的**專案進度條**（A → B → C → D；不是固定模板）。  
其下 **plan-spar** 與 **clean-cut** 協作**當前這一片**——鎖住活簡報、你 APPROVE、最小交付、回寫；進度條前進，下一片再來同一對技能。

### 產物

- **全域（僅 throughline）** — `plans.md`、`progress.md`、`findings.md`：endeavor 到哪了、發生過什麼、學到了什麼？  
- **當前寫碼** — 一份活 `PLAN.md`（每 hardpoint 就地更新）：*現在*寫什麼、如何驗證？  
- **支撐** — `CONTEXT.md` 與 `docs/adr/*`：領域用語與難逆決策。  
- **會話（可選）** — `.bcc/session.json`：跨聊天 APPROVE + plan hash，供 clean-cut 預檢。

### 怎麼用

兩種模式**同一條流水線**：throughline → plan-spar → **你 APPROVE** → clean-cut → 回寫。

| 模式 | 入口 | 說明 |
|------|------|------|
| **A — 一體化** | `/bcc-breaking-coding-chaos` | 一條命令，agent 串完整條流水線 |
| **B — 分步** | 從 `/bcc-throughline` 進入 | 你自己按步呼叫：throughline → plan-spar → clean-cut |

| 命令 | 用途 | 參數 |
|------|------|------|
| `/bcc-breaking-coding-chaos` | Mode A，或查狀態 | 目標 · `status` · 可選 `rounds=N` `review=…` |
| `/bcc-throughline` | Mode B 入口：主線 / 重排 / 恢復 | idea 或「到哪了」 |
| `/bcc-plan-spar` | 對齊、鎖 `PLAN.md`、review | **`rounds=N`** review 上限（預設 `3`，`0`=跳過）· `review=auto\|self\|subagent\|cli\|off` |
| `/bcc-clean-cut` | 你 APPROVE 後寫碼 | `lite` · `full` · `ultra` |

- plan-spar 問答：夠清楚就停（或你鎖/stop）。無預設提問次數。  
- `rounds`：只限鎖 PLAN 後的 **review**。

**Mode A**

```text
/bcc-breaking-coding-chaos 實作某某功能
/bcc-breaking-coding-chaos status
```

**Mode B**

```text
/bcc-throughline
/bcc-plan-spar HP1 rounds=3
# 你 APPROVE implement
/bcc-clean-cut
/bcc-plan-spar hotfix rounds=0 review=off
```

### 示例（Mode B — 本會話交付 4 片中的 2 片）

```text
/bcc-throughline              → 對應 01–04
/bcc-plan-spar 01 rounds=3    → 鎖 PLAN → review ≤3 → 你批准
/bcc-clean-cut                → 寫碼 + 驗證 → 回寫
/bcc-plan-spar 02 rounds=3
/bcc-clean-cut
/bcc-throughline              → 01/02 完成；03/04 待辦
```

---

## 快速開始

僅 **四個** skill（不多一個）：  
`bcc-breaking-coding-chaos` · `bcc-throughline` · `bcc-plan-spar` · `bcc-clean-cut`

### 一行安裝（推薦）

開放 [Agent Skills](https://agentskills.io) CLI — 一條命令覆蓋 Claude Code、Codex、Cursor、OpenCode、Hermes、OpenClaw 等：

```bash
npx skills add bo-cao/breaking-coding-chaos -g -y
```

只裝你用的 agent：

```bash
npx skills add bo-cao/breaking-coding-chaos -g -y \
  -a claude-code -a codex -a cursor -a opencode -a hermes-agent -a openclaw
```

然後在各 agent 開**新會話** → 確認只有四個 `bcc-*`。

### Claude Code（官方外掛）

```text
/plugin marketplace add bo-cao/breaking-coding-chaos
/plugin install bcc@breaking-coding-chaos
```

CLI：`claude plugin marketplace add bo-cao/breaking-coding-chaos` 然後 `claude plugin install bcc@breaking-coding-chaos`。  
說明：[claude.md](../docs/install/claude.md)

### Codex

```bash
npx skills add bo-cao/breaking-coding-chaos -g -y -a codex
```

安裝到 `~/.codex/skills/`。重啟 Codex / 新執行緒。說明：[codex.md](../docs/install/codex.md)

### Cursor · OpenCode · Hermes · OpenClaw

```bash
npx skills add bo-cao/breaking-coding-chaos -g -y -a cursor
npx skills add bo-cao/breaking-coding-chaos -g -y -a opencode
npx skills add bo-cao/breaking-coding-chaos -g -y -a hermes-agent
npx skills add bo-cao/breaking-coding-chaos -g -y -a openclaw
```

說明：[cursor](../docs/install/cursor.md) · [opencode](../docs/install/opencode.md) · [hermes](../docs/install/hermes.md) · [openclaw](../docs/install/openclaw.md)

### Grok / 離線 / 本機 clone

```powershell
.\install.ps1                 # ~/.grok/skills
.\install.ps1 -AllAgents      # 本機所有已知 agent 路徑
.\install.ps1 -Dest PATH      # 自訂 skills 根目錄
```

```bash
./install.sh
./install.sh --all-agents
DEST=~/.claude/skills ./install.sh
```

說明：[grok.md](../docs/install/grok.md)

貼上區塊：[INSTALL_FOR_AGENTS.md](../INSTALL_FOR_AGENTS.md) · 完整矩陣：[docs/install/README.md](../docs/install/README.md)

**驗證（任意 agent）：** 新會話 → 列出 skill → 僅四個 `bcc-*`。

---

## 產物

- **throughline** 擁有 `plans.md`、`progress.md`、`findings.md`  
- **plan-spar** 擁有 `CONTEXT.md` 與 `docs/adr/*`  
- **plan-spar + clean-cut** 共享一份活 `PLAN.md`  
- **可選** `.bcc/session.json` 用於 APPROVE / 預檢  

---

## 評測

[![Clean pass](https://img.shields.io/badge/Clean_pass-90%25-brightgreen)](../benchmark/RESULTS.md)
[![Final pass](https://img.shields.io/badge/Final_pass-100%25-success)](../benchmark/RESULTS.md)
[![Tasks](https://img.shields.io/badge/Tasks-20-blue)](../benchmark/tasks/)

我們在 **20** 個帶 **pytest oracle** 的 Python 任務上，對比了 **BCC** 與 **ad-hoc** agent 用法。

**ad-hoc** 指日常 **case by case** 驅動 agent：想到需求就寫 prompt 讓 agent 解決——**沒有**顯式分層計畫（無全域進度圖、無每片唯一活簡報、無紀律性的實作閘）。

| Metric | **BCC** | **ad-hoc** |
|--------|---------|------------|
| **Clean pass** (first full oracle green) | **90%** (18/20) | **0%** (0/20) |
| **Final pass** (within rework budget) | **100%** (20/20) | **0%** (0/20) |
| Mean failed oracle rounds | **0.10** | **2.00** |
| Mean tokens | **2.0M** | **5.1M (~2.5×)** |

雙環控制面下，agent 多數在**首次 oracle 全綠**即收口，並在預算內**完成全部任務**。Ad-hoc 短 demand（最佳化下一句聊天而非完整規格閉環）在**首紅後僅允許一次返工**時**達不到 final green**。Ad-hoc token 約 **2.5×**，與反覆 fail/fix 一致。

任務包與明細表：[`benchmark/`](../benchmark/) · 摘要：[`benchmark/RESULTS.md`](../benchmark/RESULTS.md)。

> **PS.** 本評測中，**人在迴路決策（含實作 APPROVE）由 agent 子代理**按固定策略執行，而非真人坐鎮。結果反映的是 **BCC 工作流 + 自動閘策略**。

---

## 致謝

本 skill 套件**參考了**下列專案中的相關思想（以自有 skill 名重新封裝）。我們與下列作者/組織**無隸屬關係**——感謝先前工作。

- [planning-with-files](https://github.com/OthmanAdi/planning-with-files) — Manus 式持久 markdown 規劃（throughline）
- [Manus context engineering](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) — 檔案系統作為持久 agent 上下文
- [Matt Pocock skills](https://github.com/mattpocock/skills) — grill / grill-with-docs 與領域建模（plan-spar）
- [ponytail](https://github.com/DietrichGebert/ponytail) — YAGNI / 最小實作階梯（clean-cut）

---

## Star History

<p align="center">
  <sub>SIGNAL</sub><br />
  <strong>若 BCC 幫你交付過 — 請點一顆 star</strong><br />
  <sub>不是虛榮指標——是給下一個需要控制面的人留的麵包屑。</sub>
</p>

<p align="center">
  <a href="https://www.star-history.com/#bo-cao/breaking-coding-chaos&Date">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="../assets/star-history-dark.svg?v=2" />
      <source media="(prefers-color-scheme: light)" srcset="../assets/star-history-light.svg?v=2" />
      <img alt="Star History Chart" src="../assets/star-history-light.svg?v=2" width="100%" />
    </picture>
  </a>
</p>

<p align="center">
  <a href="https://github.com/bo-cao/breaking-coding-chaos"><strong>★&nbsp; Star this repo</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/bo-cao/breaking-coding-chaos/stargazers">Stargazers</a>
  &nbsp;·&nbsp;
  <a href="https://www.star-history.com/#bo-cao/breaking-coding-chaos&Date">star-history.com</a>
</p>

---

## 貢獻

歡迎貢獻：

1. **Fork** 本倉庫  
2. **建立 feature 分支**（`git checkout -b feature/your-change`）  
3. **提交**清晰說明  
4. 向 `master` 開 **pull request**  

改 skill 行為時：保持套件精簡（**僅四個 skill**）、throughline → plan-spar → clean-cut 順序與人閘，並在使用者可見文案變更時同步 EN + 簡中 + 繁中文件。

---

## 授權

MIT — 見 [LICENSE](../LICENSE)。

Copyright (c) 2026 JC.
