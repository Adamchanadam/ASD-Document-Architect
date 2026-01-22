# ASD 智能文檔架構師 (ASD Document Architect)

> **Agent-Skill Driven Single Source of Truth (ASD-SSOT)**
> 專為 LLM 長文本檢索設計的高效、低幻覺風險、結構化封裝系統。

![Version](https://img.shields.io/badge/Version-v1.7.2-blue.svg) ![Language](https://img.shields.io/badge/Language-Traditional%20Chinese-green.svg) ![License](https://img.shields.io/badge/License-MIT-orange.svg)

## 📖 專案簡介

🔎 ASD 的用途很直接：先把長文檔整理成「可定位、可分段、可引用」的結構化檔案，再用同一套結構做問答與審計。

本專案由兩個 System Prompt 組成，建議按次序使用：

1) **`prompt_ASD_Document_Architect.md`（Architect｜封裝器）**  
將原始長文檔（PDF / Markdown / Word）整理成可檢索的 **ASD-SSOT**。封裝完成後，文檔會被切分成多個「模塊」，並附上一份索引，令下游讀取不必線性通讀整份文件。

2) **`prompt_ASD Decoder.md`（Decoder｜解碼器）**  
用於問答與檢索。Decoder 會先看索引，再跳到相關模塊，只使用命中模塊的內容回答，並提供 **`PDF_Index`** 頁碼引用（若平台無法提供頁碼，則以 `N/A` 代表）。如需審計/回測，可額外輸出 `AUDIT_EVIDENCE_PACK`（把每條主張拆開並綁定可回查片段）。如只提供 Master Knowledge Index 而未提供對應 ASD 檔案/分卷，系統會中止並要求補檔，以避免「沒有原文仍作答」造成引用漂移。

**ASD 的核心目標是降低 LLM 處理長文檔常見風險：**
- 把長文閱讀改成「先看索引，再只讀相關段落」，減少一次要處理的內容量，從而降低漏讀與跳步機率。  
- 檢索迷失（Lost-in-the-middle）  
- 內容幻覺（憑印象補全、引用漂移、頁碼亂填）


### 立即體驗（Gemini DEMO）
如需最快體驗，可直接使用以下 Gemini Gems（可能需要登入 Google 帳戶）：
- 📜 **ASD 智能文檔架構師 (ASD Document Architect)**：https://gemini.google.com/gem/1Us9GWj3H4nYNvbd_2drZUMqfuJni_8MK?usp=sharing
- 📜 **ASD-SSOT Decoder (ASD 智能解碼器)**：https://gemini.google.com/gem/1oMZeRZ-LLayNZoUZuiqSUgavZ6PN6FFY?usp=sharing

---

## 💎 關鍵功能 (Key Features)

🔎 ASD 並非讓模型「更聰明地讀」，而是用結構設計降低「讀錯、漏讀、亂引用」的機會。

* **封裝而非摘要**：以「原文全量轉錄」為目標；一旦鎖定頁碼範圍，系統會以零容忍規則限制省略／佔位符／模板殘留，避免把不完整內容當作可靠資料。
* **先確認能讀到，再開始重工**：在進入大量封裝前，先測試是否能讀取目標範圍；若平台/權限導致讀不到內文，會轉入 Text-Paste 分批處理，避免先做大量分拆規劃後才發現不可讀。
* **支援超長文件與分段封裝**：當單次輸出不足以容納內容時，可自動分拆為多個 Part；亦可按需求選取多段（非連續）頁碼範圍，逐段封裝，便於分段驗收。
* **單層頁碼錨定（PDF_Index Only）**：所有引用一律使用 `PDF_Index`（PDF Viewer／讀取工具顯示的絕對頁序）作為唯一真理來源；不輸出、不推算印刷頁碼；不可得則填 `N/A`。
* **先定位、後閱讀（Index → Jump → Cite）**：Decoder 先看索引，再跳到相關模塊閱讀，避免在整份文件「亂翻」而誤命中。
* **可審計引用（Evidence Pack）**：除 Inline `[Source: PDF_Index P.(實際值或 N/A)]` 外，可輸出 `AUDIT_EVIDENCE_PACK`，逐條主張綁定 Evidence ID、來源檔、模塊錨點與可回查片段，便於下游回測與審計。
* **下游整合友善**：可直接配合 RAG / Agent / 另一個 Chat session；文件自帶索引與模塊錨點，適合機械化定位與審計。

> **重要提示（驗收與免責）**：ASD 以「指令級」方式要求零損耗，但 LLM 在實際執行仍可能受工具權限、輸出截斷、OCR 品質、表格跨頁等因素影響。建議把「人手抽樣校對與結構性驗收」視為流程一部分（見下文「操作守則」與「已知問題」）。

---

## 🧾 術語速讀（新手友善）

🔎 以下術語只需理解一次，其後閱讀整份 README 即可自洽。

- **ASD-SSOT**：由 Architect 產出的結構化文檔，包含索引與多個模塊，便於定位與引用。
- **模塊（Module）**：把原文按邏輯切分的段落單位；Decoder 只會讀取命中的模塊，避免無關內容干擾。
- **索引（Index / Master Knowledge Index）**：一份「路由表」，用來告訴 Decoder 相關內容在哪個模塊；索引本身不包含原文內容。
- **`PDF_Index`**：PDF Viewer／讀取工具顯示的絕對頁序；如平台無法可靠提供頁序，則以 `N/A` 表示。
- **Text-Paste**：當平台讀取 PDF 失敗或截斷時，改用手動貼上文字分批處理的方式。
- **`AUDIT_EVIDENCE_PACK`**：可選的審計輸出，把答案拆成「主張 → 證據片段 → 出處」的對照表，便於回測。

---

## 🛠️ 使用方法 (Usage)

🔎 最簡單的理解方式：先用 Architect 把「長文」變成「可定位的結構化檔案」，再用 Decoder 以「索引 → 跳轉 → 引用」方式問答。

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
   * **MODE B（建立 Master Knowledge Index）**：在已保存多份 ASD-SSOT 後，用檔名清單與必要輸入建立可跳轉的總索引；若缺必要輸入將直接中止。
4. 將輸出保存為 `*_ASD-SSOT.md`；如為物理分拆，保存為多個 `_PartN.md` 檔案；MODE B 的輸出另存為獨立索引檔。

### 3. Step B — 以 Decoder 問答（先索引、後跳轉、再引用）
1. 另開一個 **New Chat**（建議與 Architect 分開，確保解碼器只以 ASD-SSOT 為唯一資料源）。
2. 貼上 `prompt_ASD Decoder.md` 全文並發送。
3. 提供剛生成的 ASD-SSOT：
   * 若是分拆檔：先提供 Part 1，按需要再依序提供 Part 2、Part 3……
   * 若同時提供多個 ASD 檔案：Decoder 會先分別建立路由，再合併候選模塊後逐一跳轉。
   * 如同時提供 Master Knowledge Index：仍必須一併提供索引中引用到的對應 ASD 檔案/分卷；否則 Decoder 會中止並要求補檔。
4. 提出問題；Decoder 會提供：
   * **答案（只使用命中模塊內容）**
   * **頁碼引用**：`[Source: PDF_Index P.(實際值或 N/A)]`
   * **可選審計包**：`AUDIT_EVIDENCE_PACK`（Evidence ID 對照每條主張的可回查片段）

---

## ✅ 實測摘要（範例：Gemini 3.0 Pro（網頁版））

🔎 以下為一次實測的流程摘要，用於說明 ASD 在「超長 PDF + 非連續頁碼 + 工具截斷」情境下的可行運作方式；不構成對所有平台/所有文件的保證。

- 輸入：200+ 頁 PDF；選取非連續的多段頁碼範圍
- 執行：按 MODE A 自動物理分拆（每檔約 1,000 行量級），可人工 copy-paste 合併為單一 `.md`
- 途中：曾出現工具截斷（Tool Truncation），依指令轉入 Text-Paste 分批補齊後完成封裝
- 後續：按 MODE B 提取各模塊 Trigger Context 與 Entity Inventory，生成 Master Knowledge Index（`.md`）
- 如倉庫內提供 `sample_doc` 目錄（示例文件），可用作對照參考與教學演示

**Scope Audit Report（範圍審計報告）**：
| 模塊 (Module) | Requested | Executed | Method |
|---|---|---|---|
| Module A（財務三表） | P.109 – P.114 | ✅ P.109 – P.114（完整） | 📄 直接讀取 PDF（Tool Read） |
| Module B（關鍵附註） | P.126 – P.145 | ✅ P.126 – P.145（完整） | 📄 直接讀取 PDF（Tool Read） |
| Module C（估值報告） | P.171 – P.190 | ✅ P.171 – P.190（完整） | 📋 手動貼上（Text-Paste） |
| Module D（五年摘要） | P.231 – P.232 | ✅ P.231 – P.232（完整） | 📋 手動貼上（Text-Paste） |

**結論（示例性表述）**：審計結果顯示，上述實測輸出在邏輯範圍上覆蓋了原先指定的模塊與頁碼；但仍建議以人手抽樣校對與結構性驗收作最後把關。

---

## 📂 ASD 輸出格式範例 (Output Structure)

🔎 ASD 的輸出重點不在「漂亮排版」，而在「索引可定位、模塊可跳轉、引用可回查」，令下游讀取更可靠。

```markdown
# [ROOT] 範例文檔（Consolidated）

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

（此處為原文轉錄的內容，保留表格、附註與格式。）

[Source: PDF_Index P.12]

---
========== [MODULE SEPARATOR] ==========
---
````

---

## 🤖 下游 AI 整合 (Downstream Integration)

🔎 下游整合的核心做法很簡單：先給 Decoder Prompt，再給 ASD-SSOT 檔案，最後提問；需要嚴格審計時，再要求輸出 `AUDIT_EVIDENCE_PACK`。

* **Decoder Prompt**：`prompt_ASD Decoder.md`

**建議流程**：

1. 在新對話中貼上 Decoder Prompt。
2. 提供由 Architect 生成的 ASD-SSOT（先提供 Part 1）。
3. 如有續章，依序提供 Part 2、Part 3……
4. 最後提出問題；Decoder 會依索引路由並精準跳轉，並提供 `PDF_Index` 頁碼引用；如需審計/回測，會額外輸出 `AUDIT_EVIDENCE_PACK` 供下游重放核對。

---

## 🗨️ 已知問題　(Q&A)

### Q1：為何有時候封裝到一半會被迫中止，不能「先輸出再補」？

**A：ASD 以「寧可中止，也不輸出可能不完整內容」作為保護機制。** 當偵測到讀取不連續、工具回傳空值/截斷、或輸出中出現任何省略/佔位符風險時，封裝會被中止以避免污染；此情況通常只能透過縮小頁碼範圍、增加物理分拆、重上載/重試，或改用 Text-Paste 分批處理來解決。

### Q2：為何 Decoder 有時答「Out of Scope」，但內容可能在文檔某處？

**A：Decoder 不會在整份 Payload 內「亂搜全文」，而是依索引與模塊跳轉。** 若上游封裝時的索引描述顆粒度不足、或模塊切分不理想，Decoder 可能無法命中正確模塊而回覆 Out of Scope；此情況通常需要回到 Architect 改善索引描述或調整模塊切分。

### Q3：為何頁碼引用有時只能是 `N/A`？

**A：因為系統只把 `PDF_Index` 視為可靠頁碼來源。** 當輸入來源為 Text-Paste、純文字、或平台無法可靠提供頁序時，`PDF_Index` 會以 `N/A` 表示，避免猜測或補齊造成「看似合規、實則不可回查」的引用。

### Q4：載入 PDF 時，如何提升讀取成功率與效能？

**A：建議優先使用「文字可被選取」的 PDF（內含文字層），避免純圖片掃描。** 純圖片 PDF 通常需要 OCR，會增加讀取失真、表格結構錯位與耗時風險；如文件只提供掃描件，建議先以 OCR 工具生成可選取文字版本，再交由 Architect 封裝。

### Q5：為何已提供 Master Knowledge Index，Decoder 仍要求補交某些 ASD 檔案/分卷？

**A：因為 Master Knowledge Index 只是一份路由表，並不包含原文內容。** Decoder 必須在定位到目標模塊後，讀取對應 ASD 檔案中的原文內容才可回答；若索引引用到的檔案/分卷未被實際提供，系統會中止並要求補檔，以避免憑印象補全或引用漂移。

---

## ⚠️ 操作守則 (Operational Rules)

🔎 最可靠的使用方式，是把 ASD 視為「結構化封裝＋可回查引用」，再以抽樣校對完成最後驗收，而非把任何平台輸出當作天然無誤。

系統在輸出前會強制執行完整性檢查，重點包括：

1. **頁碼錨定（PDF_Index Only）**：

   * `PDF_Index` 必須取自 PDF Viewer／讀取工具顯示的絕對頁序；不得從正文推斷頁碼。
   * `PDF_Index` 不可得即填 `N/A`；不得猜測或補齊數字。
2. **結構完整 (Completeness)**：模塊必要 Metadata、引用行、分隔符齊備；不足即中止，以免輸出不可回查內容。
3. **格式保護 (Format Immunity)**：JSON/YAML/XML/Code Block 應完整保留語法與縮排，避免下游解析失敗。
4. **避免省略與佔位符**：一旦出現省略/佔位符/模板殘留，應縮小範圍或增加分拆重做，而非在不完整內容上繼續推理。
5. **索引優先 (Index First)**：Decoder 應先讀索引，再跳轉讀取命中模塊；不建議線性通讀整份文件。
6. **資料源邊界 (Data Boundary)**：回答只使用命中模塊的原文內容；缺資訊則回覆 Out of Scope。
7. **人手驗收建議（推薦）**：對關鍵表格、數字與條款段落進行抽樣校對；並檢查是否存在截斷、重覆片段、或結構性缺件（分隔符／引用行／Metadata 欄位）。

---

## 📜 License

[MIT License](LICENSE)

---

**ASD Architect** - *不靠 LLM 線性通讀：以原文封裝為可路由 SSOT，依索引命中後精準跳轉並提供可回查引用。*
