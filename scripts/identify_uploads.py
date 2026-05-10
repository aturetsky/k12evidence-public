import fitz
from pathlib import Path

files = [
    "/home/ubuntu/upload/apw_unformatted-1.pdf",
    "/home/ubuntu/upload/ED568902.pdf",
]

for f in files:
    doc = fitz.open(f)
    text = "".join(doc[i].get_text() for i in range(min(3, doc.page_count)))
    doc.close()
    print(f"\n{'='*60}")
    print(f"FILE: {Path(f).name}")
    print(f"First 600 chars: {text[:600].replace(chr(10), ' ')}")
    
    # Check for key identifying terms
    full_doc = fitz.open(f)
    full_text = "".join(full_doc[i].get_text() for i in range(full_doc.page_count))
    full_doc.close()
    
    for term in ["Louisiana", "voucher", "scholarship", "CREDO", "charter", "virtual", 
                 "72 days", "180 days", "learning days", "Abdulkadiroglu", "negative effect",
                 "-0.4", "National Charter School Study"]:
        idx = full_text.lower().find(term.lower())
        if idx >= 0:
            s = max(0, idx - 100)
            e = min(len(full_text), idx + len(term) + 200)
            print(f"  '{term}': ...{full_text[s:e].replace(chr(10),' ')}...")
