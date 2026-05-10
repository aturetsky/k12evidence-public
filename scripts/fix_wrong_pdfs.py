#!/usr/bin/env python3
"""
Identify wrong/broken PDFs and attempt to download correct versions.
Papers confirmed wrong or broken:
- may2023: 404 page saved as PDF (need Reading Recovery long-term follow-up)
- cook2015: Wrong paper (NBER social learning paper, need Chicago tutoring RCT)
- kraft2021: 404 page saved as PDF (need Kraft tutoring blueprint)
- nye2004: Likely wrong paper (need Nye et al. 2004 STAR teacher quality)
- angrist2013: Wrong paper (need Angrist et al. 2013 Boston charters)
- credostanford2015: Scanned/unreadable (need CREDO 2015 national charter report)
- reardon2011: Wrong paper (need Reardon 2011 income-achievement gap)
"""

import requests
import fitz
import time
from pathlib import Path

CONSOLIDATED = Path("/home/ubuntu/k12-education-research/literature/papers/consolidated")
ELICIT_KEY = "elk_live_dliSTcNbqzcwtBiQzE5QeZbqOClWBfuP8xEAz2O4fU"

def try_download(url, dest_path, label):
    """Try to download a PDF from a URL."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (research bot; contact: research@example.com)"}
        r = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
        if r.status_code == 200 and len(r.content) > 10000:
            # Verify it's a real PDF
            if r.content[:4] == b'%PDF':
                with open(dest_path, 'wb') as f:
                    f.write(r.content)
                print(f"  ✓ Downloaded {label} ({len(r.content)//1024}KB)")
                return True
            else:
                print(f"  ✗ {label}: Not a PDF (got {r.content[:50]})")
        else:
            print(f"  ✗ {label}: HTTP {r.status_code}, size {len(r.content)}")
    except Exception as e:
        print(f"  ✗ {label}: {e}")
    return False

def search_semantic_scholar(title, authors_year):
    """Search Semantic Scholar for a paper and return open access PDF URL."""
    try:
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": title,
            "fields": "title,authors,year,openAccessPdf,externalIds",
            "limit": 5
        }
        r = requests.get(url, params=params, timeout=20)
        if r.status_code == 200:
            data = r.json()
            for paper in data.get("data", []):
                if paper.get("openAccessPdf") and paper["openAccessPdf"].get("url"):
                    print(f"  S2 found: {paper.get('title', '')[:60]} ({paper.get('year')})")
                    return paper["openAccessPdf"]["url"]
    except Exception as e:
        print(f"  S2 error: {e}")
    return None

def search_elicit(title):
    """Search Elicit for a paper."""
    try:
        headers = {
            "Authorization": f"Bearer {ELICIT_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "query": title,
            "numResults": 5,
            "resultFields": ["title", "authors", "year", "doi", "url", "pdfUrl"]
        }
        r = requests.post("https://api.elicit.com/api/v1/search", 
                         json=payload, headers=headers, timeout=20)
        if r.status_code == 200:
            data = r.json()
            for paper in data.get("papers", []):
                if paper.get("pdfUrl"):
                    print(f"  Elicit found PDF: {paper.get('title', '')[:60]}")
                    return paper["pdfUrl"]
    except Exception as e:
        print(f"  Elicit error: {e}")
    return None

# Papers to fix with their correct details
papers_to_fix = [
    {
        "key": "may2023",
        "title": "Reading Recovery long-term fadeout fourth grade lower scores",
        "description": "May et al. 2023 Reading Recovery long-term follow-up showing fadeout by 4th grade",
        "doi": "10.3102/0013189X231165056",
        "urls": [
            "https://journals.sagepub.com/doi/pdf/10.3102/0013189X231165056",
            "https://www.researchgate.net/publication/369876543",
        ]
    },
    {
        "key": "cook2015",
        "title": "Tutoring and mentoring for disadvantaged youth Chicago high school math",
        "description": "Cook et al. 2015 Chicago tutoring RCT d=0.65 math",
        "doi": "10.1126/science.1261800",
        "urls": [
            "https://www.science.org/doi/pdf/10.1126/science.1261800",
            "https://www.nber.org/system/files/working_papers/w19014/w19014.pdf",
            "https://economics.mit.edu/sites/default/files/publications/Tutoring%20and%20Mentoring%20for%20Disadvantaged%20Youth.pdf",
        ]
    },
    {
        "key": "kraft2021",
        "title": "Tutoring blueprint high dosage during school day paraprofessional",
        "description": "Kraft 2021 tutoring blueprint - during school day parameters",
        "doi": "10.1177/0013161X211042856",
        "urls": [
            "https://scholar.harvard.edu/files/mkraft/files/kraft_2021_-_a_blueprint_for_scaling_tutoring_and_mentoring_programs_in_public_schools.pdf",
            "https://www.edworkingpapers.com/sites/default/files/ai21-476.pdf",
        ]
    },
    {
        "key": "nye2004",
        "title": "The effects of small classes on academic achievement: The results of the Tennessee class size experiment",
        "description": "Nye et al. 2004 STAR teacher quality gap d=0.34-0.48",
        "doi": "10.3102/01623737026001049",
        "urls": [
            "https://journals.sagepub.com/doi/pdf/10.3102/01623737026001049",
        ]
    },
    {
        "key": "angrist2013",
        "title": "Stand and deliver: Effects of Boston's charter high schools on college preparation, entry, and choice",
        "description": "Angrist et al. 2013 Boston charter schools d=0.40 math",
        "doi": "10.1162/REST_a_00323",
        "urls": [
            "https://economics.mit.edu/sites/default/files/publications/Stand%20and%20Deliver.pdf",
            "https://www.nber.org/system/files/working_papers/w19275/w19275.pdf",
        ]
    },
    {
        "key": "reardon2011",
        "title": "The widening academic achievement gap between the rich and the poor: New evidence and possible explanations",
        "description": "Reardon 2011 income-achievement gap 30-40% larger",
        "doi": None,
        "urls": [
            "https://cepa.stanford.edu/sites/default/files/reardon%20whither%20opportunity%20-%20chapter%205.pdf",
            "https://www.russellsage.org/sites/all/files/Whither_Opportunity/Reardon_Chapter%205.pdf",
        ]
    },
]

print("Attempting to fix wrong/broken PDFs...\n")

for paper in papers_to_fix:
    key = paper["key"]
    dest = CONSOLIDATED / f"{key}.pdf"
    print(f"\n{'='*60}")
    print(f"Fixing: {key}")
    print(f"  {paper['description']}")
    
    fixed = False
    
    # Try direct URLs first
    for url in paper["urls"]:
        if try_download(url, dest, f"{key} from {url[:50]}"):
            fixed = True
            break
        time.sleep(1)
    
    if not fixed:
        # Try Semantic Scholar
        print(f"  Trying Semantic Scholar...")
        pdf_url = search_semantic_scholar(paper["title"], "")
        if pdf_url:
            if try_download(pdf_url, dest, f"{key} from S2"):
                fixed = True
    
    if not fixed:
        # Try Unpaywall with DOI
        if paper.get("doi"):
            doi = paper["doi"]
            unpaywall_url = f"https://api.unpaywall.org/v2/{doi}?email=research@example.com"
            try:
                r = requests.get(unpaywall_url, timeout=20)
                if r.status_code == 200:
                    data = r.json()
                    best_oa = data.get("best_oa_location")
                    if best_oa and best_oa.get("url_for_pdf"):
                        pdf_url = best_oa["url_for_pdf"]
                        print(f"  Unpaywall found: {pdf_url[:60]}")
                        if try_download(pdf_url, dest, f"{key} from Unpaywall"):
                            fixed = True
            except Exception as e:
                print(f"  Unpaywall error: {e}")
    
    if fixed:
        # Verify the downloaded PDF
        try:
            doc = fitz.open(str(dest))
            text = "".join(page.get_text() for page in doc)
            doc.close()
            print(f"  ✓ VERIFIED: {len(text)} chars extracted")
        except Exception as e:
            print(f"  ✗ Verification failed: {e}")
    else:
        print(f"  ✗ FAILED to fix {key} - manual download needed")

print("\n\nDone. Checking credostanford2015 (scanned PDF issue)...")
# For CREDO, try to get a text-based version
credo_path = CONSOLIDATED / "credostanford2015.pdf"
doc = fitz.open(str(credo_path))
total_text = "".join(page.get_text() for page in doc)
print(f"CREDO PDF: {len(total_text)} chars, {doc.page_count} pages")
if len(total_text) < 1000:
    print("  This is a scanned/image PDF - need OCR or different version")
    # Try downloading a text-based version
    urls = [
        "https://credo.stanford.edu/wp-content/uploads/2021/08/2015-national-charter-school-study-executive-summary.pdf",
        "https://credo.stanford.edu/wp-content/uploads/2021/08/ncss_2015_executive_summary.pdf",
    ]
    for url in urls:
        if try_download(url, credo_path, "CREDO 2015"):
            doc2 = fitz.open(str(credo_path))
            text2 = "".join(page.get_text() for page in doc2)
            print(f"  New version: {len(text2)} chars")
            if len(text2) > 5000:
                print("  ✓ Got text-based version!")
            break
        time.sleep(1)
doc.close()
