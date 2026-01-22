# ASD 智能文檔架構師 (ASD Document Architect)

> **Agent-Skill Driven Single Source of Truth (ASD-SSOT)**
> 專為 LLM 長文本檢索設計的高效、低幻覺風險、結構化封裝系統。

![Version](https://img.shields.io/badge/Version-v1.7.2-blue.svg) ![Language](https://img.shields.io/badge/Language-Traditional%20Chinese-green.svg) ![License](https://img.shields.io/badge/License-MIT-orange.svg)

## 📖 專案簡介

本專案由兩個 System Prompt 組成，建議按次序使用：

1) **`prompt_ASD_Document_Architect.md`（Architect｜封裝器）**  
把原始長文檔（PDF / Markdown / Word）封裝為可路由的 **ASD-SSOT**：  
- **封裝而非摘要**：以「原文零改寫、零刪減」為設計目標，並以 Fail-Closed 作為指令級約束  
- 生成可路由的 `> META-INDEX:` 與模組化 `## [MODULE X]`  
- 在超出單次輸出上限時，支援多卷（Part 1 / Part N）物理分拆與增量索引更新  
- 讀取受限或工具截斷時，可轉入 Text-Paste 分批處理（只處理下一個可驗收批次）

2) **`prompt_ASD Decoder.md`（Decoder｜解碼器）**  
用於問答與檢索：先讀索引、精準跳轉命中模組、只用命中模組的 `[Data Payload]` 回答，並附上 **PDF_Index** 頁碼引用（Fail-Closed）。如需審計/回測，可額外輸出 `AUDIT_EVIDENCE_PACK`（逐條主張綁定 Evidence ID、來源檔與可回查片段）。如只提供 Master Knowledge Index 而未提供對應 ASD 檔案/分卷，系統會中止並要求補檔（Fail-Closed）。

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

* **封裝而非摘要（Fail-Closed）**：以「原文全量轉錄」為目標；一旦鎖定頁碼範圍，系統以零容忍規則限制省略／佔位符／模板殘留，命中即中止以避免污染。
* **Preflight（先探測再重工）**：在進入重型封裝前先探測是否能讀取目標範圍內容；若平台/權限導致讀不到內文，立即切換 Text-Paste 模式，避免先做大量分卷計算後才發現不可讀。
* **容量估算與分卷規劃（Sizing Worksheet）**：以可展示算式的方式估算 Parts 範圍；不足時只允許縮範圍或物理分拆，不允許以摘要替代。
* **無限長度物理分拆（Part 1 / Part N）**：自動輸出可無縫拼接的多卷結構；Part 1 含全域索引，後續 Part 只輸出正文；新增模塊以 `> META-INDEX UPDATE:` 追加。
* **支援非連續頁碼範圍（Scope by Selection）**：可按需求選取多段頁碼範圍，逐段估算與封裝；結果以模塊化輸出便於分段驗收。
* **單層頁碼錨定（PDF_Index Only）**：所有引用一律使用 `PDF_Index`（PDF Viewer／讀取工具顯示的絕對頁序）作為唯一真理來源；不輸出、不推算印刷頁碼。
* **先路由、後讀取（Index → Jump → Cite）**：Decoder 先掃描 `> META-INDEX:`／合併 `> META-INDEX UPDATE:`，命中模組後才跳轉讀取；嚴禁線性通讀與 Payload 內文全文模糊搜索。
* **可審計引用（Evidence Pack）**：除 Inline `[Source: PDF_Index P.(實際值或 N/A)]` 外，可輸出 `AUDIT_EVIDENCE_PACK`，逐條主張綁定 Evidence ID、來源檔、模塊錨點與可回查片段，便於下游回測與審計。
* **下游整合友善**：可直接配合 RAG / Agent / 另一個 Chat session；文件自帶索引與模組錨點，易於機械化定位與審計。

> **重要提示（驗收與免責）**：ASD 以「指令級」方式要求零損耗，但 LLM 在實際執行仍可能受工具權限、輸出截斷、OCR 品質、表格跨頁等因素影響。建議對輸出結果進行人手抽樣校對與結構性驗收（見下文「操作守則」與「已知問題」）。

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
   * 如同時提供 Master Knowledge Index：仍必須一併提供索引中引用到的對應 ASD 檔案/分卷；否則 Decoder 會中止並要求補檔（Fail-Closed）。
4. 提出問題；Decoder 會：
   * 先掃描 `> META-INDEX:`（並合併 `> META-INDEX UPDATE:`）
   * 再以 `## [MODULE X]` 精準跳轉
   * 最後只用命中模組的 `[Data Payload]` 回答，並附上 `[Source: PDF_Index P.(實際值或 N/A)]` 引用；如需審計/回測，會額外輸出 `AUDIT_EVIDENCE_PACK`（Evidence ID 對照每條主張的可回查片段）

### 4. 實測摘要（範例：Gemini 3.0 Pro (網頁版)）
以下為一次實測的流程摘要，用於說明 ASD 在「超長 PDF + 非連續頁碼 + 工具截斷」情境下的可行運作方式（不構成對所有平台/所有文件的保證）：
- 輸入：200+ 頁 PDF；選取非連續的多段頁碼範圍
- 執行：按 MODE A 自動物理分拆（每檔約 1,000 行量級），可人工 copy-paste 合併為單一 `.md`
- 途中：曾出現工具截斷（Tool Truncation），依指令轉入 Text-Paste 分批補齊後完成封裝
- 後續：按 MODE B 提取各模塊 Trigger Context 與 Entity Inventory，生成 Master Knowledge Index（`.md`）
- 完成品及測試檔見 'sample_doc' 目錄

**實測摘要 : Result of Scope Audit Report（範圍審計報告）**：
| 模塊 (Module) | 您要求的範圍 (Requested) | 實際執行的範圍 (Executed) | 讀取方式 (Method) |
|---|---|---|---|
| Module A（財務三表） | P.109 – P.114 | ✅ P.109 – P.114（完整） | 📄 直接讀取 PDF（Tool Read） |
| Module B（關鍵附註） | P.126 – P.145 | ✅ P.126 – P.145（完整） | 📄 直接讀取 PDF（Tool Read） |
| Module C（估值報告） | P.171 – P.190 | ✅ P.171 – P.190（完整） | 📋 手動貼上（Text-Paste） |
| Module D（五年摘要） | P.231 – P.232 | ✅ P.231 – P.232（完整） | 📋 手動貼上（Text-Paste） |

**實測摘要 : 結論（示例性表述）**：審計結果顯示，上述實測輸出在邏輯範圍上覆蓋了原先指定的模塊與頁碼；但仍建議以人手抽樣校對與結構性驗收作最後把關。


---

## 📂 ASD 輸出格式範例 (Output Structure)

ASD 生成的文檔具備 **自解釋性** 與 **高顆粒度**，自動輸出包含給下游 AI 的精細化指令：

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

（此處為原文轉錄的內容，保留表格、附註與格式。）

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
4. 最後提出問題；Decoder 會依 `> META-INDEX` 路由並精準跳轉，並提供 `PDF_Index` 頁碼引用；如需審計/回測，會額外輸出 `AUDIT_EVIDENCE_PACK` 供下游重放核對。

---

## 🗨️ 已知問題　(Q&A)

### Q1：為何有時候封裝到一半會被迫中止，不能「先輸出再補」？

**A：因為系統採用 Fail-Closed。** 一旦偵測到讀取不連續、工具回傳空值/截斷、或輸出中出現任何省略/佔位符風險，Architect 必須立即中止以避免污染；此情況只能透過縮小頁碼範圍、增加物理分拆、重上載/重試，或改用 Text-Paste 分批處理來解決。

### Q2：為何 Decoder 有時答「Out of Scope」，但明明內容可能在文檔某處？

**A：因為 Decoder 嚴禁在 Payload 內全文模糊搜索，只能靠索引與模組錨點路由。** 若上游封裝時的 `> META-INDEX`／`Description`／`Trigger Context` 顆粒度不足、或模組切分不理想，Decoder 可能無法正確命中模組而回覆 Out of Scope；此情況需回到 Architect 重新分模組或加強索引描述（而非要求 Decoder 亂搜全文）。

### Q3：為何頁碼引用有時只能是 `N/A`？

**A：因為系統只支援 `PDF_Index`（PDF Viewer/讀取工具的絕對頁序）作為唯一頁碼真理來源。** 當輸入來源為 Text-Paste、純文字、或平台無法可靠提供頁序時，`PDF_Index` 必須填 `N/A`。

### Q4：載入 PDF 時，如何提升讀取成功率與效能？

**A：建議優先使用「文字可被選取」的 PDF（內含文字層），避免純圖片掃描。** 純圖片 PDF 通常需要 OCR，會增加讀取失真、表格結構錯位與耗時風險；如文件只提供掃描件，建議先以 OCR 工具生成可選取文字版本，再交由 Architect 封裝。

### Q5：為何我已提供 Master Knowledge Index，Decoder 仍要求我補交某些 ASD 檔案/分卷？

**A：因為 Master Knowledge Index 只是一份路由表，並不包含原文 Payload。** Decoder 必須以索引定位到目標模塊後，讀取對應 ASD 檔案中的 `[Data Payload]` 才能回答；若索引引用到的檔案/分卷未被實際提供，系統會中止並要求補檔（Fail-Closed），以避免憑印象補全或引用漂移。

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
7. **人手驗收建議（推薦）**：對關鍵表格、數字與條款段落進行抽樣校對；並檢查是否存在截斷、重覆片段、或結構性缺件（分隔符／引用行／Metadata 欄位）。

---

## 📜 License

[MIT License](LICENSE)

---

**ASD Architect** - *不靠 LLM 線性通讀：以原文零改寫封裝為可路由 SSOT，依索引命中後精準跳轉並嚴格引用。*

