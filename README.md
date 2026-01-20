# ASD 智能文檔架構師 (ASD Document Architect)

> **Agent-Skill Driven Single Source of Truth (ASD-SSOT)**
> 專為 LLM 長文本檢索設計的高效、零幻覺、結構化封裝系統。

![Version](https://img.shields.io/badge/Version-v1.5.5-blue.svg) ![Language](https://img.shields.io/badge/Language-Traditional%20Chinese-green.svg) ![License](https://img.shields.io/badge/License-MIT-orange.svg)

## 📖 專案簡介

**ASD Architect** - *不靠 LLM 線性通讀：以「封裝而非摘要」將原文零改寫轉為可路由 ASD-SSOT；先掃描 Meta-Index，命中模組後精準跳轉並嚴格引用。*

**ASD 智能文檔架構師（ASD Document Architect）** 是一個高階 System Prompt（系統提示詞），用於緩解 LLM 處理長文檔（PDF、Markdown、Word）時常見的 **Token 消耗過大**、**檢索迷失（Lost-in-the-middle）** 與 **內容幻覺** 風險。

ASD 不做摘要（Summarization），而是把非結構化文檔封裝為具備 **路由與酬載分離（Router–Payload Separation）** 的模組化 SSOT：以 **精細化語意路由（Granular Semantic Routing）**、**實體級清單（Entity Inventory）** 與 **場景化 Trigger** 組成全域索引（Meta-Index），令下游 AI 先路由再讀取；同時透過 **100% 原文保留**、可追溯錨定與標準化「解碼指令」提升可驗收性與可復用性。本專案概念參考自 Claude Agent Skills，但以純 Prompt 形式實作，無需安裝代碼庫，並可在不同 LLM／下游 RAG 或 Agent 場景直接整合使用。

### 立即體驗（Gemini DEMO）:
如想最快體驗 DEMO，可直接使用以下 Gemini Gems（**可能需要登入 Google 帳戶**）：
- 📜 **ASD 智能文檔架構師 (ASD Document Architect)**：https://gemini.google.com/gem/1Us9GWj3H4nYNvbd_2drZUMqfuJni_8MK?usp=sharing
- 📜 **ASD-SSOT Decoder (ASD 智能解碼器)**：https://gemini.google.com/gem/1oMZeRZ-LLayNZoUZuiqSUgavZ6PN6FFY?usp=sharing

---

## 💎 關鍵功能 (Key Features)

* **零幻覺封裝 (Zero Hallucination)**：嚴格執行「封裝而非摘要」協議，確保輸出的 Markdown 內容與原文 100% 字元級一致。
* **雙層頁碼錨定 (Dual-Layer Anchoring)**：解決 PDF 物理頁碼與印刷頁碼不一致的痛點，強制標註 `PDF_Index` (檔案座標) 與 `Print_Label` (業務座標)，徹底消除溯源歧義。
* **精細化語意路由 (Granular Semantic Routing)**：引入實體級清單與場景化觸發機制，預判用戶意圖 (如 "Why did...", "What is the specific value of...")，實現「手術刀級」的數據定位。
* **實體級清單 (Entity-Level Inventory)**：在元數據中強制提取關鍵人名、地名、專案代號及數據指標，解決傳統 RAG 系統對細節內容「漏召回」的問題。
* **下游 AI 友善 (Downstream Friendly)**：生成的文檔內嵌標準化「解碼指令」與 `Meta-Index`，無需額外配置即可被 RAG 系統或 Agent 精準讀取。
* **無縫分拆 (Seamless Stitching)**：內建 20,000 Token 閾值檢測，對於超長文檔自動採用「物理分拆」策略，並支援 Copy-Paste 完美無縫合併。

---

## 🌟 核心原理 (Core Principles)

1.  **原文神聖性 (Content Fidelity)**
    * **封裝而非摘要**：嚴禁改寫或縮減內容。所有的 URL、表格、數據、代碼塊均保持 100% 字元級一致。
    * **完整性檢查**：內建多項檢查機制，確保輸出內容行數不減反增。

2.  **元數據增強 (Metadata Enrichment)**
    * **Description (Granular)**：必須包含「摘要」、「實體清單」與「負向消歧」三個層次。
    * **Trigger (Interrogative)**：必須使用具體場景的疑問句，而非單純的關鍵詞標籤。

3.  **路由與酬載分離 (Router-Payload Separation)**
    * **L1 Index (Router)**：包含豐富元數據的全局索引。
    * **L2 Module (Payload)**：實際內容被封裝在獨立模塊中，只有在 Trigger 匹配時才被讀取。

---
## 🛠️ 使用方法 (Usage)

> **目標**：先用 **ASD Document Architect** 把原文「封裝而非摘要」成可路由的 **ASD-SSOT**；再用 **ASD-SSOT Decoder** 先掃描 `> META-INDEX`，命中模組後精準跳轉並嚴格引用。

### 1. 準備（一次性）
本工具無需安裝代碼庫；只需準備兩份 Prompt 與一份原文：
1. 於本倉庫根目錄複製以下兩個檔案全文：
    * `prompt_ASD_Document_Architect.md`（封裝器／Architect）
    * `prompt_ASD Decoder.md`（解碼器／Decoder）
2. 準備要處理的原文檔（PDF / Markdown / Word）。

### 2. Step A — 生成 ASD-SSOT（用 ASD Document Architect 封裝原文）
1. 在任一 LLM 平台開啟 **New Chat**（建議使用獨立對話，避免混入其他上下文）。
2. 貼上 `prompt_ASD_Document_Architect.md` 全文並發送。
3. 上傳原文檔案，按 Architect 提示執行並取得輸出：
    * **Mode A（整合式）**：文檔規模可於單次上下文內處理（通常 < 20k tokens）；輸出為單一整合檔，模組以 `[MODULE SEPARATOR]` 分隔。
    * **Mode B（分拆式）**：文檔超長或要建立知識庫；輸出會分成多個 Part（可依序 Copy-Paste 無縫拼接）。
4. 將輸出保存為一份完整的 `*_ASD-SSOT.md`（Mode B 則先依序拼接成單一檔案後保存）。

### 3. Step B — 以 Decoder 問答（先索引、後跳轉、再引用）
1. 另開一個 **New Chat**（建議與 Architect 分開，確保解碼器只以 ASD-SSOT 為唯一資料源）。
2. 貼上 `prompt_ASD Decoder.md` 全文並發送。
3. 提供剛生成的 `*_ASD-SSOT.md`（可直接貼上或上載檔案）。
4. 提出問題；Decoder 會先掃描 `> META-INDEX`，再跳轉至命中模組，並在回答中提供引用（例如 `[Source: PDF_Index | Print_Label]`）。

### 4. 新手提示（Troubleshooting）
* **回答未先掃描索引**：在同一對話要求 Decoder 重新執行「先掃描 `> META-INDEX` → 命中模組 → 只用該模組 `Data Payload` 回答」。
* **內容過長**：用 Mode B；在 Decoder 階段優先提供需要的 Part，或提供已拼接的完整 ASD-SSOT。
* **PDF 有兩套頁碼**：請確保封裝輸出同時包含 `PDF_Index` 與 `Print_Label`，以免溯源歧義。

---


## 📂 輸出格式範例 (Output Structure)

ASD v1.5.5 生成的文檔具備 **自解釋性** 與 **高顆粒度**，包含給下游 AI 的精細化指令：

```markdown
# [ROOT] 2025 全球局勢報告 (Consolidated)

> **SYSTEM INSTRUCTION FOR DOWNSTREAM AI**:
> This file contains multiple logical modules.
> 1. Do NOT read linearly. Scan the [META-INDEX] below.
> 2. Find the target module by searching for the exact header: `## [MODULE X]`.
> ...

> **META-INDEX**:
> - Module 1: `trade_data_2025` (Anchor: [MODULE 1])
> - Module 2: `fed_rates_decision` (Anchor: [MODULE 2])

---
========== [MODULE SEPARATOR] ==========
---

## [MODULE 1]

---
module_id: trade_data_2025
source_file: report.pdf
last_updated: 2026-01-20
---

### [Data Payload: 美中貿易數據]
> **Description (Granular)**:
> 1. **摘要**：本模塊詳述了 2025 年美中貿易順差的變化及關稅政策影響。
> 2. **實體清單 (Entity Inventory)**：涵蓋了 **USTR 代表**、**上海港吞吐量**、**301 條款修訂案**、以及關鍵數據 **YoY +5.4%**。
> 3. **負向消歧 (Negative Scope)**：本模塊 **不包含** 歐盟地區的貿易數據（請參見 Module 3）。
>
> **Trigger Context (Scenario-Based)**:
> - "How did the new tariffs affect Shanghai port throughput?"
> - "What is the specific trade surplus value in 2025 Q1?"
> - "List the amendments to Section 301."

(此處為 100% 原文內容...)

[Source: PDF_Index P.12 | Print_Label P.8]

---
========== [MODULE SEPARATOR] ==========
---

```

---

## 🤖 下游 AI 整合 (Downstream Integration)

要讓其他 AI (如 RAG 系統或另一個 Chat session) 高效讀取 ASD 文檔，建議在傳送 ASD 檔案前，先使用本倉庫的 **Decoder Prompt（唯一 SSOT）**：

* **Decoder Prompt**：[`prompt_ASD Decoder.md`](https://github.com/Adamchanadam/ASD-Document-Architect/blob/main/prompt_ASD%20Decoder.md) 

**建議流程**：

1. 先在新對話中貼上 Decoder Prompt。
2. 再提供由 `prompt_ASD_Document_Architect.md` 生成的 ASD-SSOT 文檔。
3. 最後提出問題，Decoder 會根據 `> META-INDEX` 進行跳轉，並在回答時提供 `[Source: PDF_Index | Print_Label]` 雙重引用。

---

## ⚠️ 操作守則 (Operational Rules)

系統在輸出前會強制執行 **8 項完整性檢查**，包含：

1. **頁碼錨定 (Anchoring)**：嚴格執行 `PDF_Index` 與 `Print_Label` 雙重標註。
2. **完整性**：URL、表格是否跑版？
3. **行數驗證**：新輸出的行數必須 > 原文行數。
4. **格式保護**：JSON/YAML/Code Block 必須保留語法。
5. **禁止佔位符**：嚴禁出現 `(...)` 或 `[同上]`。
6. **元數據顆粒度**：Description 必須包含實體清單，Trigger 必須是疑問句。
... (詳見 Prompt 內文)

---

## 📜 License

[MIT License](https://opensource.org/licenses/MIT)

---

**ASD Architect** - *不靠 LLM 線性通讀：以原文零改寫封裝為可路由 SSOT，依索引命中後精準跳轉並嚴格引用。*
