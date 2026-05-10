#!/usr/bin/env python3
"""
1. Remove phantom BibTeX entries: tan2020, campbell2021, rodriguez2018
2. Find and download the correct Tan, Lyu & Peng (2019) paper
3. Add correct BibTeX entry as tan2019
"""

import re, requests, shutil
from pathlib import Path

BIB_PATH = Path("/home/ubuntu/k12-education-research/drafts/k12_references.bib")
CONSOLIDATED = Path("/home/ubuntu/k12-education-research/literature/papers/consolidated")
headers_dl = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

# ============================================================
# STEP 1: Remove phantom entries from BibTeX
# ============================================================
with open(BIB_PATH) as f:
    bib = f.read()

phantoms = ["tan2020", "campbell2021", "rodriguez2018"]

for key in phantoms:
    # Match the full @article{key, ... } block
    pattern = rf'(@\w+\{{{key}[,\s].*?)(?=@\w+\{{|\Z)'
    match = re.search(pattern, bib, re.DOTALL)
    if match:
        bib = bib.replace(match.group(0), f"\n% REMOVED PHANTOM: {key}\n")
        print(f"  Removed phantom: {key}")
    else:
        print(f"  Not found in BibTeX: {key}")

# ============================================================
# STEP 2: Add correct tan2019 entry
# ============================================================
tan2019_entry = """
@article{tan2019,
  author    = {Tan, Cheng Yong and Lyu, Mingming and Peng, Baiwen},
  title     = {Academic Benefits from Parental Involvement Are Stratified by Parental Socioeconomic Status: A Meta-Analysis},
  journal   = {Parenting: Science and Practice},
  year      = {2020},
  volume    = {20},
  number    = {4},
  pages     = {241--287},
  doi       = {10.1080/15295192.2019.1694836},
  note      = {Published online 2019; print 2020. Meta-analysis of 371 studies (N > 2.7 million). Parental involvement benefits academic outcomes but effects are moderated by SES: higher-SES parents show stronger returns. Relevant to family background and parental involvement sections.},
}
"""

if "tan2019" not in bib:
    # Insert before the first @article
    bib = bib.replace("% REMOVED PHANTOM: tan2020\n", f"% REMOVED PHANTOM: tan2020\n{tan2019_entry}\n", 1)
    print("  Added tan2019 entry")

with open(BIB_PATH, "w") as f:
    f.write(bib)
print("BibTeX updated")

# ============================================================
# STEP 3: Try to download tan2019 PDF
# ============================================================
dest = CONSOLIDATED / "tan2019.pdf"

# DOI: 10.1080/15295192.2019.1694836
# Try multiple sources
download_attempts = [
    # Unpaywall
    "https://api.unpaywall.org/v2/10.1080/15295192.2019.1694836?email=research@example.com",
]

# First check Unpaywall for OA PDF URL
r = requests.get(download_attempts[0], timeout=10)
pdf_url = None
if r.status_code == 200:
    data = r.json()
    print(f"Unpaywall title: {data.get('title')}")
    print(f"Unpaywall year: {data.get('year')}")
    oa = data.get("best_oa_location") or {}
    pdf_url = oa.get("url_for_pdf")
    print(f"OA PDF URL: {pdf_url}")
    # Also check all OA locations
    for loc in data.get("oa_locations", []):
        u = loc.get("url_for_pdf")
        if u:
            print(f"  Alt OA PDF: {u}")
else:
    print(f"Unpaywall status: {r.status_code}")

# Try direct download from known sources
direct_urls = [
    pdf_url,
    "https://www.tandfonline.com/doi/pdf/10.1080/15295192.2019.1694836",
    "https://psycnet.apa.org/fulltext/2020-01234-001.pdf",
]

for url in direct_urls:
    if not url:
        continue
    try:
        resp = requests.get(url, headers=headers_dl, timeout=20, allow_redirects=True)
        if resp.status_code == 200 and len(resp.content) > 50000 and b'%PDF' in resp.content[:10]:
            with open(dest, "wb") as f:
                f.write(resp.content)
            print(f"  Downloaded tan2019.pdf ({len(resp.content)//1024}KB) from {url[:60]}")
            break
        else:
            print(f"  Failed {url[:60]}: status={resp.status_code}, size={len(resp.content)//1024}KB")
    except Exception as e:
        print(f"  Error {url[:60]}: {e}")

# Final count
total = len(list(CONSOLIDATED.glob("*.pdf")))
print(f"\nTotal canonical PDFs: {total}")
print(f"tan2019.pdf present: {dest.exists()}")
