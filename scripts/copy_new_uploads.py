#!/usr/bin/env python3
import shutil
from pathlib import Path

UPLOAD = Path("/home/ubuntu/upload")
CONSOLIDATED = Path("/home/ubuntu/k12-education-research/literature/papers/consolidated")
SUPPLEMENTARY = Path("/home/ubuntu/k12-education-research/literature/papers/supplementary")
SUPPLEMENTARY.mkdir(parents=True, exist_ok=True)

# Verified mapping: upload filename -> (canonical_key, is_supplementary, note)
mapping = {
    "DevelopmentandValidationoftheShortGritScaleGritS.pdf":
        ("duckworth2009", False, "Duckworth & Quinn 2009 Short Grit Scale — Journal of Personality Assessment"),

    "ehri-et-al-2001-systematic-phonics-instruction-helps-students-learn-to-read-evidence-from-the-national-reading-panel-s.pdf":
        ("ehri2001", False, "Ehri et al. 2001 Systematic Phonics — Review of Educational Research"),

    "sisk-et-al-2018-to-what-extent-and-under-which-circumstances-are-growth-mind-sets-important-to-academic-achievement-two.pdf":
        ("sisk2018", False, "Sisk et al. 2018 Growth Mindsets Meta-Analysis — Psychological Science"),

    "2016-15978-005.pdf":
        ("yeager2016", False, "Yeager et al. 2016 Design Thinking Growth Mindset — PNAS"),

    "1-s2.0-S0272775710001718-main.pdf":
        ("hanushek2011", False, "Hanushek 2011 Economic Value of Teacher Quality — Economics of Education Review"),

    "science.1248429.pdf":
        ("campbell2014", False, "Campbell et al. 2014 Early Childhood Investments — Science"),

    "ED566667.pdf":
        ("lipsey2018", False, "Lipsey et al. 2018 Tennessee Pre-K RCT K-1 Follow-Up — ERIC"),

    "pion-lipsey-2021-impact-of-the-tennessee-voluntary-prekindergarten-program-on-children-s-literacy-language-and.pdf":
        ("lipsey2021_supp", True, "Lipsey et al. 2021 Tennessee Pre-K Literacy Follow-Up — AERA Open [associated piece]"),

    "JPolicyAnalManage-2002-Howell-Schoolvouchersandacademicperformanceresultsfromthreerandomizedfieldtrials.pdf":
        ("howell2002", False, "Howell Wolf Campbell Peterson 2002 School Vouchers — JPAM"),

    "castles-et-al-2018-ending-the-reading-wars-reading-acquisition-from-novice-to-expert.pdf":
        ("castles2018", False, "Castles Rastle Nation 2018 Ending Reading Wars — Psychological Science in the Public Interest"),

    "2018-corrigendum-ending-the-reading-wars-reading-acquisition-from-novice-to-expert.pdf":
        ("castles2018_corrigendum", True, "Castles 2018 Corrigendum [associated piece]"),

    "ChildDevelopment-2011-Durlak-TheImpactofEnhancingStudentsSocialandEmotionalLearningAMeta\u2010Analysisof.pdf":
        ("durlak2011", False, "Durlak et al. 2011 SEL Meta-Analysis — Child Development"),

    "2019-SEL-ICCs-NCME.pdf":
        ("rodriguez2019_supp", True, "Rodriguez Nickodem Lamm 2019 SEL ICCs NCME [associated piece to rodriguez2018]"),
}

print("=== COPYING TO CANONICAL LIBRARY ===\n")
for fname, (key, is_supp, note) in mapping.items():
    src = UPLOAD / fname
    if not src.exists():
        print(f"  NOT FOUND: {fname}")
        continue

    if is_supp:
        dest = SUPPLEMENTARY / f"{key}.pdf"
        dest_label = "supplementary"
        icon = "SUPP"
    else:
        dest = CONSOLIDATED / f"{key}.pdf"
        dest_label = "consolidated"
        icon = "OK"

    shutil.copy2(str(src), str(dest))
    size = dest.stat().st_size
    print(f"  [{icon}] {key}.pdf -> {dest_label}/ ({size//1024}KB)")
    print(f"       {note}")

print("\n=== FINAL CONSOLIDATED COUNT ===")
count = len(list(CONSOLIDATED.glob("*.pdf")))
print(f"  {count} canonical PDFs in consolidated/")

print("\n=== SUPPLEMENTARY FILES ===")
for f in sorted(SUPPLEMENTARY.glob("*.pdf")):
    print(f"  [SUPP] {f.name} ({f.stat().st_size//1024}KB)")
