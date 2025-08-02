# pdf_parser/extract_text.py

import json
import os
import requests
import fitz  # PyMuPDF
from tqdm import tqdm

INPUT_FILE = "../data/rvce_pages.json"
OUTPUT_FILE = "../data/rvce_pages_with_pdfs.json"

def download_pdf(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and "application/pdf" in response.headers.get("Content-Type", ""):
            return response.content
    except Exception as e:
        print(f"[ERROR] Failed to download {url} -> {e}")
    return None

def extract_text_from_pdf_bytes(pdf_bytes):
    try:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            return text.strip()
    except Exception as e:
        print(f"[ERROR] Failed to extract text -> {e}")
        return ""

def run():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        pages = json.load(f)

    pdf_links = set()
    for page in pages:
        if ".pdf" in page["url"].lower():
            pdf_links.add(page["url"])

    print(f"[INFO] Found {len(pdf_links)} PDF URLs")

    pdf_items = []

    for url in tqdm(sorted(pdf_links)):
        pdf_bytes = download_pdf(url)
        if pdf_bytes:
            content = extract_text_from_pdf_bytes(pdf_bytes)
            if content:
                pdf_items.append({
                    "url": url,
                    "title": os.path.basename(url),
                    "content": content
                })

    print(f"[INFO] Successfully extracted {len(pdf_items)} PDFs")

    # Merge and write output
    merged = pages + pdf_items
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    print(f"[DONE] Final output saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    run()
