"""Download remaining NBER papers using curl subprocess for better timeout control."""
import subprocess
import os
from pathlib import Path

OUTPUT_DIR = Path("/home/ubuntu/k12-education-research/literature/papers/missing_downloads")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PAPERS = [
    ("garca2022", "w30004", "Garcia_Heckman_Ronda_2022_early_childhood"),
    ("jackson2016", "w20847", "Jackson_Johnson_Persico_2016_school_spending"),
    ("lafortune2018", "w22011", "Lafortune_Rothstein_Schanzenbach_2018_school_finance"),
    ("nickow2020", "w27476", "Nickow_Oreopoulos_Quan_2020_tutoring"),
    ("goldhaber2022", "w30010", "Goldhaber_etal_2022_remote_hybrid_pandemic"),
    ("guryan2023", "w28531", "Guryan_etal_2023_not_too_late"),
    ("cook2015", "w21001", "Cook_etal_2015_not_too_late"),
    ("hoxby2009", "w14852", "Hoxby_Murarka_2009_charter_nyc"),
    ("fryer2014", "w17851", "Fryer_2014_charter_best_practices"),
    ("bailey2021", "w26299", "Bailey_etal_2021_head_start"),
]

for key, num, name in PAPERS:
    out = OUTPUT_DIR / f"{key}_{name}.pdf"
    if out.exists() and out.stat().st_size > 10000:
        print(f"SKIP (exists): {key}")
        continue
    url = f"https://www.nber.org/system/files/working_papers/{num}/{num}.pdf"
    print(f"Downloading {key} from {url}...")
    result = subprocess.run(
        ["curl", "-s", "-L", "--max-time", "25", "-o", str(out), url],
        capture_output=True, timeout=30
    )
    if out.exists() and out.stat().st_size > 10000:
        print(f"  ✓ {out.stat().st_size//1024}KB")
    else:
        print(f"  ✗ Failed")
        if out.exists():
            out.unlink()

# Also try direct URLs for non-NBER papers
DIRECT = [
    ("greenberg2009", "https://www.bmj.com/content/bmj/339/bmj.b2680.full.pdf", "Greenberg_2009_citation_distortion"),
    ("jones2019", "https://www.aspeninstitute.org/wp-content/uploads/2019/09/SEAD-Research-Brief-9.17.19.pdf", "Jones_2019_SEL_evidence"),
    ("credostanford2015", "https://credo.stanford.edu/wp-content/uploads/2021/08/urban_charter_school_study_report_2015.pdf", "CREDO_2015_urban_charter"),
]

for key, url, name in DIRECT:
    out = OUTPUT_DIR / f"{key}_{name}.pdf"
    if out.exists() and out.stat().st_size > 10000:
        print(f"SKIP (exists): {key}")
        continue
    print(f"Downloading {key}...")
    result = subprocess.run(
        ["curl", "-s", "-L", "--max-time", "25", "-A", "Mozilla/5.0", "-o", str(out), url],
        capture_output=True, timeout=30
    )
    if out.exists() and out.stat().st_size > 10000:
        print(f"  ✓ {out.stat().st_size//1024}KB")
    else:
        print(f"  ✗ Failed")
        if out.exists():
            out.unlink()

print("\nAll done. Files in output dir:")
for f in sorted(OUTPUT_DIR.glob("*.pdf")):
    print(f"  {f.name} ({f.stat().st_size//1024}KB)")
