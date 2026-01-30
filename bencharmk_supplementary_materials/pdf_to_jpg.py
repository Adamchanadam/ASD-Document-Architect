import fitz  # PyMuPDF
import os

# PDF 文件路徑
pdf_path = r"D:\_Adam_Projects\AI\ASD 智能文檔架構師\bencharmk_supplementary_materials\ASD_Research_Report_Scorecard_2026_01_27.pdf"

# 打開 PDF
pdf_document = fitz.open(pdf_path)

# 獲取 PDF 文件名（不含擴展名）
pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

# 創建輸出目錄
output_dir = os.path.join(os.path.dirname(pdf_path), f"{pdf_name}_pages")
os.makedirs(output_dir, exist_ok=True)

print(f"PDF 總共有 {len(pdf_document)} 頁")
print(f"輸出目錄: {output_dir}")

# 遍歷每一頁
for page_num in range(len(pdf_document)):
    # 獲取頁面
    page = pdf_document[page_num]

    # 設置縮放比例以提高圖片質量（2.0 表示 2 倍分辨率）
    zoom = 2.0
    mat = fitz.Matrix(zoom, zoom)

    # 將頁面渲染為圖片
    pix = page.get_pixmap(matrix=mat)

    # 生成輸出文件名（從 1 開始編號）
    output_filename = os.path.join(output_dir, f"{pdf_name}_page_{page_num + 1:03d}.jpg")

    # 保存為 JPG
    pix.save(output_filename)

    print(f"已保存: {os.path.basename(output_filename)}")

# 關閉 PDF
pdf_document.close()

print(f"\n完成！所有圖片已保存到: {output_dir}")
