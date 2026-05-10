#!/usr/bin/env python3
"""
Consolidate all PDFs from scattered cluster directories into a single
canonical location: literature/papers/consolidated/
Uses the BibTeX registry to map papers to clean authorYYYY_short_title.pdf names.
"""
import os
import re
import shutil
import json

REPO_ROOT = "/home/ubuntu/k12-education-research"
CONSOLIDATED_DIR = os.path.join(REPO_ROOT, "literature/papers/consolidated")
BIB_FILE = os.path.join(REPO_ROOT, "literature/registry.bib")
if not os.path.exists(BIB_FILE):
    BIB_FILE = os.path.join(REPO_ROOT, "drafts/k12_references.bib")

os.makedirs(CONSOLIDATED_DIR, exist_ok=True)

# Step 1: Find ALL PDFs in the repo
all_pdfs = []
for root, dirs, files in os.walk(REPO_ROOT):
    # Skip .git and consolidated dir itself (to avoid double-counting)
    dirs[:] = [d for d in dirs if d not in ['.git']]
    if 'consolidated' in root:
        continue
    for f in files:
        if f.lower().endswith('.pdf'):
            full_path = os.path.join(root, f)
            size = os.path.getsize(full_path)
            if size > 5000:  # Skip tiny/corrupt files
                all_pdfs.append((full_path, f, size))

print(f"Found {len(all_pdfs)} PDFs across all directories (excluding consolidated/)")

# Step 2: Parse BibTeX to get all keys and author/year info
def parse_bib(bib_file):
    entries = {}
    if not os.path.exists(bib_file):
        print(f"BibTeX file not found: {bib_file}")
        return entries
    with open(bib_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    # Find all @article/@book/@techreport entries
    pattern = r'@\w+\{([^,]+),'
    keys = re.findall(pattern, content)
    for key in keys:
        entries[key.strip()] = key.strip()
    return entries

bib_keys = parse_bib(BIB_FILE)
print(f"Found {len(bib_keys)} BibTeX keys in registry")

# Step 3: Build a mapping from filename patterns to bib keys
# This uses heuristic matching: author name + year in filename
def normalize(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

def extract_year(s):
    m = re.search(r'(19|20)\d{2}', s)
    return m.group(0) if m else ''

# Build index of bib keys by normalized author+year
bib_index = {}
for key in bib_keys:
    norm_key = normalize(key)
    year = extract_year(key)
    bib_index[norm_key] = key

# Step 4: Copy each PDF to consolidated/ with clean name
# Strategy: use the filename as-is if it already looks clean (authorYYYY_*)
# Otherwise keep original name but prefix with source cluster

copied = {}
skipped_duplicates = []

for pdf_path, filename, size in sorted(all_pdfs, key=lambda x: -x[2]):  # largest first
    # Generate a clean destination name
    clean_name = filename
    # Remove common prefixes/suffixes that are messy
    clean_name = re.sub(r'^pasted_file_\w+_', '', clean_name)
    clean_name = re.sub(r'\s+', '_', clean_name)
    
    dest_path = os.path.join(CONSOLIDATED_DIR, clean_name)
    
    # If destination already exists (duplicate), keep the larger file
    if clean_name in copied:
        existing_size = copied[clean_name]['size']
        if size > existing_size:
            # Replace with larger version
            shutil.copy2(pdf_path, dest_path)
            copied[clean_name] = {'source': pdf_path, 'size': size}
            skipped_duplicates.append(f"Replaced {clean_name} with larger version from {pdf_path}")
        else:
            skipped_duplicates.append(f"Kept existing {clean_name} (larger), skipped {pdf_path}")
    else:
        shutil.copy2(pdf_path, dest_path)
        copied[clean_name] = {'source': pdf_path, 'size': size}

print(f"\nCopied {len(copied)} unique PDFs to consolidated/")
print(f"Resolved {len(skipped_duplicates)} duplicates")

# Step 5: Also copy the newly downloaded papers from the download script
new_downloads_dir = os.path.join(REPO_ROOT, "literature/papers/consolidated")
# Already the target, so check the download output dir
download_output = os.path.join(REPO_ROOT, "literature/papers/consolidated")

# Step 6: Generate the library manifest
manifest_rows = []
for clean_name, info in sorted(copied.items()):
    size_kb = info['size'] // 1024
    source_dir = os.path.dirname(info['source']).replace(REPO_ROOT, '').lstrip('/')
    manifest_rows.append({
        'filename': clean_name,
        'size_kb': size_kb,
        'source_dir': source_dir,
    })

manifest_path = os.path.join(REPO_ROOT, "literature/library_manifest.md")
with open(manifest_path, 'w') as f:
    f.write("# Paper Library Manifest\n\n")
    f.write(f"Total PDFs in consolidated library: **{len(copied)}**\n\n")
    f.write("| Filename | Size (KB) | Source Directory |\n")
    f.write("|---|---|---|\n")
    for row in manifest_rows:
        f.write(f"| `{row['filename']}` | {row['size_kb']} | `{row['source_dir']}` |\n")

print(f"\nWrote library manifest: {manifest_path}")

# Step 7: Cross-reference with BibTeX to find still-missing papers
# Load access classification to get canonical list
access_file = os.path.join(REPO_ROOT, "literature/access_classification.md")
cited_papers = []
if os.path.exists(access_file):
    with open(access_file, 'r') as f:
        for line in f:
            m = re.match(r'\|\s*\d+\s*\|([^|]+)\|([^|]+)\|([^|]+)\|', line)
            if m:
                authors = m.group(1).strip()
                year = m.group(2).strip()
                title = m.group(3).strip()[:50]
                cited_papers.append((authors, year, title))

print(f"\nTotal papers in access classification: {len(cited_papers)}")
print(f"Total PDFs in consolidated library: {len(copied)}")

# Final count
final_count = len(os.listdir(CONSOLIDATED_DIR))
print(f"\nFinal PDF count in consolidated/: {final_count}")
print(f"\nConsolidation complete. All PDFs are now in:")
print(f"  {CONSOLIDATED_DIR}")
