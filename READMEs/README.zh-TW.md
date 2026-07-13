# breaking-coding-chaos

**breaking-coding-chaos（BCC）** 是一套 **人在迴路（human-in-the-loop）的雙環控制面 Agent Skill**：在用 coding agent 落地 idea 時，幫你掌控**進度**與**技術細節**，分步交付、不丟主線。

**適用於所有 agents。** 標準 Agent Skills 目錄（`SKILL.md`），可裝到 Claude Code、Codex、Grok、Cursor、OpenCode、Hermes、OpenClaw，以及任何支援同一 skill 格式的執行環境。

[English](../README.md) | [简体中文](./README.zh-CN.md) | [繁體中文](./README.zh-TW.md)

動機說明、How it works 架構圖與致謝見 **[英文 README](../README.md)**。

**前提：** 需要一個**還算完善的 idea**。本 skill 幫你 **1:1 實作** 並掌控進度/細節，**不是**從零空想產品。

1. **bcc-throughline** — 全域三檔  
2. **bcc-plan-spar** — **必須在 throughline 之後**；**唯一** `PLAN.md` 就地更新  
3. **bcc-clean-cut** — 最小實作 + 驗證 + **強制回寫** throughline  

**命名：** slash `bcc-`；聊天可用 `bcc:`。  
**結構：** 僅 **1 主 + 3 子** skill。狀態內嵌主 skill。  
**安裝：** `.\install.ps1`（預設只裝 Grok）。

---

## Skills（僅 4 個）

| Skill | 職責 |
|-------|------|
| `bcc-breaking-coding-chaos` | **主**：Mode A 或短狀態 |
| `bcc-throughline` | 全域三檔 |
| `bcc-plan-spar` | throughline 之後；唯一 PLAN |
| `bcc-clean-cut` | 寫碼 + 強制回寫 |

```text
bcc-throughline → plan-spar（APPROVE）→ bcc-clean-cut → 回寫 throughline
```

**命名：** plan-spar = 搞計畫；clean-cut = 乾淨下刀寫碼（對應 ponytail）。

**`bcc-breaking-coding-chaos` 不是必經入口**——可以直接 `/bcc-throughline` 起步。見下方兩種用法。

---

## 兩種使用方向

同一套四個 skill、同一套產物檔；差別在於**誰驅動步驟順序**。

### 方向 A — Agent 自己串（編排）

**適合：** 第一次用 BCC、目標較大、不想記命令順序。

**入口：** `/bcc-breaking-coding-chaos`（或：「用 BCC 做某某」）

```text
你 → /bcc-breaking-coding-chaos
      → throughline（大地圖 / 進度 / 調整）
      → plan-spar（對齊 → 鎖 PLAN → 自動 review）
      → 你 APPROVE 再寫
      → bcc-clean-cut（最小實作 + 驗證 + 回寫）
      → throughline（看進度；下一片或停）
```

你仍要回答對齊問題、最終點頭；**不必**自己決定下一步該調哪個 skill。

### 方向 B — 使用者自己控制（手動）

**適合：** 已熟悉套件、只要查進度、或每一步都想顯式下指令。

**入口：** **`/bcc-throughline` 即可**，**不需要**先調 `/bcc-breaking-coding-chaos`。

```text
1. /bcc-throughline           ← 大規劃到哪了？建/改 cockpit
2. /bcc-plan-spar <這一片>    ← 對齊、鎖 PLAN、自動 review
3. 你：APPROVE implement
4. /bcc-clean-cut             ← 寫碼 + 驗證
5. /bcc-throughline           ← 再看進度、調優先級
6. 回到 2 …
```

| 只想… | 呼叫 |
|--------|------|
| 看進度 / 改階段 | 只 `/bcc-throughline` |
| 鎖下一片簡報 | `/bcc-plan-spar …` |
| PLAN 已點頭，開寫 | `/bcc-clean-cut` |

### 怎麼選

| | **A · Agent 串** | **B · 你控制** |
|--|------------------|----------------|
| 入口 | `/bcc-breaking-coding-chaos` | `/bcc-throughline`（或任意單 skill） |
| 順序 | Agent 推雙環 | 你逐步點 skill |
| 共同點 | 人閘後再 clean-cut；產物在磁碟上 | 相同 |

可混用：開局用 A，後面切片用 B。

---

## 完整示例：多切片 + HITL 介入點

用一個**全域**場景理解工作流（方向 B 逐步呼叫）：規劃 **4** 個 RL 教學案例，本輪只交付 **2** 個；另外兩個留在 throughline 地圖上。

### 時間線（技能順序）

```text
bcc-throughline       →  畫 4 例地圖；本輪只做 01+02
bcc-plan-spar 01      →  鎖 PLAN → 自動 review → 你 APPROVE 開寫
bcc-clean-cut 01      →  實作 + 驗證 → 回寫 throughline
bcc-plan-spar 02      →  鎖 PLAN → 自動 review（可能 REVISE）→ 你 APPROVE
bcc-clean-cut 02      →  實作 + 驗證 → 回寫
bcc-throughline       →  01/02 完成；03/04 仍為 pending
```

### HITL 介入表示例（你真正要點頭的地方）

自動 review 的 `VERDICT: REVISE / APPROVED` 是 **agent/審閱方**，不是你。  
**你的閘**主要是下表（agent 自改 PLAN 的 REVISE 不算人閘）。

| # | 階段 | 類型 | 你的決定（示例） |
|---|------|------|------------------|
| 0 | bcc-throughline | 課程/大範圍 | 批准 4 例地圖；本輪只做 **01+02** |
| 1 | bcc-plan-spar 01 Phase 1 | 鎖 PLAN | **LOCK PLAN NOW**（或繼續問 / 停） |
| 2 | bcc-plan-spar 01 審完 | 實作閘 | **APPROVE IMPLEMENT** → `bcc-clean-cut`（或改 PLAN / 停） |
| 3 | bcc-plan-spar 02 Phase 1 | 鎖 PLAN | **LOCK PLAN NOW** |
| 4 | bcc-plan-spar 02 自動審 | agent REVISE | *非人閘* — builder 改 PLAN（如補安全步數上限） |
| 5 | bcc-plan-spar 02 審完 | 實作閘 | **APPROVE IMPLEMENT** → `bcc-clean-cut` |

**記法：**

| 角色 | 常見動作 |
|------|----------|
| **你** | 定大地圖 · 每片鎖 PLAN · 是否開寫 · 在 throughline 上改優先級 |
| **Agent** | 對齊提問 · 寫產物 · 自動 review · REVISE 後改 PLAN · 你點頭後 bcc-clean-cut · 回寫進度 |

`bcc-clean-cut` **預設無人閘**（除非驗證失敗要升級問人）。

可選：專案裡維護 `HITL_INTERVENTIONS.md` 用同款表做審計。

---

## 示例（短）

**方向 A：** `/bcc-breaking-coding-chaos` 做 Anki CLI → agent 串 throughline → plan-spar → 你 APPROVE → bcc-clean-cut。

**方向 B：** 你依次 `/bcc-throughline` → `/bcc-plan-spar` → APPROVE → `/bcc-clean-cut` → 再 `/bcc-throughline`。

| 你說 | 技能 / 方向 |
|------|-------------|
| 用 BCC 跑我的原型 | A → breaking-coding-chaos |
| 我們到哪了？ | B → throughline |
| plan-spar：支付回呼 | B → plan-spar |
| 按 PLAN 實作 | B → bcc-clean-cut |

---

## 適合誰

| 身分 | 為什麼用 BCC |
|------|----------------|
| **工程師 / Tech Lead**（生產系統、多模組交付） | 長會話裡仍能看見取捨與「做到哪了」 |
| **獨立開發者 / 創辦人**（用 agent 寫產品） | idea 分步落地，避免每輪聊天被 agent 推倒重寫 |
| **科研 / 高年級學生**（方法復現、實驗、論文級程式） | 硬約束與驗收落在檔案裡，不靠模糊記憶 |
| **大倉 / 從零倉庫維護者** | 全域地圖 + 一次只啃一片；`/clear` 後不易丟線 |
| **已在用 Claude / Codex / Cursor 等的人** | 同一套四個 skill，跨 agent 同一工作流 |

## 適合哪些場景

| 場景 | 適合度 |
|------|--------|
| 多步 / 多週、能拆成若干自然子任務的 endeavor | **很適合** — throughline 管進度條；每片 plan-spar → clean-cut |
| 高難度單片：隱蔽 bug、遷移、必須貼合 brief 的實驗 | **很適合** — 鎖 PLAN、加壓 review、你 APPROVE 再最小實作 |
| `/clear`、壓縮上下文、或換 agent 後繼續做 | **很適合** — 進度在磁碟檔案上 |
| 一句話 vibe、隨手腳本 | **不太需要** — 直接聊即可 |
| 還沒有具體 idea（只想「隨便做個酷的」） | **不適用** — BCC 實作 idea，不替你空想產品 |

---

## 快速開始

僅 **四個** skill：`bcc-breaking-coding-chaos` · `bcc-throughline` · `bcc-plan-spar` · `bcc-clean-cut`。

以 **Claude Code** 與 **Codex** 為主；其他 agent 見文末。

### Claude Code（主）

```bash
# macOS / Linux — 使用者級
cp -R skills/bcc-breaking-coding-chaos skills/bcc-throughline \
      skills/bcc-plan-spar skills/bcc-clean-cut ~/.claude/skills/
```

```powershell
# Windows
.\install.ps1 -Dest "$env:USERPROFILE\.claude\skills"
```

| 範圍 | 路徑 |
|------|------|
| 使用者 | `~/.claude/skills/<name>/` |
| 專案 | `.claude/skills/<name>/`（同上四個資料夾拷進倉庫） |

新開 Claude Code 工作階段 → 輸入 `/` 確認四個 `bcc-*` → 試 `/bcc-throughline`。  
詳情：[claude.md](../docs/install/claude.md)

### Codex（主）

預設**不**裝進 Codex（避免技能列表膨脹）；需要時：

```bash
cp -R skills/bcc-breaking-coding-chaos skills/bcc-throughline \
      skills/bcc-plan-spar skills/bcc-clean-cut ~/.codex/skills/
# 常一併：
cp -R … ~/.agents/skills/
```

```powershell
.\install.ps1 -Dest "$env:USERPROFILE\.codex\skills"
.\install.ps1 -Dest "$env:USERPROFILE\.agents\skills"
```

重啟 Codex / 新執行緒 → 技能列表應只有這四個 BCC。  
詳情：[codex.md](../docs/install/codex.md)

### 其他（輔）

```powershell
.\install.ps1 -AllAgents
```

```bash
./install.sh --all-agents
```

| Agent | 路徑 | 文件 |
|-------|------|------|
| Grok | `~/.grok/skills/` | 預設 `install.ps1` |
| Cursor | `~/.cursor/skills/` | [cursor.md](../docs/install/cursor.md) |
| 其他 | 見矩陣 | [docs/install](../docs/install/README.md) · [INSTALL_FOR_AGENTS.md](../INSTALL_FOR_AGENTS.md) |



## Star History

上下排布的全寬版塊見 **[英文 README · Star History](../README.md#star-history)**。圖中曲線是**倉庫內靜態示意**，不是未發布時的即時 star；公開後 GitHub 才記 star，即時曲線點 Live curve。

---

## Contributing

歡迎貢獻。請：Fork → 建 feature 分支 → 提 PR。完整說明見 **[英文 README · Contributing](../README.md#contributing)**。

---

License: MIT。