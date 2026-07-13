# breaking-coding-chaos

**人在环路 Agent Skill 套件：分步交付，不丢进度与掌控。**

[English](../README.md) | [简体中文](./README.zh-CN.md) | [繁體中文](./README.zh-TW.md)

1. **throughline** — 看进度、调方向  
2. **plan-spar** — 对齐一片、锁/瘦 `PLAN.md`、审计划、你 APPROVE  
3. **clean-cut** — 按 PLAN **最小实现**（ponytail 梯子）+ 验证 + 回写  

---

## 四个 skill

| Skill | 职责 | 思想来源 |
|-------|------|----------|
| `breaking-coding-chaos` | 编排 | — |
| `throughline` | 进度可见与调整 | planning-with-files |
| `plan-spar` | 对齐 + 锁/审 PLAN（**不写业务代码**） | grill-with-docs |
| **`clean-cut`** | **写代码**（YAGNI 梯子） | **ponytail** |

```text
throughline → plan-spar（APPROVE）→ clean-cut → 回写 throughline
```

**命名：** plan-spar = 搞计划；clean-cut = 干净下刀写码（对应 ponytail）。

---

## 示例

**你：** `/breaking-coding-chaos` 做 Anki CLI，先 cloze。  
**throughline：** 建三文件，你改地图。  
**plan-spar：** 锁 PLAN → 审 → 你 APPROVE。  
**clean-cut：** 最小 diff + 验证 → 约减 PLAN → 回写。  
**下一片：** 再 `/plan-spar` → APPROVE → `/clean-cut`。

| 你说 | 技能 |
|------|------|
| 我们到哪了？ | throughline |
| plan-spar：支付回调 | plan-spar |
| 按 PLAN 实现 / clean-cut | clean-cut |

---

## 安装

拷贝四个目录，见 [docs/install/README.md](../docs/install/README.md)。

License: MIT。
