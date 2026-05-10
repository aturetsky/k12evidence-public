import fitz, shutil
from pathlib import Path

CONSOLIDATED = Path("/home/ubuntu/k12-education-research/literature/papers/consolidated")
UPLOAD = Path("/home/ubuntu/upload")

# Check the CREDO online charter study
print("="*60)
print("Checking online_charter_study_final.pdf")
print("="*60)
doc = fitz.open(str(UPLOAD / "online_charter_study_final.pdf"))
full_text = "".join(doc[i].get_text() for i in range(doc.page_count))
pages = doc.page_count
doc.close()

print(f"Pages: {pages}, Chars: {len(full_text)}")
print(f"First 500 chars: {full_text[:500].replace(chr(10), ' ')}")

for term in ["72", "180", "days", "virtual", "online charter", "learning days", "CREDO", "2015"]:
    idx = full_text.lower().find(term.lower())
    if idx >= 0:
        s = max(0, idx - 150)
        e = min(len(full_text), idx + len(term) + 200)
        print(f"\n  '{term}': ...{full_text[s:e].replace(chr(10),' ')}...")

# Now copy both files to canonical names
print("\n" + "="*60)
print("Copying files to canonical names")
print("="*60)

copies = [
    ("apw_unformatted-1.pdf", "abdulkadirolu2018.pdf"),
    ("online_charter_study_final.pdf", "credostanford2015.pdf"),
]

for src_name, dest_name in copies:
    src = UPLOAD / src_name
    dest = CONSOLIDATED / dest_name
    if src.exists():
        shutil.copy2(src, dest)
        doc = fitz.open(str(dest))
        text = "".join(doc[i].get_text() for i in range(doc.page_count))
        doc.close()
        print(f"  ✓ {dest_name}: {len(text)} chars, {doc.page_count} pages")
    else:
        print(f"  ✗ Source not found: {src_name}")
