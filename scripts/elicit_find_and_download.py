#!/usr/bin/env python3
"""
Use Elicit API to locate missing papers, get DOIs, then download via Semantic Scholar open-access PDFs.
"""

import os, requests, time, json, fitz
from pathlib import Path

ELICIT_KEY = "elk_live_dliSTcNbqzcwtBiQqzE5QeZbqOClWBfuP8xEAz2O4fU"
CONSOLIDATED = Path("/home/ubuntu/k12-education-research/literature/papers/consolidated")
HEADERS_ELICIT = {
    "Authorization": f"Bearer {ELICIT_KEY}",
    "Content-Type": "application/json",
}
HEADERS_DL = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
}

# Papers still missing — (bibtex_key, search_query)
MISSING = {
    "duckworth2009":     "Development and Validation of the Short Grit Scale Duckworth Quinn 2009",
    "morgan2016":        "Still No Effect of Resources Even in the New Gilded Age Morgan Jung 2016 Sociology of Education",
    "sahlberg2020":      "Finnish Lessons 3.0 What Can the World Learn from Educational Change in Finland Sahlberg 2020",
    "koedel2009":        "Value Added to What How a Ceiling in the Testing Instrument Influences Value-Added Estimation Koedel Betts 2009",
    "campbell2021":      "Developing Teachers as Professionals Lessons from High-Performing Systems Campbell OECD 2021",
    "ehri2001":          "Systematic Phonics Instruction Helps Students Learn to Read Evidence from the National Reading Panel's Meta-Analysis Ehri 2001",
    "sisk2018":          "To What Extent and Under Which Circumstances Are Growth Mind-Sets Important to Academic Achievement Sisk 2018",
    "yeager2016":        "Using Design Thinking to Improve Psychological Interventions Yeager 2016 PNAS growth mindset",
    "tan2020":           "Intensive Parenting Attitudes Tan 2020 Journal of Family Issues",
    "hanushek2011":      "The Economic Value of Higher Teacher Quality Hanushek 2011 Economics of Education Review",
    "campbell2014":      "Early Childhood Programs and Human Capital Abecedarian Project Campbell 2014",
    "lipsey2018":        "Translating the Statistical Representation of the Effects of Education Interventions Lipsey 2018",
    "hanushek2003":      "The Failure of Input-Based Schooling Policies Hanushek 2003 Economic Journal",
    "abdulkadirolu2018": "Research Design Meets Market Design Three Quasi-Experimental Studies of the Effects of Boston's Charter High Schools Abdulkadiroglu 2018",
    "howell2002":        "School Vouchers and Academic Performance Results from Three Randomized Field Trials Howell Peterson Wolf Campbell 2002",
    "castles2018":       "Ending the Reading Wars Reading Acquisition From Novice to Expert Castles Rastle Nation 2018",
    "kjeldsen2014":      "Gains from Training in Phonological Awareness in Kindergarten Kjeldsen 2014",
    "may2016":           "Reading Recovery Evaluation i3 Scale-Up May Sirinides 2016",
    "durlak2011":        "The Impact of Enhancing Students Social and Emotional Learning Durlak Weissberg 2011 Child Development",
    "rodriguez2018":     "Family Socioeconomic Status and Children Academic Achievement Rodriguez 2018",
    "hanushek2015":      "The Knowledge Capital of Nations Education and the Economics of Growth Hanushek Woessmann 2015",
    "greenberg2009":     "How Citation Distortions Create Unfounded Authority Analysis of a Citation Network Greenberg BMJ 2009",
    "sims2023":          "Quantifying Promising Trials Bias in Randomized Controlled Trials Sims 2023",
    "porter2022":        "Implementing the Every Student Succeeds Act Porter Fusarelli 2022",
    "mourshed2010":      "How the World Most Improved School Systems Keep Getting Better Mourshed Chijioke Barber McKinsey 2010",
    "hanford2018":       "Hard Words Why Aren't Kids Being Taught to Read Hanford APM Reports 2018",
}

def elicit_search(query, num_results=5):
    """Search Elicit for a paper and return top results."""
    url = "https://elicit.com/api/v1/search"
    payload = {
        "query": query,
        "numResults": num_results,
        "filters": {}
    }
    try:
        r = requests.post(url, headers=HEADERS_ELICIT, json=payload, timeout=20)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"  Elicit error {r.status_code}: {r.text[:200]}")
            return None
    except Exception as e:
        print(f"  Elicit request error: {e}")
        return None

def semantic_scholar_pdf(doi=None, title=None):
    """Try to get open-access PDF URL from Semantic Scholar."""
    headers = {"User-Agent": "research-bot/1.0 (mailto:research@example.com)"}
    
    if doi:
        url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=title,year,openAccessPdf,externalIds"
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                data = r.json()
                pdf_info = data.get("openAccessPdf")
                if pdf_info and pdf_info.get("url"):
                    return pdf_info["url"], data
        except Exception as e:
            print(f"  S2 DOI error: {e}")
    
    if title:
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={requests.utils.quote(title)}&fields=title,year,openAccessPdf,externalIds&limit=3"
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                data = r.json()
                papers = data.get("data", [])
                for p in papers:
                    pdf_info = p.get("openAccessPdf")
                    if pdf_info and pdf_info.get("url"):
                        return pdf_info["url"], p
        except Exception as e:
            print(f"  S2 title error: {e}")
    
    return None, None

def try_download(key, urls):
    """Try to download PDF from a list of URLs."""
    dest = CONSOLIDATED / f"{key}.pdf"
    for url in urls:
        if not url:
            continue
        try:
            r = requests.get(url, headers=HEADERS_DL, timeout=25, allow_redirects=True)
            if r.status_code == 200 and len(r.content) > 30000 and b'%PDF' in r.content[:10]:
                with open(dest, "wb") as f:
                    f.write(r.content)
                return len(r.content)
        except Exception as e:
            pass
    return 0

def verify_pdf(key):
    """Verify the PDF is readable and return first 200 chars of text."""
    dest = CONSOLIDATED / f"{key}.pdf"
    if not dest.exists():
        return None
    try:
        doc = fitz.open(str(dest))
        text = doc[0].get_text()[:200].replace('\n', ' ').strip()
        return text
    except:
        return None

# ============================================================
# MAIN LOOP
# ============================================================
results = {}

for key, query in MISSING.items():
    dest = CONSOLIDATED / f"{key}.pdf"
    if dest.exists() and dest.stat().st_size > 50000:
        print(f"✓ Already have {key}.pdf")
        continue
    
    print(f"\n{'='*60}")
    print(f"Searching: {key}")
    print(f"  Query: {query[:70]}...")
    
    # Step 1: Elicit search
    elicit_result = elicit_search(query, num_results=3)
    
    doi = None
    elicit_urls = []
    elicit_title = None
    
    if elicit_result:
        papers = elicit_result.get("papers", [])
        if papers:
            top = papers[0]
            doi = top.get("doi")
            elicit_urls = top.get("urls", [])
            elicit_title = top.get("title", "")
            year = top.get("year", "?")
            authors = top.get("authors", [])[:2]
            print(f"  Elicit top hit: {elicit_title[:60]} ({year}) by {authors}")
            if doi:
                print(f"  DOI: {doi}")
            if elicit_urls:
                print(f"  URLs: {elicit_urls[:2]}")
    
    # Step 2: Semantic Scholar for open-access PDF
    s2_pdf_url, s2_data = semantic_scholar_pdf(doi=doi, title=elicit_title or query[:80])
    if s2_pdf_url:
        print(f"  S2 open-access PDF: {s2_pdf_url[:70]}")
    
    # Step 3: Try to download
    all_urls = []
    if s2_pdf_url:
        all_urls.append(s2_pdf_url)
    all_urls.extend(elicit_urls)
    
    size = try_download(key, all_urls)
    
    if size > 0:
        text = verify_pdf(key)
        print(f"  ✓ Downloaded {key}.pdf ({size//1024}KB)")
        print(f"  Preview: {text[:120] if text else 'unreadable'}")
        results[key] = {"status": "downloaded", "doi": doi, "size_kb": size//1024}
    else:
        print(f"  ✗ Could not download {key}.pdf")
        results[key] = {"status": "missing", "doi": doi, "elicit_urls": elicit_urls}
    
    time.sleep(1.5)  # Rate limit

# ============================================================
# SUMMARY
# ============================================================
print(f"\n{'='*60}")
print("SUMMARY")
print(f"{'='*60}")
downloaded = [k for k, v in results.items() if v["status"] == "downloaded"]
still_missing = [k for k, v in results.items() if v["status"] == "missing"]

print(f"Downloaded: {len(downloaded)}")
for k in downloaded:
    print(f"  ✓ {k}")

print(f"\nStill missing: {len(still_missing)}")
for k in still_missing:
    doi = results[k].get("doi", "no DOI")
    urls = results[k].get("elicit_urls", [])
    print(f"  ✗ {k} | DOI: {doi} | URLs: {urls[:1]}")

# Save results
with open("/home/ubuntu/k12-education-research/literature/elicit_search_results.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\nTotal canonical PDFs in consolidated/: {len(list(CONSOLIDATED.glob('*.pdf')))}")
