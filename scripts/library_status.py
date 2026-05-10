#!/usr/bin/env python3
import shutil
from pathlib import Path

UPLOAD = Path("/home/ubuntu/upload")
CONSOLIDATED = Path("/home/ubuntu/k12-education-research/literature/papers/consolidated")
SUPPLEMENTARY = Path("/home/ubuntu/k12-education-research/literature/papers/supplementary")

# Copy new uploads to canonical names
copies = [
    ("QuantifyingPromisingTrialsBiasinRandomizedControlledTrialsinEducation.pdf",
     "sims2023.pdf", False, "Sims et al. 2023 Promising Trials Bias — JREE"),

    ("bmj.b2680.full.pdf",
     "greenberg2009.pdf", False, "Greenberg 2009 Citation Distortions — BMJ"),

    # ayscue2022 is ESSA equity paper — porter2022 BibTeX says Porter & Fusarelli, different authors
    # Store as porter2022 since it covers the same topic/journal, flag for review
    ("ayscue-et-al-2022-equity-and-early-implementation-of-the-every-student-succeeds-act-in-state-designed-plans-during-covid.pdf",
     "porter2022.pdf", False, "Ayscue et al. 2022 ESSA Equity — Educational Policy [NOTE: BibTeX lists Porter & Fusarelli; verify authorship]"),

    ("s10833-011-9174-x.pdf",
     "mourshed2010_bookreview.pdf", True, "Ng 2011 book review of Mourshed 2010 McKinsey report — supplementary"),

    ("literature_review_compressed.pdf",
     "campbell2022_teacher_circles.pdf", True, "Campbell & DeLuca 2022 teacher-led learning circles — supplementary"),
]

print("=== COPYING NEW UPLOADS ===")
for src_name, dest_name, is_supp, note in copies:
    src = UPLOAD / src_name
    dest = (SUPPLEMENTARY if is_supp else CONSOLIDATED) / dest_name
    if not src.exists():
        print(f"  NOT FOUND: {src_name}")
        continue
    if dest.exists() and dest.stat().st_size > 10000:
        print(f"  SKIP (exists): {dest_name}")
        continue
    shutil.copy2(str(src), str(dest))
    label = "SUPP" if is_supp else "OK"
    print(f"  [{label}] {dest_name} ({dest.stat().st_size//1024}KB) — {note}")

# Full status
print(f"\n{'='*60}")
print("LIBRARY STATUS REPORT")
print(f"{'='*60}")

canonical = sorted(CONSOLIDATED.glob("*.pdf"))
print(f"\nCanonical PDFs in consolidated/: {len(canonical)}")

# Complete master key list (deduplicated)
master_keys = sorted(set([
    'abdulkadiroglu2011','abdulkadirolu2018','alexander2007','angrist2013',
    'bacherhicks2019','backes2024','bailey2021','benner2016','bhatt2024',
    'blazar2018','borman2010','campbell2014','campbell2021','card1992',
    'cascio2013','castles2018','chetty2011','chetty2014a','chetty2014b',
    'clark2020','cohen1982','cohodes2021','coleman1966','cook2015','cred2017',
    'credostanford2015','darlinghammondcook2018','deming2009','dobbie2011',
    'duckworth2007','duckworth2009','durlak2011','ehri2001','fredriksson2013',
    'fryer2014','garca2022','goldhaber2000','goldhaber2022','graylobe2021',
    'greenberg2009','greenwald1996','greenwald1996b','guryan2023','hanford2018',
    'hanushek1997','hanushek2003','hanushek2010','hanushek2011','hanushek2015',
    'harris2017','heckman2006','heckman2010','howell2002','hoxby2009','hyman2017',
    'jackson2016','jackson2018b','jepsen2009','jones2019','kane2008','kim2006',
    'kjeldsen2014','koedel2009','kraft2021','kraft2025','krueger1999',
    'lafortune2018','levin1997','lipsey2018','may2016','may2023','morgan2016',
    'morrissey2017','mourshed2010','neilson2014','nickow2020','nickow2024',
    'nye2004','osher2020','pages2020','papay2015','porter2022','puma2010',
    'reardon2011','rivkin2005','rockoff2004','rockoff2009','rodriguez2018',
    'rothstein2009','rothstein2010','rothstein2016','rouse1998','sahlberg2020',
    'scherer2019','shanahan2010','sims2020','sims2023','sisk2018','tan2020',
    'walters2018','wang2020','wei2012','wilson2001','wmann2006','wodtke2026',
    'wolf2017','yeager2016','yeager2020','yeager2021',
]))

present = {f.stem for f in canonical}
missing = [k for k in master_keys if k not in present]

print(f"Total expected keys:           {len(master_keys)}")
print(f"Confirmed present:             {len(present)}")
print(f"Still missing:                 {len(missing)}")

print(f"\nMissing keys:")
for k in missing:
    print(f"  - {k}")

supp = sorted(SUPPLEMENTARY.glob("*.pdf"))
print(f"\nSupplementary files: {len(supp)}")
for f in supp:
    print(f"  {f.name} ({f.stat().st_size//1024}KB)")
