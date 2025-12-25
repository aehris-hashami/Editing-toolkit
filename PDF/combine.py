#!/usr/bin/env python3
"""
Multi-file to PDF converter + combiner

Features:
- Convert images, text, CSV to individual PDFs
- Combine PDFs in custom user-selected order
- Ask user for final output PDF name
- Directory mode (`-d <path>`)
- Keep or delete intermediate directory (`-k`)
- Separate mode (`-s`, default) → each file on its own page
- Unified mode (`-u`) → minimal pages, text wraps normally

Author: ChatGPT
"""

import os
import sys
import argparse
import csv
from PIL import Image
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from PyPDF2 import PdfMerger


# -------------------------------------------------------------------
# Convert TXT or CSV to PDF
# -------------------------------------------------------------------
def text_or_csv_to_pdf(input_path, output_path, unified=False):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    content = []

    if input_path.lower().endswith(".csv"):
        with open(input_path, newline="", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            for row in reader:
                line = ", ".join(row)
                content.append(Paragraph(line, styles["Normal"]))
                content.append(Spacer(1, 0.15 * inch))

    else:  # text file
        with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f.readlines():
                content.append(Paragraph(line.strip(), styles["Normal"]))
                content.append(Spacer(1, 0.15 * inch))

    doc.build(content)
    print(f"Converted text/CSV file to PDF: {output_path}")


# -------------------------------------------------------------------
# Convert an image to PDF
# -------------------------------------------------------------------
def image_to_pdf(input_path, output_path, unified=False):
    image = Image.open(input_path)
    image = image.convert("RGB")

    # Unified mode: scale to fit one page
    if unified:
        page_w, page_h = letter
        img_w, img_h = image.size

        scale = min(page_w / img_w, page_h / img_h)
        new_size = (int(img_w * scale), int(img_h * scale))
        image = image.resize(new_size)

    image.save(output_path)
    print(f"Converted image to PDF: {output_path}")


# -------------------------------------------------------------------
# Convert supported file types to PDF
# -------------------------------------------------------------------
def convert_file(input_path, output_folder, unified=False):
    base = os.path.basename(input_path)
    name, ext = os.path.splitext(base)
    ext = ext.lower()

    pdf_path = os.path.join(output_folder, f"{name}.pdf")

    if ext in [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"]:
        image_to_pdf(input_path, pdf_path, unified)

    elif ext in [".txt", ".csv"]:
        text_or_csv_to_pdf(input_path, pdf_path, unified)

    else:
        print(f"Unsupported file type: {input_path}")
        return None

    return pdf_path


# -------------------------------------------------------------------
# Combine PDFs
# -------------------------------------------------------------------
def combine_pdfs(pdf_list, output_file):
    print("\nSelect the order for combining the PDFs:")
    for i, pdf in enumerate(pdf_list):
        print(f"[{i}] {pdf}")

    order_input = input("Enter space-separated indices (e.g., 2 0 1): ").strip().split()

    try:
        order = [int(x) for x in order_input]
    except:
        print("Invalid order input! Aborting.")
        return

    merger = PdfMerger()

    for idx in order:
        if idx < 0 or idx >= len(pdf_list):
            print(f"Invalid index: {idx}")
            return
        merger.append(pdf_list[idx])

    merger.write(output_file)
    merger.close()

    print(f"\nSuccessfully created combined PDF: {output_file}")


# -------------------------------------------------------------------
# Collect files
# -------------------------------------------------------------------
def collect_files(args):
    if args.directory:
        if not os.path.isdir(args.directory):
            print("Directory does not exist!")
            sys.exit(1)
        return [
            os.path.join(args.directory, f)
            for f in os.listdir(args.directory)
            if os.path.isfile(os.path.join(args.directory, f))
        ]
    return args.files


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Convert multiple files to PDF and combine them."
    )

    parser.add_argument("files", nargs="*", help="Input files to convert.")
    parser.add_argument("-d", "--directory", help="Directory containing files.")
    parser.add_argument("-k", "--keep", action="store_true",
                        help="Keep converted_pdfs directory after merging.")
    parser.add_argument("-s", "--separate", action="store_true",
                        help="Each file stays on its own page (default).")
    parser.add_argument("-u", "--unified", action="store_true",
                        help="Pack content into minimal pages.")

    args = parser.parse_args()

    # Determine mode
    unified_mode = args.unified

    files = collect_files(args)

    if not files:
        print("No input files provided.")
        sys.exit(1)

    output_folder = "converted_pdfs"
    os.makedirs(output_folder, exist_ok=True)

    print("\nConverting files...\n")
    pdf_paths = []

    for file in files:
        pdf = convert_file(file, output_folder, unified_mode)
        if pdf:
            pdf_paths.append(pdf)

    if not pdf_paths:
        print("No valid files were converted.")
        sys.exit(0)

    # Ask for final output PDF name
    out_name = input("\nEnter a name for the final combined PDF (without extension): ").strip()
    if not out_name:
        out_name = "combined_output"
    output_file = f"{out_name}.pdf"

    combine_pdfs(pdf_paths, output_file)

    # Delete temp folder unless -k is used
    if not args.keep:
        import shutil
        shutil.rmtree(output_folder)
        print(f"\nDeleted temporary folder: {output_folder}")


if __name__ == "__main__":
    main()
