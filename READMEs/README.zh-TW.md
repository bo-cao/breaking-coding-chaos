# breaking-coding-chaos

**人在迴路 Agent Skill 套件：分步交付，不丟進度與掌控。**

[English](../README.md) | [简体中文](./README.zh-CN.md) | [繁體中文](./README.zh-TW.md)

1. **throughline** — 看進度、調方向  
2. **plan-spar** — 對齊一片、鎖/瘦 `PLAN.md`、審計畫、你 APPROVE  
3. **clean-cut** — 按 PLAN **最小實作**（ponytail 梯子）+ 驗證 + 回寫  

---

## 四個 skill

| Skill | 職責 | 思想來源 |
|-------|------|----------|
| `breaking-coding-chaos` | 編排 | — |
| `throughline` | 進度可見與調整 | planning-with-files |
| `plan-spar` | 對齊 + 鎖/審 PLAN（**不寫業務代碼**） | grill-with-docs |
| **`clean-cut`** | **寫代碼**（YAGNI 梯子） | **ponytail** |

```text
throughline → plan-spar（APPROVE）→ clean-cut → 回寫 throughline
```

**命名：** plan-spar = 搞計畫；clean-cut = 乾淨下刀寫碼（對應 ponytail）。

---

## 示例

**你：** `/breaking-coding-chaos` 做 Anki CLI，先 cloze。  
**throughline：** 建三檔，你改地圖。  
**plan-spar：** 鎖 PLAN → 審 → 你 APPROVE。  
**clean-cut：** 最小 diff + 驗證 → 約減 PLAN → 回寫。  
**下一片：** 再 `/plan-spar` → APPROVE → `/clean-cut`。

| 你說 | 技能 |
|------|------|
| 我們到哪了？ | throughline |
| plan-spar：支付回呼 | plan-spar |
| 按 PLAN 實作 / clean-cut | clean-cut |

---

## 安裝

拷貝四個目錄，見 [docs/install/README.md](../docs/install/README.md)。

License: MIT。
