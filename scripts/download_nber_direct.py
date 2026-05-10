"""
Download NBER working papers directly using their known paper numbers.
NBER PDFs are publicly accessible at https://www.nber.org/system/files/working_papers/wXXXXX/wXXXXX.pdf
"""

import requests
import time
from pathlib import Path

REPO = Path("/home/ubuntu/k12-education-research")
OUTPUT_DIR = REPO / "literature" / "papers" / "missing_downloads"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

# Known NBER paper numbers for our missing papers
NBER_PAPERS = [
    ("angrist2013",   "w17890", "Angrist_Pathak_Walters_2013_charter_schools"),
    ("abdulkadiroglu2011", "w17332", "Abdulkadiroglu_etal_2011_charter_accountability"),
    ("heckman2010",   "w15471", "Heckman_etal_2010_perry_preschool_roi"),
    ("garca2022",     "w30004", "Garcia_Heckman_Ronda_2022_early_childhood"),
    ("jackson2016",   "w20847", "Jackson_Johnson_Persico_2016_school_spending"),
    ("lafortune2018", "w22011", "Lafortune_Rothstein_Schanzenbach_2018_school_finance"),
    ("nickow2020",    "w27476", "Nickow_Oreopoulos_Quan_2020_tutoring"),
    ("nickow2024",    "w27476", "Nickow_Oreopoulos_Quan_2024_tutoring"),  # same paper, updated
    ("goldhaber2022", "w30010", "Goldhaber_etal_2022_remote_hybrid_pandemic"),
    ("guryan2023",    "w28531", "Guryan_etal_2023_not_too_late"),
    ("cook2015",      "w21001", "Cook_etal_2015_not_too_late_disadvantaged"),
    ("hoxby2009",     "w14852", "Hoxby_Murarka_2009_charter_nyc"),
    ("fryer2014",     "w17851", "Fryer_2014_charter_best_practices"),
    ("bailey2021",    "w26299", "Bailey_etal_2021_head_start_long_run"),
]

# Also try direct journal/author URLs for non-NBER papers
DIRECT_URLS = [
    ("greenberg2009", "https://www.bmj.com/content/bmj/339/bmj.b2680.full.pdf", "Greenberg_2009_citation_distortion"),
    ("sims2023",      "https://www.tandfonline.com/doi/pdf/10.1080/19345747.2022.2090470", "Sims_2023_promising_trials_bias"),
    ("jones2019",     "https://www.aspeninstitute.org/wp-content/uploads/2019/09/SEAD-Research-Brief-9.17.19.pdf", "Jones_2019_evidence_base_SEL"),
    ("credostanford2015", "https://credo.stanford.edu/wp-content/uploads/2021/08/urban_charter_school_study_report_2015.pdf", "CREDO_2015_urban_charter_study"),
    ("mourshed2010",  "https://www.mckinsey.com/~/media/mckinsey/industries/public%20and%20social%20sector/our%20insights/how%20the%20worlds%20most%20improved%20school%20systems%20keep%20getting%20better/how_the_worlds_most_improved_school_systems_keep_getting_better.pdf", "McKinsey_2010_school_systems"),
    ("hanford2018",   "https://s3.amazonaws.com/apmreports/hard_words/hard_words_why_american_kids_cant_read.pdf", "Hanford_2018_hard_words"),
]

downloaded = []
failed = []

print("=== Downloading NBER working papers ===")
for key, nber_num, name in NBER_PAPERS:
    output_path = OUTPUT_DIR / f"{key}_{name}.pdf"
    if output_path.exists() and output_path.stat().st_size > 10000:
        print(f"  SKIP (exists): {key}")
        downloaded.append(key)
        continue
    
    url = f"https://www.nber.org/system/files/working_papers/{nber_num}/{nber_num}.pdf"
    print(f"  Trying {key}: {url}")
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code == 200 and r.content[:4] == b'%PDF':
            with open(output_path, 'wb') as f:
                f.write(r.content)
            print(f"    ✓ Downloaded ({output_path.stat().st_size//1024}KB)")
            downloaded.append(key)
        else:
            print(f"    ✗ HTTP {r.status_code}")
            failed.append((key, url))
    except Exception as e:
        print(f"    ✗ Error: {e}")
        failed.append((key, url))
    time.sleep(1)

print("\n=== Downloading from direct URLs ===")
for key, url, name in DIRECT_URLS:
    output_path = OUTPUT_DIR / f"{key}_{name}.pdf"
    if output_path.exists() and output_path.stat().st_size > 10000:
        print(f"  SKIP (exists): {key}")
        downloaded.append(key)
        continue
    
    print(f"  Trying {key}...")
    try:
        r = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
        if r.status_code == 200 and len(r.content) > 10000:
            with open(output_path, 'wb') as f:
                f.write(r.content)
            print(f"    ✓ Downloaded ({output_path.stat().st_size//1024}KB)")
            downloaded.append(key)
        else:
            print(f"    ✗ HTTP {r.status_code}")
            failed.append((key, url))
    except Exception as e:
        print(f"    ✗ Error: {e}")
        failed.append((key, url))
    time.sleep(1)

print(f"\n=== SUMMARY ===")
print(f"Downloaded: {len(downloaded)}")
print(f"Failed: {len(failed)}")
print("\nFailed papers:")
for key, url in failed:
    print(f"  {key}: {url}")
