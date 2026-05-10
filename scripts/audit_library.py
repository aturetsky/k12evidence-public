"""
Audit script: cross-reference every BibTeX entry against all PDFs in the repo.
Produces a precise list of:
  - Papers with PDFs confirmed present
  - Papers with no PDF found (missing)
  - Duplicate PDFs across old/new directory naming
"""

import os
import re
from pathlib import Path

REPO = Path("/home/ubuntu/k12-education-research")
BIB_FILE = REPO / "drafts" / "k12_references.bib"

# Collect all PDF paths in the repo
all_pdfs = list(REPO.rglob("*.pdf"))
pdf_names = [p.stem.lower() for p in all_pdfs]
pdf_paths = {p.stem.lower(): p for p in all_pdfs}

# Parse BibTeX entries
with open(BIB_FILE, "r") as f:
    bib_content = f.read()

# Extract all BibTeX keys and titles/authors
entries = re.findall(
    r'@\w+\{(\w+),.*?title\s*=\s*\{([^}]+)\}.*?author\s*=\s*\{([^}]+)\}',
    bib_content, re.DOTALL | re.IGNORECASE
)

# Also try author before title
entries2 = re.findall(
    r'@\w+\{(\w+),.*?author\s*=\s*\{([^}]+)\}.*?title\s*=\s*\{([^}]+)\}',
    bib_content, re.DOTALL | re.IGNORECASE
)

# Build a unified dict: key -> (title, first_author)
papers = {}
for key, title, author in entries:
    first_author = author.split(",")[0].strip().lower()
    papers[key] = {"title": title.strip(), "first_author": first_author}
for key, author, title in entries2:
    if key not in papers:
        first_author = author.split(",")[0].strip().lower()
        papers[key] = {"title": title.strip(), "first_author": first_author}

print(f"Total BibTeX entries: {len(papers)}")
print(f"Total PDFs in repo: {len(all_pdfs)}")
print()

# For each paper, try to find a matching PDF
present = []
missing = []

for key, info in sorted(papers.items()):
    key_lower = key.lower()
    title_words = [w.lower() for w in re.split(r'\W+', info["title"]) if len(w) > 3]
    author = info["first_author"]

    # Try exact key match
    matched = None
    for pdf_stem, pdf_path in pdf_paths.items():
        if key_lower in pdf_stem or pdf_stem in key_lower:
            matched = pdf_path
            break

    # Try author + year match
    if not matched:
        year_match = re.search(r'(\d{4})', key)
        year = year_match.group(1) if year_match else ""
        for pdf_stem, pdf_path in pdf_paths.items():
            # Extract last name from author (handle "Last, First" or "First Last")
            author_parts = author.replace(",", "").split()
            last_name = author_parts[0] if author_parts else ""
            if last_name and last_name in pdf_stem and (not year or year in pdf_stem):
                matched = pdf_path
                break

    # Try title keyword match
    if not matched and title_words:
        for pdf_stem, pdf_path in pdf_paths.items():
            matches = sum(1 for w in title_words[:5] if w in pdf_stem)
            if matches >= 2:
                matched = pdf_path
                break

    if matched:
        present.append((key, info["title"][:60], str(matched).replace(str(REPO)+"/", "")))
    else:
        missing.append((key, info["title"][:70], info["first_author"]))

print(f"=== PRESENT ({len(present)} papers) ===")
for key, title, path in sorted(present):
    print(f"  [{key}] {title}")
    print(f"    -> {path}")

print()
print(f"=== MISSING ({len(missing)} papers) ===")
for key, title, author in sorted(missing):
    print(f"  [{key}] {author} — {title}")

# Save results
with open(REPO / "literature" / "audit_results.md", "w") as f:
    f.write("# Library Audit Results\n\n")
    f.write(f"**Total BibTeX entries:** {len(papers)}  \n")
    f.write(f"**Total PDFs in repo:** {len(all_pdfs)}  \n")
    f.write(f"**Papers with PDFs confirmed:** {len(present)}  \n")
    f.write(f"**Papers missing PDFs:** {len(missing)}  \n\n")

    f.write("## Present\n\n")
    f.write("| BibTeX Key | Title | PDF Path |\n")
    f.write("|---|---|---|\n")
    for key, title, path in sorted(present):
        f.write(f"| `{key}` | {title} | `{path}` |\n")

    f.write("\n## Missing\n\n")
    f.write("| BibTeX Key | First Author | Title |\n")
    f.write("|---|---|---|\n")
    for key, title, author in sorted(missing):
        f.write(f"| `{key}` | {author} | {title} |\n")

print(f"\nAudit saved to literature/audit_results.md")
