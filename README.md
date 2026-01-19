# ASD 智能文檔架構師 (ASD Document Architect)

> **Agent-Skill Driven Single Source of Truth (ASD-SSOT)**
> 專為 LLM 長文本檢索設計的高效、零幻覺、結構化封裝系統。

![Version](https://img.shields.io/badge/Version-v1.5.4-blue.svg) ![Language](https://img.shields.io/badge/Language-Traditional%20Chinese-green.svg) ![License](https://img.shields.io/badge/License-MIT-orange.svg)

## 📖 專案簡介

**ASD 智能文檔架構師** 是一個高階 System Prompt（系統提示詞），旨在解決 LLM 在處理長文檔（PDF、Markdown、Word）時面臨的「Token 消耗過大」、「檢索迷失 (Lost-in-the-middle)」以及「內容幻覺」問題。

本系統不進行摘要（Summarization），而是將非結構化文檔轉化為具備 **精細化語意路由 (Granular Semantic Routing)** 的智能模塊。它將靜態文檔轉化為 AI Agent 可以調用的「技能 (Skills)」，實現 **100% 原文保留** 與 **手術刀級精準檢索**。概念參考自 Claude Agent Skills。

---

## 💎 關鍵功能 (Key Features)

* **零幻覺封裝 (Zero Hallucination)**：嚴格執行「封裝而非摘要」協議，確保輸出的 Markdown 內容與原文 100% 字元級一致。
* **精細化語意路由 (Granular Semantic Routing)**：(v1.5.4 新增) 引入實體級清單與場景化觸發機制，預判用戶意圖 (如 "Why did...", "What is the specific value of...")，實現「手術刀級」的數據定位。
* **實體級清單 (Entity-Level Inventory)**：在元數據中強制提取關鍵人名、地名、專案代號及數據指標，解決傳統 RAG 系統對細節內容「漏召回」的問題。
* **下游 AI 友善 (Downstream Friendly)**：生成的文檔內嵌標準化「解碼指令」與 `Meta-Index`，無需額外配置即可被 RAG 系統或 Agent 精準讀取。
* **無縫分拆 (Seamless Stitching)**：內建 20,000 Token 閾值檢測，對於超長文檔自動採用「物理分拆」策略，並支援 Copy-Paste 完美無縫合併。

---

## 🌟 核心原理 (Core Principles)

1.  **原文神聖性 (Content Fidelity)**
    * **封裝而非摘要**：嚴禁改寫或縮減內容。所有的 URL、表格、數據、代碼塊均保持 100% 字元級一致。
    * **完整性檢查**：內建多項檢查機制，確保輸出內容行數不減反增。

2.  **元數據增強 (Metadata Enrichment)** (v1.5.4 核心)
    * **Description (Granular)**：必須包含「摘要」、「實體清單」與「負向消歧」三個層次。
    * **Trigger (Interrogative)**：必須使用具體場景的疑問句，而非單純的關鍵詞標籤。

3.  **路由與酬載分離 (Router-Payload Separation)**
    * **L1 Index (Router)**：包含豐富元數據的全局索引。
    * **L2 Module (Payload)**：實際內容被封裝在獨立模塊中，只有在 Trigger 匹配時才被讀取。

---

## 🛠️ 使用方法 (Usage)

### 1. 安裝 (Installation)
本工具無需安裝代碼庫，僅需導入 Prompt。
1.  查看本倉庫源碼（根目錄）。
2.  複製 `prompt_ASD_Document_Architect.md` 的完整內容。

### 2. 啟動 (Initialization)
在 ChatGPT (GPT-5) 或 Claude (Sonnet 3.5/3.7) 或 Gemini (1.5 Pro) 中開啟 **New Chat**，貼上 Prompt 並發送。
> **系統回應**：「ASD 智能文檔架構師 已就緒。支援無限分卷無縫拼接與精細化語意路由。」

### 3. 執行轉換 (Execution)
直接上傳您的 PDF 或 Markdown 檔案，系統將自動判斷模式。

#### 💡 常見應用案例 (Common Use Cases)

**🟢 案例 A：處理 100 頁的公司年報 (PDF) —— [Mode A: 範圍界定]**
* **場景**：檔案巨大，無法一次讀完。
* **操作**：直接上傳 PDF。
* **AI 行為**：AI 不會硬讀全文，而是先掃描前 20 頁目錄，詢問您要提取哪部分（如：財務摘要、ESG 報告）。
* **結果**：您指定「財務摘要」後，AI 僅提取該部分並進行「實體增強封裝」。

**🟢 案例 B：處理 10,000 中文字資料 (Markdown) —— [Mode A: 單檔整合]**
* **場景**：內容豐富但未超過 Context Window 極限（< 20k Tokens）。
* **操作**：上傳 Markdown 檔。
* **AI 行為**：AI 評估容量後，自動採用 **「整合式結構 (Consolidated Structure)」**。
* **結果**：輸出一個單一的 `.md` 檔，內部包含多個由 `[MODULE SEPARATOR]` 分隔的區塊，每個區塊均附帶精細化的 Description 與 Trigger。

**🔵 案例 C：處理超長文檔或建立知識庫 —— [Mode B: 無縫分拆]**
* **場景**：總內容 > 20,000 Tokens (如技術手冊、法規全文)。
* **操作**：AI 自動啟動分拆模式。
* **AI 行為**：
    * **Part 1**：輸出包含增強元數據的全域索引 (Master Meta-Index) 及前段內容。
    * **Part 2+**：僅輸出後續模塊內容 (無標頭，方便拼接)。
* **結果**：您只需將各 Part 依序複製貼上，即可組合成一個完整的 ASD-SSOT 檔案。

---

## 📂 輸出格式範例 (Output Structure)

ASD v1.5.4 生成的文檔具備 **自解釋性** 與 **高顆粒度**，包含給下游 AI 的精細化指令：

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
last_updated: 2026-01-19
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

[Source: PDF P.12]

---
========== [MODULE SEPARATOR] ==========
---

```

---

## 🤖 下游 AI 整合 (Downstream Integration)

要讓其他 AI (如 RAG 系統或另一個 Chat session) 高效讀取 ASD 文檔，建議在傳送 ASD 檔案前，先使用本倉庫的 **Decoder Prompt（唯一 SSOT）**：

* **Decoder Prompt**：[`prompt_ASD Decoder.md`](https://www.google.com/search?q=./prompt_ASD%2520Decoder.md)

**建議流程**：

1. 先在新對話中貼上 Decoder Prompt。
2. 再提供由 `prompt_ASD_Document_Architect.md` 生成的 ASD-SSOT 文檔。
3. 最後提出問題，Decoder 會根據 `> META-INDEX` 與 `Description (Granular)` 進行結構化跳轉讀取並嚴格引用。

---

## ⚠️ 操作守則 (Operational Rules)

系統在輸出前會強制執行以下檢查：

1. **完整性**：URL、表格是否跑版？
2. **行數驗證**：新輸出的行數必須 > 原文行數。
3. **格式保護**：JSON/YAML/Code Block 必須保留語法。
4. **禁止佔位符**：嚴禁出現 `(...)` 或 `[同上]`。
5. **元數據顆粒度 (Metadata Granularity)**：檢查 Description 是否已列出具體實體？Trigger 是否包含疑問句？嚴禁使用籠統描述。

---

## 📜 License

[MIT License](https://www.google.com/search?q=LICENSE)

---

**ASD Architect** - *Turning Documents into Agent Skills.*

