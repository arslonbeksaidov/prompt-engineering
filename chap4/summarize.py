import pymupdf
import os

pdf_file_path = "chap4/data/invoicesample.pdf"
doc = pymupdf.open(pdf_file_path)

full_text = ''

# Loop through document pages
for page in doc:
    text = page.get_text()  # Extract page text
    full_text += text

# Remove file extension
pdf_file_name = os.path.basename(pdf_file_path)
pdf_file_name = os.path.splitext(pdf_file_name)[0]

# Save as text file
txt_file_path = f"chap4/output/{pdf_file_name}.txt"
with open(txt_file_path, 'w', encoding='utf-8') as f:
    f.write(full_text)
