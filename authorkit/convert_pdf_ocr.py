#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""PDF to Markdown converter using PaddleOCR for Korean text extraction"""

import fitz  # pymupdf
import os
import sys
import re
import tempfile
from datetime import datetime
from pathlib import Path

def extract_pdf_with_ocr(pdf_path, output_dir, ref_id):
    """Convert PDF to markdown using PaddleOCR for better Korean text extraction"""

    from paddleocr import PaddleOCR

    # Initialize PaddleOCR with Korean + English (v2.9 API)
    ocr = PaddleOCR(use_angle_cls=True, lang='korean', use_gpu=True, show_log=False)

    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    all_text = []
    image_count = 0
    headings_detected = 0

    print(f"Processing: {os.path.basename(pdf_path)}")
    print(f"Total pages: {total_pages}")
    print(f"Using PaddleOCR (Korean + GPU)")

    for page_num in range(total_pages):
        page = doc[page_num]

        # Try pymupdf text extraction first
        raw_text = page.get_text("text").strip()

        # If text is too short or has garbled chars, use OCR
        korean_ratio = len(re.findall(r'[가-힣]', raw_text)) / max(len(raw_text), 1)
        use_ocr = len(raw_text) < 50 or korean_ratio < 0.05

        if use_ocr:
            # Render page as image for OCR
            mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better OCR
            pix = page.get_pixmap(matrix=mat)
            img_path = os.path.join(tempfile.gettempdir(), f"ocr_page_{page_num}.png")
            pix.save(img_path)

            # Run PaddleOCR
            result = ocr.ocr(img_path, cls=True)
            ocr_lines = []
            if result and result[0]:
                for line in result[0]:
                    text_content = line[1][0]
                    confidence = line[1][1]
                    if confidence > 0.5:
                        ocr_lines.append(text_content)
            text = '\n'.join(ocr_lines)
            os.remove(img_path)
        else:
            text = raw_text

        # Extract embedded images
        page_images = page.get_images()
        for img_idx, img in enumerate(page_images):
            try:
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n >= 5:
                    pix = fitz.Pixmap(fitz.csRGB, pix)

                # Skip tiny images (likely decorative)
                if pix.width < 50 or pix.height < 50:
                    continue

                img_filename = f"p{page_num+1:04d}_img{img_idx}.png"
                img_path_save = os.path.join(images_dir, img_filename)
                pix.save(img_path_save)
                image_count += 1
                text += f"\n\n![이미지 {page_num+1}-{img_idx}](images/{img_filename})\n"
            except Exception as e:
                print(f"  Warning: Image extraction failed on page {page_num+1}: {e}")

        # Detect headings
        lines = text.split('\n')
        processed_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                processed_lines.append("")
                continue

            # Korean chapter/section patterns
            if re.match(r'^제?\s*\d+장', line) or re.match(r'^제?\s*[IVX]+\s*[\.장]', line):
                processed_lines.append(f"\n## {line}\n")
                headings_detected += 1
            elif re.match(r'^\d+\.\s+[가-힣A-Z]', line):
                processed_lines.append(f"\n## {line}\n")
                headings_detected += 1
            elif re.match(r'^\d+\.\d+\s+[가-힣A-Z]', line) or re.match(r'^[가-힣]+\s*\d+\.\s', line):
                processed_lines.append(f"\n### {line}\n")
                headings_detected += 1
            elif re.match(r'^\d+\.\d+\.\d+', line):
                processed_lines.append(f"\n#### {line}\n")
                headings_detected += 1
            else:
                processed_lines.append(line)

        page_text = '\n'.join(processed_lines)
        all_text.append(f"\n---\n<!-- Page {page_num+1} -->\n{page_text}")

        if (page_num + 1) % 10 == 0:
            print(f"  Processed {page_num + 1}/{total_pages} pages...")

    doc.close()

    # Write full markdown
    full_md = '\n'.join(all_text)
    full_md_path = os.path.join(output_dir, "full.md")
    with open(full_md_path, 'w', encoding='utf-8') as f:
        f.write(f"# {os.path.basename(pdf_path)}\n\n")
        f.write(f"> Converted: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"> OCR Engine: PaddleOCR (Korean + GPU)\n\n")
        f.write(full_md)

    # Write conversion log
    log_path = os.path.join(output_dir, "conversion-log.md")
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f"# Conversion Log\n\n")
        f.write(f"- **Source**: {os.path.basename(pdf_path)}\n")
        f.write(f"- **Ref ID**: {ref_id}\n")
        f.write(f"- **Pages**: {total_pages}\n")
        f.write(f"- **Converted**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"- **OCR Engine**: PaddleOCR (Korean + GPU)\n")
        f.write(f"- **Text characters**: {len(full_md):,}\n")
        f.write(f"- **Images extracted**: {image_count}\n")
        f.write(f"- **Headings detected**: {headings_detected}\n")

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
        print("Usage: python convert_pdf_ocr.py <pdf_path> <output_dir> <ref_id>")
        print("\nBatch mode:")
        print("  python convert_pdf_ocr.py --batch <pdf_dir> <output_base_dir> <start_ref_num>")
        sys.exit(1)

    if sys.argv[1] == "--batch":
        pdf_dir = sys.argv[2]
        output_base = sys.argv[3]
        start_num = int(sys.argv[4])

        pdf_files = sorted([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])
        print(f"Found {len(pdf_files)} PDF files:")
        for i, f in enumerate(pdf_files):
            print(f"  ref-{start_num+i:03d}: {f}")
        print()

        results = {}
        for i, pdf_file in enumerate(pdf_files):
            ref_id = f"ref-{start_num+i:03d}"
            pdf_path = os.path.join(pdf_dir, pdf_file)
            out_dir = os.path.join(output_base, ref_id)
            os.makedirs(out_dir, exist_ok=True)

            print(f"\n{'='*60}")
            print(f"[{i+1}/{len(pdf_files)}] {ref_id}: {pdf_file}")
            print(f"{'='*60}")

            result = extract_pdf_with_ocr(pdf_path, out_dir, ref_id)
            results[ref_id] = {**result, 'filename': pdf_file}

        # Print summary
        print(f"\n{'='*60}")
        print("BATCH CONVERSION SUMMARY")
        print(f"{'='*60}")
        for ref_id, info in results.items():
            print(f"  {ref_id}: {info['filename']}")
            print(f"    Pages: {info['pages']} | Chars: {info['characters']:,} | Images: {info['images']} | Headings: {info['headings']}")
    else:
        pdf_path = sys.argv[1]
        output_dir = sys.argv[2]
        ref_id = sys.argv[3]
        os.makedirs(output_dir, exist_ok=True)
        extract_pdf_with_ocr(pdf_path, output_dir, ref_id)
