#!/usr/bin/env python3
"""
Targeted open-access download script for the 33 missing papers.
Tries NBER working paper URLs, arXiv, SSRN, and Unpaywall API.
"""
import requests
import os
import time

OUTPUT_DIR = "/home/ubuntu/k12-education-research/literature/papers/consolidated"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {"User-Agent": "k12-lit-review-research@case.edu"}

# Map of bib key -> list of URLs to try in order
PAPERS = {
    # NBER working papers - direct PDF links
    "deming2009": [
        "https://www.nber.org/system/files/working_papers/w15072/w15072.pdf",
        "https://scholar.harvard.edu/files/ddeming/files/deming_headstart_2009.pdf",
    ],
    "cascio2013": [
        "https://www.nber.org/system/files/working_papers/w19452/w19452.pdf",
    ],
    "dobbie2011": [
        "https://scholar.harvard.edu/files/fryer/files/dobbie_fryer_hcz_aej_final.pdf",
        "https://www.nber.org/system/files/working_papers/w17468/w17468.pdf",
    ],
    "walters2018": [
        "https://www.nber.org/system/files/working_papers/w22502/w22502.pdf",
        "https://eml.berkeley.edu/~cwalters/papers/demand_charters.pdf",
    ],
    "pages2020": [
        "https://www.nber.org/system/files/working_papers/w28266/w28266.pdf",
    ],
    "bhatt2024": [
        "https://www.nber.org/system/files/working_papers/w32285/w32285.pdf",
    ],
    "backes2024": [
        "https://www.nber.org/system/files/working_papers/w32101/w32101.pdf",
        "https://cepa.stanford.edu/sites/default/files/wp23-07.pdf",
    ],
    "neilson2014": [
        "https://www.nber.org/system/files/working_papers/w20350/w20350.pdf",
        "https://economics.yale.edu/sites/default/files/neilson_zimmerman_2014.pdf",
    ],
    "fredriksson2013": [
        "https://www.nber.org/system/files/working_papers/w18482/w18482.pdf",
        "https://www.iza.org/publications/dp/6910/class-size-and-student-outcomes-research-and-policy-implications",
    ],
    "blazar2018": [
        "https://www.nber.org/system/files/working_papers/w24243/w24243.pdf",
        "https://scholar.harvard.edu/files/dblazar/files/blazar_kraft_2018_teacher_effects_attitudes.pdf",
    ],
    "benner2016": [
        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5026510/pdf/nihms806789.pdf",
    ],
    "wolf2017": [
        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5555376/pdf/nihms882682.pdf",
    ],
    "rodriguez2018": [
        "https://www.researchgate.net/publication/322776847",
    ],
    # Coleman 1966 - government document, available via ERIC
    "coleman1966": [
        "https://files.eric.ed.gov/fulltext/ED012275.pdf",
    ],
    # Card & Krueger 1992 - NBER
    "card1992": [
        "https://www.nber.org/system/files/working_papers/w3358/w3358.pdf",
        "https://davidcard.berkeley.edu/papers/school-quality-returns.pdf",
    ],
    # Durlak 2011 - Child Development - try PMC
    "durlak2011": [
        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3612993/pdf/nihms392128.pdf",
        "https://casel.org/wp-content/uploads/2016/06/meta-analysis-child-development-1.pdf",
    ],
    # Ehri 2001 - Elementary School Journal
    "ehri2001": [
        "https://files.eric.ed.gov/fulltext/ED446340.pdf",
    ],
    # Castles 2018 - Psychological Science in Public Interest
    "castles2018": [
        "https://journals.sagepub.com/doi/pdf/10.1177/1529100618772271",
        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6280769/pdf/10.1177_1529100618772271.pdf",
    ],
    # Shanahan 2010 - NELP report - ERIC
    "shanahan2010": [
        "https://files.eric.ed.gov/fulltext/ED508381.pdf",
    ],
    # Hanford 2018 - APM Reports journalism piece - free online
    "hanford2018": [
        "https://www.apmreports.org/documents/hard-words-report.pdf",
        "https://apmreports.org/documents/hard-words-report.pdf",
    ],
    # Credé 2017 - Journal of Personality and Social Psychology
    "cred2017": [
        "https://www.researchgate.net/publication/305522102",
        "https://osf.io/preprints/psyarxiv/",
    ],
    # Sims 2023 - JREE
    "sims2023": [
        "https://www.tandfonline.com/doi/pdf/10.1080/19345747.2022.2090470",
        "https://www.researchgate.net/publication/362018742",
    ],
    # Porter 2022
    "porter2022": [
        "https://files.eric.ed.gov/fulltext/EJ1348621.pdf",
    ],
    # Mourshed 2010 - McKinsey report - free online
    "mourshed2010": [
        "https://www.mckinsey.com/~/media/McKinsey/Industries/Social%20Sector/Our%20Insights/How%20the%20worlds%20most%20improved%20school%20systems%20keep%20getting%20better/How-the-worlds-most-improved-school-systems-keep-getting-better.pdf",
    ],
    # Blau & Duncan style - check Hanushek school finance
    "lafortune2018": [
        "https://www.nber.org/system/files/working_papers/w22011/w22011.pdf",
        "https://eml.berkeley.edu/~jrothst/workingpapers/lafortune_rothstein_schanzenbach.pdf",
    ],
    # Jackson 2016 - QJE - NBER
    "jackson2016": [
        "https://www.nber.org/system/files/working_papers/w20847/w20847.pdf",
        "https://scholar.harvard.edu/files/ckjackson/files/jackson_johnson_persico_2016.pdf",
    ],
    # Krueger 1999 - QJE - NBER
    "krueger1999": [
        "https://www.nber.org/system/files/working_papers/w5987/w5987.pdf",
        "https://dataspace.princeton.edu/bitstream/88435/dsp01kh04dp89g/1/393.pdf",
    ],
    # Angrist 2013
    "angrist2013": [
        "https://www.nber.org/system/files/working_papers/w19078/w19078.pdf",
    ],
    # Heckman 2010 - various
    "heckman2010": [
        "https://heckmanequation.org/assets/2017/01/F_Heckman_Perry_Study_Summary_2012.pdf",
        "https://www.nber.org/system/files/working_papers/w15471/w15471.pdf",
    ],
}

def try_download(key, urls):
    out_path = os.path.join(OUTPUT_DIR, f"{key}.pdf")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
        print(f"  ALREADY EXISTS: {key}")
        return True
    for url in urls:
        try:
            print(f"  Trying: {url[:80]}...")
            r = requests.get(url, headers=HEADERS, timeout=20, allow_redirects=True)
            if r.status_code == 200 and len(r.content) > 10000:
                # Check it's actually a PDF
                if r.content[:4] == b'%PDF' or 'pdf' in r.headers.get('content-type','').lower():
                    with open(out_path, 'wb') as f:
                        f.write(r.content)
                    print(f"  SUCCESS: {key} ({len(r.content)//1024}KB)")
                    return True
                else:
                    print(f"  Not a PDF (content-type: {r.headers.get('content-type','')})")
            else:
                print(f"  HTTP {r.status_code}")
        except Exception as e:
            print(f"  Error: {e}")
        time.sleep(1)
    print(f"  FAILED: {key}")
    return False

print(f"Attempting open-access downloads for {len(PAPERS)} missing papers...")
print(f"Output: {OUTPUT_DIR}\n")

succeeded = []
failed = []

for key, urls in PAPERS.items():
    print(f"\n[{key}]")
    if try_download(key, urls):
        succeeded.append(key)
    else:
        failed.append(key)

print(f"\n{'='*60}")
print(f"SUCCEEDED ({len(succeeded)}): {', '.join(succeeded)}")
print(f"\nFAILED ({len(failed)}): {', '.join(failed)}")
print(f"\nStill need CWRU upload for: {len(failed)} papers")

# Write the still-missing list
still_missing_path = "/home/ubuntu/k12-education-research/literature/still_missing.md"
with open(still_missing_path, 'w') as f:
    f.write("# Papers Still Missing from Library\n\n")
    f.write(f"Updated: after open-access download attempt\n\n")
    if failed:
        f.write("## Needs CWRU Upload\n\n")
        for k in failed:
            f.write(f"- `{k}`\n")
    else:
        f.write("**All papers present. Library complete.**\n")

print(f"\nWrote still_missing.md")
