#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""PDF to Markdown converter for authorkit"""

import fitz  # pymupdf
import os
import sys
import re
from datetime import datetime

def extract_pdf_to_markdown(pdf_path, output_dir, ref_id):
    """Convert PDF to markdown with embedded images"""

    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    all_text = []
    image_count = 0
    headings_detected = 0

    print(f"Processing: {os.path.basename(pdf_path)}")
    print(f"Total pages: {total_pages}")

    for page_num in range(total_pages):
        page = doc[page_num]

        # Extract text
        text = page.get_text("text")

        # Extract images
        images = page.get_images()
        for img_idx, img in enumerate(images):
            try:
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)

                # Convert CMYK to RGB if needed
                if pix.n >= 5:
                    pix = fitz.Pixmap(fitz.csRGB, pix)

                img_filename = f"p{page_num+1:04d}_img{img_idx}.png"
                img_path = os.path.join(images_dir, img_filename)
                pix.save(img_path)
                image_count += 1

                # Add image reference to text
                text += f"\n\n![이미지 {page_num+1}-{img_idx}](images/{img_filename})\n"

            except Exception as e:
                print(f"  Warning: Could not extract image on page {page_num+1}: {e}")

        # Detect headings (lines that are likely headers)
        lines = text.split('\n')
        processed_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                processed_lines.append("")
                continue

            # Detect chapter/section patterns
            if re.match(r'^제?\s*\d+장', line) or re.match(r'^\d+\.\s+[가-힣]', line):
                processed_lines.append(f"\n## {line}\n")
                headings_detected += 1
            elif re.match(r'^\d+\.\d+\s+[가-힣]', line) or re.match(r'^[가-힣]+\s*\d+\.\s', line):
                processed_lines.append(f"\n### {line}\n")
                headings_detected += 1
            elif re.match(r'^\d+\.\d+\.\d+', line):
                processed_lines.append(f"\n#### {line}\n")
                headings_detected += 1
            else:
                processed_lines.append(line)

        page_text = '\n'.join(processed_lines)
        all_text.append(f"\n---\n<!-- Page {page_num+1} -->\n{page_text}")

        if (page_num + 1) % 50 == 0:
            print(f"  Processed {page_num + 1}/{total_pages} pages...")

    doc.close()

    # Write full markdown
    full_md = '\n'.join(all_text)
    full_md_path = os.path.join(output_dir, "full.md")
    with open(full_md_path, 'w', encoding='utf-8') as f:
        f.write(f"# {os.path.basename(pdf_path)}\n\n")
        f.write(f"> Converted: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(full_md)

    # Write conversion log
    log_path = os.path.join(output_dir, "conversion-log.md")
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f"# Conversion Log\n\n")
        f.write(f"- **Source**: {os.path.basename(pdf_path)}\n")
        f.write(f"- **Pages**: {total_pages}\n")
        f.write(f"- **Converted**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"- **Text characters**: {len(full_md):,}\n")
        f.write(f"- **Images extracted**: {image_count}\n")
        f.write(f"- **Headings detected**: {headings_detected}\n\n")
        f.write(f"## Output Files\n\n")
        f.write(f"- `full.md` - Complete converted content\n")
        f.write(f"- `images/` - Extracted images ({image_count} files)\n")

    print(f"\nConversion complete!")
    print(f"  Text: {len(full_md):,} characters")
    print(f"  Images: {image_count}")
    print(f"  Headings: {headings_detected}")
    print(f"  Output: {full_md_path}")

    return {
        'pages': total_pages,
        'characters': len(full_md),
        'images': image_count,
        'headings': headings_detected
    }

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python convert_pdf.py <pdf_path> <output_dir> <ref_id>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2]
    ref_id = sys.argv[3]

    extract_pdf_to_markdown(pdf_path, output_dir, ref_id)
