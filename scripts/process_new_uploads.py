#!/usr/bin/env python3
"""
Verify and process the 13 newly uploaded PDFs.
Map each to its canonical BibTeX key, copy to consolidated/.
Flag supplementary/associated pieces separately.
"""

import fitz, shutil, requests, time
from pathlib import Path

UPLOAD = Path("/home/ubuntu/upload")
CONSOLIDATED = Path("/home/ubuntu/k12-education-research/literature/papers/consolidated")
SUPPLEMENTARY = Path("/home/ubuntu/k12-education-research/literature/papers/supplementary")
SUPPLEMENTARY.mkdir(parents=True, exist_ok=True)

# The 13 uploaded files
uploads = [
    "DevelopmentandValidationoftheShortGritScaleGritS.pdf",
    "ehri-et-al-2001-systematic-phonics-instruction-helps-students-learn-to-read-evidence-from-the-national-reading-panel-s.pdf",
    "sisk-et-al-2018-to-what-extent-and-under-which-circumstances-are-growth-mind-sets-important-to-academic-achievement-two.pdf",
    "2016-15978-005.pdf",                          # yeager2016? duckworth? need to verify
    "1-s2.0-S0272775710001718-main.pdf",           # hanushek2011? need to verify
    "science.1248429.pdf",                          # campbell2014 (Science journal)
    "ED566667.pdf",                                 # lipsey2018? ERIC doc
    "pion-lipsey-2021-impact-of-the-tennessee-voluntary-prekindergarten-program-on-children-s-literacy-language-and.pdf",
    "JPolicyAnalManage-2002-Howell-Schoolvouchersandacademicperformanceresultsfromthreerandomizedfieldtrials.pdf",
    "castles-et-al-2018-ending-the-reading-wars-reading-acquisition-from-novice-to-expert.pdf",
    "2018-corrigendum-ending-the-reading-wars-reading-acquisition-from-novice-to-expert.pdf",
    "ChildDevelopment-2011-Durlak-TheImpactofEnhancingStudentsSocialandEmotionalLearningAMeta\u2010Analysisof.pdf",
    "2019-SEL-ICCs-NCME.pdf",
]

print("=== VERIFYING UPLOADED FILES ===\n")
for fname in uploads:
    fpath = UPLOAD / fname
    if not fpath.exists():
        print(f"NOT FOUND: {fname}")
        continue
    size = fpath.stat().st_size
    try:
        doc = fitz.open(str(fpath))
        text = ""
        for page in doc.pages(0, min(2, len(doc))):
            t = page.get_text()
            if t:
                text += t
        preview = text[:250].replace('\n', ' ').strip()
        print(f"[{size//1024}KB] {fname}")
        print(f"  → {preview}")
        print()
    except Exception as e:
        print(f"ERROR {fname}: {e}")

EOF_MARKER = True
