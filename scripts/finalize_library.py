#!/usr/bin/env python3
"""Copy the 3 final PDFs to canonical names and verify all 6 fixed papers."""

import fitz
import shutil
from pathlib import Path

CONSOLIDATED = Path("/home/ubuntu/k12-education-research/literature/papers/consolidated")
UPLOAD = Path("/home/ubuntu/upload")

# Map upload filenames to canonical keys
new_files = [
    ("pasted_file_k250tu_Nye-LargeTeacherEffects-2004.pdf", "nye2004.pdf"),
    ("pasted_file_ssJ9pf_Long-TermImpactsofReadingRecoverythrough3rdand4thGradeARegressionDiscontinuityStudy.pdf", "may2023.pdf"),
    ("pasted_file_cbrrmH_kraft-falken-2021-a-blueprint-for-scaling-tutoring-and-mentoring-across-public-schools.pdf", "kraft2021.pdf"),
]

print("Copying new PDFs to canonical names...")
for src_name, dest_name in new_files:
    src = UPLOAD / src_name
    dest = CONSOLIDATED / dest_name
    if src.exists():
        shutil.copy2(src, dest)
        doc = fitz.open(str(dest))
        text = "".join(page.get_text() for page in doc)
        pages = doc.page_count
        doc.close()
        print(f"  ✓ {dest_name}: {len(text)} chars, {pages} pages")
    else:
        print(f"  ✗ Source not found: {src_name}")

print("\nVerifying all 6 fixed papers...")
checks = {
    "cook2015": {
        "terms": ["0.65", "Chicago", "tutoring", "math"],
        "claim": "Chicago tutoring d=0.65 math"
    },
    "angrist2013": {
        "terms": ["Boston", "charter", "math", "lottery"],
        "claim": "Boston charters d=0.40 math"
    },
    "reardon2011": {
        "terms": ["income", "achievement gap", "2001"],
        "claim": "Income-achievement gap 30-40% larger"
    },
    "kraft2021": {
        "terms": ["tutoring", "school day", "paraprofessional", "blueprint"],
        "claim": "During-school tutoring parameters"
    },
    "may2023": {
        "terms": ["Reading Recovery", "fourth grade", "lower", "control"],
        "claim": "Reading Recovery 4th grade lower than control"
    },
    "nye2004": {
        "terms": ["STAR", "teacher", "effect"],
        "claim": "Teacher quality gap d=0.34-0.48"
    },
}

all_ok = True
for key, info in checks.items():
    pdf_path = CONSOLIDATED / f"{key}.pdf"
    doc = fitz.open(str(pdf_path))
    text = "".join(page.get_text() for page in doc)
    pages = doc.page_count
    doc.close()
    
    found = [t for t in info["terms"] if t.lower() in text.lower()]
    status = "✓" if found else "✗"
    if not found:
        all_ok = False
    print(f"  [{status}] {key} ({len(text)} chars, {pages}p): {info['claim']}")
    if found:
        print(f"      Found: {found}")
    else:
        print(f"      WARNING: None of {info['terms']} found!")
        print(f"      First 200 chars: {text[:200].replace(chr(10), ' ')}")

print(f"\n{'All 6 papers verified!' if all_ok else 'Some papers still have issues.'}")

# Now do a spot-check on the key specific numbers
print("\n--- Spot-checking specific numbers ---")
spot_checks = [
    ("nye2004", "teacher quality gap", ["0.34", "0.35", "0.36", "0.37", "0.38", "0.39", "0.40", "0.41", "0.42", "0.43", "0.44", "0.45", "0.46", "0.47", "0.48", "75th", "25th"]),
    ("cook2015", "d=0.65 math tutoring", ["0.65", "0.6"]),
    ("may2023", "4th grade lower than control", ["fourth grade", "4th grade", "lower than", "below"]),
    ("kraft2021", "during school day", ["school day", "during school", "in-school", "embedded"]),
    ("reardon2011", "30-40% larger", ["30 to 40", "30-40", "40 percent larger", "30 percent larger", "larger among"]),
    ("angrist2013", "d=0.40 per year", ["0.40", "0.4 standard", "per year"]),
]

for key, claim, terms in spot_checks:
    pdf_path = CONSOLIDATED / f"{key}.pdf"
    doc = fitz.open(str(pdf_path))
    text = "".join(page.get_text() for page in doc)
    doc.close()
    
    for term in terms:
        idx = text.lower().find(term.lower())
        if idx >= 0:
            start = max(0, idx - 150)
            end = min(len(text), idx + len(term) + 150)
            snippet = text[start:end].replace('\n', ' ').strip()
            print(f"\n  {key} | '{term}': ...{snippet}...")
            break
    else:
        print(f"\n  {key} | NONE FOUND: {terms}")
