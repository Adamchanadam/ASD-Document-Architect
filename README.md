# ASD 智能文檔架構師 (ASD Document Architect)

> **Agent-Skill Driven Single Source of Truth (ASD-SSOT)**
> 專為 LLM 長文本檢索設計的高效、低幻覺風險、結構化封裝系統。

![Version](https://img.shields.io/badge/Version-v1.7.2-blue.svg) ![Language](https://img.shields.io/badge/Language-Traditional%20Chinese-green.svg) ![License](https://img.shields.io/badge/License-MIT-orange.svg)

## 📖 專案簡介

本專案由兩個 System Prompt 組成，建議按次序使用：

1) **`prompt_ASD_Document_Architect.md`（Architect｜封裝器）**  
把原始長文檔（PDF / Markdown / Word）封裝為可路由的 **ASD-SSOT**：  
- **封裝而非摘要**：原文零改寫、零刪減（Fail-Closed）  
- 生成可路由的 `> META-INDEX:` 與模組化 `## [MODULE X]`  
- 在超出單次輸出上限時，支援多卷（Part 1 / Part N）物理分拆與增量索引更新

2) **`prompt_ASD Decoder.md`（Decoder｜解碼器）**  
用於問答與檢索：先讀索引、精準跳轉命中模組、只用命中模組的 `[Data Payload]` 回答，並附上 **PDF_Index** 頁碼引用（Fail-Closed）。

ASD 的核心目標是降低 LLM 處理長文檔常見風險：  
- Token 消耗過大  
- 檢索迷失（Lost-in-the-middle）  
- 內容幻覺（憑印象補全、引用漂移、頁碼亂填）

### 立即體驗（Gemini DEMO）
如需最快體驗，可直接使用以下 Gemini Gems（可能需要登入 Google 帳戶）：
- 📜 **ASD 智能文檔架構師 (ASD Document Architect)**：https://gemini.google.com/gem/1Us9GWj3H4nYNvbd_2drZUMqfuJni_8MK?usp=sharing
- 📜 **ASD-SSOT Decoder (ASD 智能解碼器)**：https://gemini.google.com/gem/1oMZeRZ-LLayNZoUZuiqSUgavZ6PN6FFY?usp=sharing

---

## 💎 關鍵功能 (Key Features)

* **封裝而非摘要（Fail-Closed）**：一旦鎖定頁碼範圍，輸出必須與原文 100% 字元級一致；任何省略／佔位符／模板殘留一律視為不合格並中止。
* **Preflight（先探測再重工）**：在進入重型封裝前先探測是否能讀取目標範圍內容；若平台/權限導致讀不到內文，立即切換 Text-Paste 模式，避免白做分卷計算。
* **容量估算與分卷規劃（Sizing Worksheet）**：以可展示算式的方式估算 Parts 範圍；不足時只允許縮範圍或物理分拆，不允許摘要替代。
* **無限長度物理分拆（Part 1 / Part N）**：自動輸出可無縫拼接的多卷結構；Part 1 含全域索引，後續 Part 只輸出正文；新增模塊以 `> META-INDEX UPDATE:` 追加。
* **單層頁碼錨定（PDF_Index Only）**：所有引用一律使用 `PDF_Index`（PDF Viewer／讀取工具顯示的絕對頁序）作為唯一真理來源；嚴禁輸出或推算 `Print_Label`。
* **先路由、後讀取（Index → Jump → Cite）**：Decoder 先掃描 `> META-INDEX:`／合併 `> META-INDEX UPDATE:`，命中模組後才跳轉讀取；嚴禁線性通讀與 Payload 內文全文模糊搜索。
* **下游整合友善**：可直接配合 RAG / Agent / 另一個 Chat session；文件自帶索引與模組錨點，易於機械化定位與審計。

---

## 🌟 核心原理 (Core Principles)

1. **絕對全量協議 (Absolute Full-Text Protocol)**
   * **封裝而非摘要**：嚴禁改寫或縮減內容；URL、表格、代碼塊必須完整保留。
   * **零損耗提取**：只要鎖定範圍，就必須完整轉錄；不足時改以物理分拆，不以智能濾除替代。

2. **元數據增強 (Metadata Enrichment)**
   * **Description (Granular)**：包含摘要、實體清單、負向消歧三部分，提升可召回性並降低誤命中。
   * **Trigger (Interrogative)**：以具體疑問句描述可命中情境，而非單純關鍵詞標籤。

3. **路由與酬載分離 (Router-Payload Separation)**
   * **L1 Index (Router)**：先用索引定位模組。
   * **L2 Module (Payload)**：只讀取命中模組的 Payload，避免無關內容污染推理。

---

## 🛠️ 使用方法 (Usage)

> **目標**：先用 Architect 把原文封裝成 ASD-SSOT；再用 Decoder 進行問答（先索引 → 再跳轉 → 再引用）。

### 1. 準備（一次性）
本工具無需安裝代碼庫；只需兩份 Prompt 與一份原文：
1. 於本倉庫根目錄複製以下兩個檔案全文：
   * `prompt_ASD_Document_Architect.md`（封裝器／Architect）
   * `prompt_ASD Decoder.md`（解碼器／Decoder）
2. 準備要處理的原文檔案（PDF / Markdown / Word）。

### 2. Step A — 生成 ASD-SSOT（用 Architect 封裝原文）
1. 在任一 LLM 平台開啟 **New Chat**（建議使用獨立對話，避免混入其他上下文）。
2. 貼上 `prompt_ASD_Document_Architect.md` 全文並發送。
3. 上傳原文檔案，按 Architect 提示執行：
   * **MODE A（封裝原始長文）**：輸出單檔或多卷 Part（依容量與平台限制自動處理）。
   * **MODE B（建立 Master Knowledge Index）**：在已保存多份 ASD-SSOT 後，用檔名清單與必要輸入建立可跳轉的總索引；若缺必要輸入將直接中止（Fail-Closed）。
4. 將輸出保存為 `*_ASD-SSOT.md`；如為物理分拆，保存為多個 `_PartN.md` 檔案；MODE B 的輸出另存為獨立索引檔。

### 3. Step B — 以 Decoder 問答（先索引、後跳轉、再引用）
1. 另開一個 **New Chat**（建議與 Architect 分開，確保解碼器只以 ASD-SSOT 為唯一資料源）。
2. 貼上 `prompt_ASD Decoder.md` 全文並發送。
3. 提供剛生成的 ASD-SSOT：
   * 若是分拆檔：先提供 Part 1，按需要再依序提供 Part 2、Part 3……
   * 若同時提供多個 ASD 檔案：Decoder 會先分別建路由表，再合併候選模組後逐一跳轉。
4. 提出問題；Decoder 會：
   * 先掃描 `> META-INDEX:`（並合併 `> META-INDEX UPDATE:`）
   * 再以 `## [MODULE X]` 精準跳轉
   * 最後只用命中模組的 `[Data Payload]` 回答，並附上 `[Source: PDF_Index P.(實際值或 N/A)]` 引用

### 4. 新手提示（Troubleshooting）
* **回答未先掃描索引**：要求 Decoder 重新執行「先索引 → 再跳轉 → 再引用」，並確認已合併 `> META-INDEX UPDATE:`。
* **先做大量分卷才發現讀不到 PDF 中段**：回到 Architect，先做 Preflight 的探測；若讀取受限，改用 Text-Paste 並分批貼上再封裝。
* **輸出出現省略／佔位符／模板 token**：屬 Fail-Closed；必須縮小範圍或增加物理分拆重做；不得以推測補足。
* **PDF 存在印刷頁碼或羅馬數字頁碼**：一律忽略印刷頁碼；引用只使用 `PDF_Index`（PDF Viewer／讀取工具顯示的絕對頁序）。如無法可靠取得 `PDF_Index`，必須輸出 `N/A`。

---

## 📂 輸出格式範例 (Output Structure)

ASD 生成的文檔具備 **自解釋性** 與 **高顆粒度**，包含給下游 AI 的精細化指令：

```markdown
# [ROOT] 範例文檔（Consolidated）

> **SYSTEM INSTRUCTION FOR DOWNSTREAM AI**:
> This file contains multiple logical modules.
> 1. Do NOT read linearly. Scan the [META-INDEX] below.
> 2. Find the target module by searching for the exact header: `## [MODULE X]`.
> 3. Only load the specific [MODULE] payload when User Query matches the `Trigger Context`.

> META-INDEX:
> - Module 1: `topic_a` (Anchor: [MODULE 1])
> - Module 2: `topic_b` (Anchor: [MODULE 2])

---
========== [MODULE SEPARATOR] ==========
---

## [MODULE 1]

---
module_id: topic_a
source_file: example.pdf
---

### [Data Payload: 範例段落標題]
> **Description (Granular)**:
> 1. **摘要**：此模組涵蓋範例主題 A 的關鍵段落。
> 2. **實體清單 (Entity Inventory)**：列出主要實體與關鍵指標。
> 3. **負向消歧 (Negative Scope)**：不包含範例主題 B 的內容（請參見 Module 2）。
>
> **Trigger Context (Scenario-Based)**:
> - "Where is the definition of X?"
> - "List the constraints for Y."

（此處為 100% 原文轉錄的內容，保留表格、附註與格式。）

[Source: PDF_Index P.12]

---
========== [MODULE SEPARATOR] ==========
---
````

---

## 🤖 下游 AI 整合 (Downstream Integration)

要讓其他 AI（如 RAG 系統或另一個 Chat session）高效讀取 ASD 文檔，建議在傳送 ASD 檔案前先使用 Decoder Prompt：

* **Decoder Prompt**：`prompt_ASD Decoder.md`

**建議流程**：

1. 在新對話中貼上 Decoder Prompt。
2. 提供由 Architect 生成的 ASD-SSOT（先提供 Part 1）。
3. 如有續章，依序提供 Part 2、Part 3……
4. 最後提出問題；Decoder 會依 `> META-INDEX` 路由並精準跳轉，優先採用直接引用策略並提供 `PDF_Index` 頁碼引用。

---

## 🗨️ 已知問題　(Q&A)

### Q1：為何有時候封裝到一半會被迫中止，不能「先輸出再補」？

**A：因為系統採用 Fail-Closed。** 一旦偵測到讀取不連續、工具回傳空值/截斷、或輸出中出現任何省略/佔位符風險，Architect 必須立即中止以避免污染；此情況只能透過縮小頁碼範圍、增加物理分拆、重上載/重試，或改用 Text-Paste 分批處理來解決。

### Q2：為何 Decoder 有時答「Out of Scope」，但明明內容可能在文檔某處？

**A：因為 Decoder 嚴禁在 Payload 內全文模糊搜索，只能靠索引與模組錨點路由。** 若上游封裝時的 `> META-INDEX`／`Description`／`Trigger Context` 顆粒度不足、或模組切分不理想，Decoder 可能無法正確命中模組而回覆 Out of Scope；此情況需回到 Architect 重新分模組或加強索引描述（而非要求 Decoder 亂搜全文）。

### Q3：為何頁碼引用有時只能是 `N/A`，或不適用於人類看到的印刷頁碼？

**A：因為系統只支援 `PDF_Index`（PDF Viewer/讀取工具的絕對頁序）作為唯一頁碼真理來源。** 當輸入來源為 Text-Paste、純文字、或平台無法可靠提供頁序時，`PDF_Index` 必須填 `N/A`；同時系統不輸出/不推算印刷頁碼，因此人類若要用印刷頁碼定位，需自行在 PDF Viewer 內對照查找。



---
## ⚠️ 操作守則 (Operational Rules)

系統在輸出前會強制執行完整性檢查，重點包括：

1. **頁碼錨定（PDF_Index Only）**：

   * `PDF_Index` 必須取自 PDF Viewer／讀取工具顯示的絕對頁序；不得從正文推斷頁碼。
   * `PDF_Index` 不可得即填 `N/A`；不得猜測或補齊數字。
2. **結構完整 (Completeness)**：Module 必要 Metadata、引用行、分隔符齊備；不足即 Fail-Closed。
3. **格式無損保護 (Format Immunity)**：JSON/YAML/XML/Code Block 必須完整保留語法與縮排。
4. **禁止省略與佔位符 (Fail-Closed)**：命中模板 token／省略／佔位符即中止，要求縮小範圍或增加分拆重做。
5. **索引優先 (Index First)**：Decoder 必須先讀索引並合併增量索引，再跳轉讀取命中模組；嚴禁線性通讀。
6. **資料源邊界 (Data Boundary)**：回答只可使用命中模組的 `[Data Payload]`；缺資訊即回覆 Out of Scope。

---

## 📜 License

[MIT License](LICENSE)

---

**ASD Architect** - *不靠 LLM 線性通讀：以原文零改寫封裝為可路由 SSOT，依索引命中後精準跳轉並嚴格引用。*

