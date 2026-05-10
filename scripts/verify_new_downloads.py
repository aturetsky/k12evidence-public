import fitz
from pathlib import Path

CONSOLIDATED = Path("/home/ubuntu/k12-education-research/literature/papers/consolidated")

checks = {
    "cook2015": ["0.65", "Chicago", "tutoring", "math", "course failure"],
    "angrist2013": ["Boston", "charter", "0.40", "math", "lottery"],
    "reardon2011": ["income", "achievement gap", "30", "40", "2001"],
    "kraft2021": ["tutoring", "school day", "paraprofessional", "dosage"],
    "may2023": ["Reading Recovery", "fourth grade", "lower", "fadeout"],
    "nye2004": ["STAR", "teacher", "0.34", "0.35", "0.36", "0.37", "0.38", "0.39", "0.40", "0.41", "0.42", "0.43", "0.44", "0.45", "0.46", "0.47", "0.48"],
}

for key, terms in checks.items():
    pdf_path = CONSOLIDATED / f"{key}.pdf"
    doc = fitz.open(str(pdf_path))
    text = "".join(page.get_text() for page in doc)
    page_count = doc.page_count
    doc.close()
    
    print(f"\n{'='*50}")
    print(f"{key}: {len(text)} chars, {page_count} pages")
    print(f"First 200 chars: {text[:200].replace(chr(10), ' ')}")
    
    found = []
    for term in terms:
        if term.lower() in text.lower():
            found.append(term)
    print(f"Found terms: {found}")
    
    if not found:
        print(f"  WARNING: No expected terms found - likely still wrong paper!")
    else:
        print(f"  OK: {len(found)}/{len(terms)} terms found")
