# ASD 智能文檔架構師 (ASD Document Architect)

> **Agent-Skill Driven Single Source of Truth (ASD-SSOT)**
> 專為 LLM 長文本檢索設計的高效、低幻覺風險、結構化封裝系統。

![Version](https://img.shields.io/badge/Version-v1.6.2-blue.svg) ![Language](https://img.shields.io/badge/Language-Traditional%20Chinese-green.svg) ![License](https://img.shields.io/badge/License-MIT-orange.svg)

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

* **絕對全量協議 (Absolute Full-Text Protocol)**：嚴格執行「封裝而非摘要」協議。一旦頁碼範圍鎖定，輸出的 Markdown 內容必須與原文 100% 字元級一致，拒絕採摘式刪減。
* **Preflight（Fail-Fast + Safe Scope Cap）**：在進入 Sizing Worksheet 前先做 **Access Probe**（探測是否能讀到 PDF 中段文字層／內文）。若探測失敗，立即切換 **Text-Paste**，並先計算「單批可安全貼上」的頁數上限（Safe Scope Cap），避免「先算一大堆 Parts 才發現讀不到內容」。
* **容量估算與分卷規劃 (Sizing Worksheet)**：按頁數與密度分級完成保守雙界估算，輸出 `parts_min–parts_max`（含假設與算式）；禁止憑印象估計 Part 數量，寧可分拆多份也不可壓縮內容。
* **分卷上限 presets（按平台切換｜3 檔 preset）**：`PRESET_GEMINI: 50000`；`PRESET_CLAUDE: 50000`；`PRESET_CHATGPT: 13000（不建議；僅作兼容／緊急用途）`。
* **無限長度物理分拆 (Physical Splitting)**：當內容超出單次輸出安全上限時，自動分卷輸出 `Part 1`（含全域導航與 Master Meta-Index）及後續 `Part N`（Body）。每個 Part 必須以**單一** ```markdown 代碼塊封裝，並在結尾以三行分隔符收束（`---`、`========== [MODULE SEPARATOR] ==========`、`---`），以支援 Copy-Paste 無縫拼接；新增模塊僅用 `> META-INDEX UPDATE:` 追加增量索引。
* **雙層頁碼錨定 (Dual-Layer Anchoring)**：強制標註 `PDF_Index`（檔案座標）與 `Print_Label`（引用座標；如無則 `N/A`）。`PDF_Index` 必須取自 PDF 閱讀器／工具顯示的絕對頁序；不得從正文推斷或以 `Print_Label` 代填。
* **精細化語意路由 (Granular Semantic Routing)**：以實體級清單與場景化疑問句 Trigger，實現「先路由、後讀取」的精準定位。
* **實體級清單 (Entity-Level Inventory)**：在元數據中強制提取關鍵人名、地名、公司名、專案代號及數據指標，降低漏召回風險。
* **下游 AI 友善 (Downstream Friendly)**：文檔內嵌標準化解碼指令與索引；解碼器先讀 `> META-INDEX` 並合併 `> META-INDEX UPDATE:`，再以模塊錨點精準跳轉。

---


## 🌟 核心原理 (Core Principles)

1.  **絕對全量協議 (Absolute Full-Text Protocol)**
    * **封裝而非摘要**：嚴禁改寫或縮減內容。所有的 URL、表格、數據、代碼塊均保持 100% 字元級一致。
    * **零損耗提取**：一旦頁碼範圍鎖定，AI 必須盲目轉錄所有內容，禁止智能過濾。

2.  **元數據增強 (Metadata Enrichment)**
    * **Description (Granular)**：必須包含「摘要」、「實體清單」與「負向消歧」三個層次。
    * **Trigger (Interrogative)**：必須使用具體場景的疑問句，而非單純的關鍵詞標籤。

3.  **路由與酬載分離 (Router-Payload Separation)**
    * **L1 Index (Router)**：包含豐富元數據的全局索引。
    * **L2 Module (Payload)**：實際內容被封裝在獨立模塊中，只有在 Trigger 匹配時才被讀取。

---
## 🛠️ 使用方法 (Usage)

> **目標**：先用 **ASD Document Architect** 把原文「封裝而非摘要」成可路由的 **ASD-SSOT**；再用 **ASD-SSOT Decoder** 先掃描 `> META-INDEX`（並合併 `> META-INDEX UPDATE:`），命中模組後精準跳轉並嚴格引用。

**平台建議（先讀）**：
* **建議平台**：優先使用支援較高單次輸出上限的平台（例如 Gemini／Claude），以降低 Parts 數量並減少跨頁表格截斷風險。
* **不建議 ChatGPT**：單次輸出上限偏低，會令 Parts 數暴增並提高結構損壞風險；若仍需使用，務必縮小頁碼範圍並採用更保守的分卷上限。
* **part_budget presets（3 檔 preset）**：`PRESET_GEMINI: 50000`；`PRESET_CLAUDE: 50000`；`PRESET_CHATGPT: 13000（不建議；僅作兼容／緊急用途）`。

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
    * **MODE A（原始長文轉模塊）**：把原文封裝為可路由 ASD-SSOT；輸出可能是單檔整合或多 Part 物理分拆（由容量與分卷上限自動判斷）。
    * **MODE B（構建技能索引）**：在已保存多份 ASD-SSOT 檔案後，生成 Master Knowledge Index；必須先提供 **FILE MANIFEST（檔名清單）** 及 **SOURCE INPUT（全文或至少 `> META-INDEX` + `Trigger Context` 區段）**，否則 Fail-Closed。
4. 將輸出保存為 `*_ASD-SSOT.md`；如為物理分拆，保存為多個 `_PartN.md` 檔案。MODE B 的索引輸出則另存為獨立的 Index Markdown 檔。


### 3. Step B — 以 Decoder 問答（先索引、後跳轉、再引用）
1. 另開一個 **New Chat**（建議與 Architect 分開，確保解碼器只以 ASD-SSOT 為唯一資料源）。
2. 貼上 `prompt_ASD Decoder.md` 全文並發送。
3. 提供剛生成的 `*_ASD-SSOT.md`（若是分拆檔，先提供 Part 1，待 AI 回應後再提供 Part 2...）。
4. 提出問題；Decoder 會先掃描 `> META-INDEX`，再跳轉至命中模組，並在回答中提供引用（例如 `[Source: PDF_Index | Print_Label]`）。

### 4. 新手提示（Troubleshooting）
* **回答未先掃描索引**：在同一對話要求 Decoder 重新執行「先掃描 `> META-INDEX`（如有 `> META-INDEX UPDATE:` 必須先合併）→ 命中模組 → 只用該模組 `Data Payload` 回答」。
* **先算大量 Parts 才發現讀不到 PDF 中段**：要求 Architect 先做 Preflight 的 **Access Probe**；如回報 `ACCESS=RESTRICTED`，立即改用 Text-Paste，並按 Safe Scope Cap 分批貼上。
* **輸出出現省略／佔位符**：屬 Fail-Closed；必須縮小頁碼範圍或增加物理分拆，重建 해당 Module／Part；不得以推測補足。
* **PDF 有兩套頁碼**：`PDF_Index` 必須取自 PDF 閱讀器／工具顯示的絕對頁序；`Print_Label` 取自紙面印刷頁碼（無則 `N/A`）。如為 Text-Paste 且無法可靠取得 `PDF_Index`，則以 `N/A` 原樣標示。


---


## 📂 輸出格式範例 (Output Structure)

ASD 生成的文檔具備 **自解釋性** 與 **高顆粒度**，包含給下游 AI 的精細化指令：

```markdown
# [ROOT] 2025 全球局勢報告 (Consolidated)

> **SYSTEM INSTRUCTION FOR DOWNSTREAM AI**:
> This file contains multiple logical modules.
> 1. Do NOT read linearly. Scan the [META-INDEX] below.
> 2. Find the target module by searching for the exact header: `## [MODULE X]`.
> 3. Only load the specific [MODULE] payload when User Query matches the `Trigger Context`.

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

(此處為 100% 盲目轉錄的原文內容，保留所有表格與附註。)

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
2. 再提供由 `prompt_ASD_Document_Architect.md` 生成的 ASD-SSOT 文檔（Part 1）。
3. (如有) 繼續提供 Part 2... Decoder 會自動掛載續章。
4. 最後提出問題，Decoder 會根據 `> META-INDEX` 進行跳轉，優先採用 **直接引用** 策略，並提供 `[Source: PDF_Index | Print_Label]` 雙重引用。

---

## ⚠️ 操作守則 (Operational Rules)

系統在輸出前會強制執行 **8 項完整性檢查**，包含：

1. **頁碼錨定 (Dual-Layer Anchoring)**：
   * `PDF_Index` 必須取自 PDF 閱讀器／工具顯示的絕對頁序；不得從正文推斷或以 `Print_Label` 代填。
   * `Print_Label` 取自紙面印刷頁碼；無法可靠識別則填 `N/A`。
2. **完整性 (Completeness)**：URL、表格、代碼塊是否完整且未跑版？每個 Module 是否包含引用行與分隔符？
3. **行數驗證（禁用）**：禁止以「行數比較」作為合規依據；改用：
   * **結構完整**：必要 Metadata／引用行／分隔符齊備；
   * **表格完整**：不得截斷跨頁表格；不足則改為物理分拆並在自然邊界收束；
   * **引用存在**：每個 Module 至少一行 `[Source: PDF_Index ... | Print_Label ...]`（不可得則 `N/A`）。
4. **格式無損保護 (Format Immunity)**：JSON/YAML/XML/Code Block 必須 100% 保留語法與縮排。
5. **禁止省略與佔位符 (Fail-Closed)**：嚴禁 `...`（用作省略）、`(XXX)`、`[同上]`、`[見原文]` 等；命中即中止並要求縮小範圍或增加分拆重做。
6. **元數據顆粒度 (Metadata Granularity)**：Description 必須包含實體清單與負向消歧；Trigger 必須為疑問句式場景。
7. **語言 (Language)**：對話用繁體中文，但 Data Payload 內原文語言不可變更。
8. **Initialization**：啟動後必須宣告已就緒與支援能力（如零損耗提取、雙層頁碼錨定、無縫拼接）。



---

## 📜 License

[MIT License](https://opensource.org/licenses/MIT)

---

**ASD Architect** - *不靠 LLM 線性通讀：以原文零改寫封裝為可路由 SSOT，依索引命中後精準跳轉並嚴格引用。*
