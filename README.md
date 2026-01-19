# ASD 智能文檔架構師 (ASD Document Architect)

> **Agent-Skill Driven Single Source of Truth (ASD-SSOT)**
> 專為 LLM 長文本檢索設計的高效、零幻覺、結構化封裝系統。

![Version](https://img.shields.io/badge/Version-v1.5.3-blue.svg) ![Language](https://img.shields.io/badge/Language-Traditional%20Chinese-green.svg) ![License](https://img.shields.io/badge/License-MIT-orange.svg)

## 📖 專案簡介

**ASD 智能文檔架構師** 是一個高階 System Prompt（系統提示詞），旨在解決 LLM 在處理長文檔（PDF、Markdown、Word）時面臨的「Token 消耗過大」、「檢索迷失 (Lost-in-the-middle)」以及「內容幻覺」問題。

本系統不進行摘要（Summarization），而是將非結構化文檔轉化為具備 **路由觸發機制 (Trigger-Based Routing)** 的智能模塊。它將靜態文檔轉化為 AI Agent 可以調用的「技能 (Skills)」，實現 **100% 原文保留** 與 **精準檢索**。概念參考自 Claude Agent Skills。

---

## 💎 關鍵功能 (Key Features)

* **零幻覺封裝 (Zero Hallucination)**：嚴格執行「封裝而非摘要」協議，確保輸出的 Markdown 內容與原文 100% 字元級一致。
* **智能路由機制 (Smart Routing)**：自動生成 `Trigger Context`（觸發語境），讓下游 AI 僅在必要時讀取特定模塊，極大節省 Token。
* **結構化錨點 (Structured Anchors)**：使用 `## [MODULE X]` 作為硬性錨點，解決 LLM 在長文中定位錯誤的問題。
* **容量自適應 (Adaptive Volume)**：內建 20,000 Token 閾值檢測，自動決定採用「單檔整合」或「物理分拆」策略。**(v1.5.3 新增：分拆模式支援無縫拼接，Part 1 內建全域索引。)**
* **下游 AI 友善 (Downstream Friendly)**：生成的文檔內嵌「解碼指令」，無需額外配置即可被 RAG 系統或 Agent 精準讀取。

### 🚀 v1.5.3 (Seamless Stitching Edition) 核心更新
* **無縫拼接 (Seamless Stitching)**：物理分拆模式下，Part 2 及後續分卷自動去除重複標頭，支援直接 Copy-Paste 完美還原為單一文檔。
* **全域索引 (Global Master Index)**：Part 1 預先生成涵蓋所有分卷 (Part 1-N) 的完整索引，解決分卷檢索時的「視野盲區」問題。
* **防幻覺降級 (Fallback Protocol)**：下游解碼器新增 Step 4 檢測機制，當無資料匹配時強制回報 Out of Scope，嚴禁編造數據。

---

## 🌟 核心原理 (Core Principles)

1.  **原文神聖性 (Content Fidelity)**
    * **封裝而非摘要**：嚴禁改寫或縮減內容。所有的 URL、表格、數據、代碼塊均保持 100% 字元級一致。
    * **完整性檢查**：內建六大檢查機制，確保輸出內容行數不減反增。

2.  **路由與酬載分離 (Router-Payload Separation)**
    * **L1 Index (Router)**：輕量級索引，僅包含「技能名稱」與「觸發條件」。
    * **L2 Module (Payload)**：實際內容被封裝在獨立模塊中，只有在 Trigger 匹配時才被讀取。

3.  **觸發優先 (Trigger First)**
    * 每個模塊均附帶 `Trigger Context`（例如：「當用戶詢問 Q4 財報數據時...」），引導下游 AI 進行非線性跳轉閱讀。

---

## 🛠️ 使用方法 (Usage)

### 1. 安裝 (Installation)
本工具無需安裝代碼庫，僅需導入 Prompt。
1.  進入 `prompts/` 資料夾（或查看本倉庫源碼）。
2.  複製 `prompt_ASD_Document_Architect.md` 的完整內容。

### 2. 啟動 (Initialization)
在 ChatGPT (GPT-5) 或 Claude (Sonnet 4.5) 或 Gemini (3.0 Pro) 中開啟 **New Chat**，貼上 Prompt 並發送。
> **系統回應**：「ASD 智能文檔架構師 已就緒...」

### 3. 執行轉換 (Execution)
直接上傳您的 PDF 或 Markdown 檔案，系統將自動判斷模式。

#### 💡 常見應用案例 (Common Use Cases)

**🟢 案例 A：處理 100 頁的公司年報 (PDF) —— [Mode A: 範圍界定]**
* **場景**：檔案巨大，無法一次讀完。
* **操作**：直接上傳 PDF。
* **AI 行為**：AI 不會硬讀全文，而是先掃描前 20 頁目錄，列出章節（如：財務摘要、ESG 報告、管理層討論...），詢問您要提取哪部分。
* **結果**：您指定「財務摘要」後，AI 僅提取該部分並封裝為 ASD 模塊。

**🟢 案例 B：處理 10,000 中文字資料 (Markdown) —— [Mode A: 單檔整合]**
* **場景**：內容豐富但未超過 Context Window 極限（< 20k Tokens）。
* **操作**：上傳 Markdown 檔。
* **AI 行為**：AI 評估容量後，自動採用 **「整合式結構 (Consolidated Structure)」**。
* **結果**：輸出一個單一的 `.md` 檔，內部包含多個由 `[MODULE SEPARATOR]` 分隔的區塊，並附帶 Meta-Index 索引，方便下游 AI 一次性讀取與跳轉。

**🔵 案例 C：處理超長文檔或建立知識庫 —— [Mode B: 無縫分拆]**
* **場景**：總內容 > 20,000 Tokens (如技術手冊、法規全文)。
* **操作**：AI 自動啟動分拆模式。
* **AI 行為**：
    * **Part 1**：輸出全域索引及前段內容。
    * **Part 2+**：僅輸出後續模塊內容 (無標頭)。
* **結果**：您只需將各 Part 依序複製貼上，即可組合成一個完整的 ASD-SSOT 檔案，無需手動修復格式。

---

## 📂 輸出格式範例 (Output Structure)

ASD 生成的文檔具備**自解釋性**，包含給下游 AI 的指令：

```markdown
# [ROOT] 2025 全球局勢報告 (Consolidated)

> **SYSTEM INSTRUCTION FOR DOWNSTREAM AI**:
> This file contains multiple logical modules separated by the exact text line: `========== [MODULE SEPARATOR] ==========`.
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
last_updated: 2026-01-18
---

### [Data Payload: 美中貿易數據]
> **Trigger Context (AI)**: When user asks about China's trade surplus or tariff impacts in 2025.

(此處為 100% 原文內容...)

[Source: PDF P.12]

---
========== [MODULE SEPARATOR] ==========
---


```

---

## 🤖 下游 AI 整合 (Downstream Integration)

要讓其他 AI (如 RAG 系統或另一個 Chat session) 高效讀取 ASD 文檔，建議在傳送 ASD 檔案前，先發送以下 **Decoder Prompt**。這將強制 AI 採用「跳躍式讀取」而非「線性閱讀」，最大化 Token 效率。

```markdown
# System Prompt: ASD-SSOT Decoder (ASD 智能解碼器)

**Role Definition**:
你是一個專門讀取 **ASD-SSOT (Agent-Skill Driven)** 格式文檔的智能閱讀器。

**PROTOCOL (讀取協議)**:
在回答用戶問題時，嚴格遵守以下「跳躍式讀取」流程：

1. **Step 1: 索引路由 (Index Routing)**
   * 讀取文檔頂部的 `> META-INDEX`。
   * 根據用戶 Query 關鍵詞，匹配最相關的 `Module ID` 或 `Description`。
   * *Critical*: 若 Query 涉及多個面向（如「營收與估值關係」），請規劃讀取多個 Module (e.g., Mod 2 + Mod 4)。

2. **Step 2: 精確跳轉 (Precision Jump)**
   * 直接搜索標題錨點 `## [MODULE X]`。
   * **忽略** 所有非目標 Module 的內容以節省注意力資源。

3. **Step 3: 驗證與提取 (Verify & Fetch)**
   * 檢查該 Module 的 `Trigger Context`。
   * 僅從 `[Data Payload]` 區塊中提取資訊。

4. **Step 4: 回答生成與降級 (Response & Fallback)**
   * **引用規則**：回答必須基於提取的原文，並標註 `[Source: PDF P.XX]`。
   * **Fallback (v1.5.3)**：如果所有 Module 的 Trigger 都不匹配，請直接回答：「ASD 知識庫中未包含此具體資訊（Out of Scope）。」**嚴禁編造數據。**

**Input Context**:
用戶將提供一個 ASD 格式的 Markdown 檔案。

```

---

## ⚠️ 操作守則 (Operational Rules)

系統在輸出前會強制執行以下檢查：

1. **完整性**：URL、表格是否跑版？
2. **行數驗證**：新輸出的行數必須 > 原文行數。
3. **格式保護**：JSON/YAML/Code Block 必須保留語法。
4. **禁止佔位符**：嚴禁出現 `(...)` 或 `[同上]`。

---

## 📜 License

[MIT License](https://www.google.com/search?q=LICENSE)

---

**ASD Architect** - *Turning Documents into Agent Skills.*
