"""
Semantic Scholar Citation Network Analysis
K-12 Education Evidence Synthesis

Queries the Semantic Scholar API for 15 anchor papers (one per cluster),
retrieves similar papers, top citing papers, and identifies papers
potentially missing from our review.
"""

import requests
import json
import time
import re
from pathlib import Path

BASE_URL = "https://api.semanticscholar.org/graph/v1"

# 15 anchor papers: one per cluster, identified by DOI or S2 paper ID
# Format: (cluster_name, doi_or_id, citation_key)
ANCHOR_PAPERS = [
    ("Cluster 1: Teacher Quality",          "10.1257/aer.104.9.2593",   "chetty2014"),
    ("Cluster 2: Early Childhood Ed",       "10.1257/aer.101.5.1980",   "heckman2011"),   # Heckman Perry
    ("Cluster 3: Class Size",               "10.1257/aer.89.4.749",     "krueger1999"),   # Krueger STAR
    ("Cluster 4: School Choice/Vouchers",   "10.1257/aer.102.5.2017",   "abdulkadiroglu2011"), # Boston/NYC
    ("Cluster 5: Charter Schools",          "10.1257/aer.101.5.2026",   "angrist2013"),   # KIPP
    ("Cluster 6: Curriculum & Instruction", "10.3102/0034654316669821", "slavin2016"),    # Slavin meta
    ("Cluster 7: SEL",                      "10.1111/j.1467-8624.2011.01589.x", "durlak2011"), # Durlak SEL meta
    ("Cluster 8: Technology",               "10.3102/0034654316672285", "escueta2017"),   # Escueta tech
    ("Cluster 9: Out-of-School",            "10.1257/aer.20150572",     "chetty2016"),    # MTO
    ("Cluster 10: International",           "10.1016/j.econedurev.2006.07.001", "wossmann2006"), # Woessmann
    ("Cluster 11: Citation Distortion",     "10.1136/bmj.b2680",        "greenberg2009"), # Greenberg BMJ
    ("Cross-cutting: Teacher Certification","10.1257/jep.24.3.133",     "hanushek2010"),  # Hanushek teacher quality
    ("Cross-cutting: School Finance",       "10.1093/qje/qjw002",       "jackson2016"),   # Jackson school finance
    ("Cross-cutting: Accountability",       "10.1257/aer.101.5.2157",   "deming2013"),    # Deming accountability
    ("Cross-cutting: Grit/Non-cognitive",   "10.1037/a0021890",         "duckworth2007"), # Duckworth grit
]

def get_paper_details(doi):
    """Fetch paper details from Semantic Scholar by DOI."""
    url = f"{BASE_URL}/paper/DOI:{doi}"
    params = {
        "fields": "paperId,title,authors,year,citationCount,referenceCount,fieldsOfStudy,abstract"
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"  [WARN] {doi} -> HTTP {r.status_code}")
            return None
    except Exception as e:
        print(f"  [ERROR] {doi}: {e}")
        return None

def get_similar_papers(paper_id, limit=20):
    """Fetch papers similar to the given S2 paper ID."""
    url = f"{BASE_URL}/paper/{paper_id}/recommendations"
    params = {"fields": "paperId,title,authors,year,citationCount,externalIds", "limit": limit}
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            return r.json().get("recommendedPapers", [])
        return []
    except Exception as e:
        print(f"  [ERROR] recommendations for {paper_id}: {e}")
        return []

def get_top_citing_papers(paper_id, limit=20):
    """Fetch the most-cited papers that cite the given S2 paper ID."""
    url = f"{BASE_URL}/paper/{paper_id}/citations"
    params = {
        "fields": "paperId,title,authors,year,citationCount,externalIds",
        "limit": 500  # fetch many, then sort by citation count
    }
    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code == 200:
            citations = r.json().get("data", [])
            # Each item has a "citingPaper" key
            papers = [c["citingPaper"] for c in citations if "citingPaper" in c]
            # Sort by citation count descending
            papers.sort(key=lambda x: x.get("citationCount", 0), reverse=True)
            return papers[:limit]
        return []
    except Exception as e:
        print(f"  [ERROR] citations for {paper_id}: {e}")
        return []

def doi_from_paper(paper):
    """Extract DOI from a paper's externalIds."""
    ext = paper.get("externalIds", {})
    return ext.get("DOI", ext.get("doi", ""))

def main():
    results = []
    all_candidate_papers = {}  # doi -> paper info, for deduplication

    print("=== Semantic Scholar Citation Network Analysis ===\n")

    for cluster, doi, key in ANCHOR_PAPERS:
        print(f"\n--- {cluster} ({key}) ---")
        print(f"  Fetching: {doi}")

        details = get_paper_details(doi)
        if not details:
            print(f"  [SKIP] Could not retrieve paper")
            results.append({"cluster": cluster, "key": key, "doi": doi,
                           "found": False, "similar": [], "top_citing": []})
            time.sleep(1)
            continue

        paper_id = details.get("paperId")
        title = details.get("title", "")
        citation_count = details.get("citationCount", 0)
        print(f"  Found: '{title[:70]}...' | Citations: {citation_count:,}")

        # Get similar papers
        print(f"  Fetching similar papers...")
        similar = get_similar_papers(paper_id, limit=20)
        time.sleep(0.5)

        # Get top citing papers
        print(f"  Fetching top citing papers...")
        top_citing = get_top_citing_papers(paper_id, limit=20)
        time.sleep(0.5)

        # Collect candidates
        for p in similar + top_citing:
            d = doi_from_paper(p)
            if d and d not in all_candidate_papers:
                all_candidate_papers[d] = p

        results.append({
            "cluster": cluster,
            "key": key,
            "doi": doi,
            "found": True,
            "paper_id": paper_id,
            "title": title,
            "citation_count": citation_count,
            "similar": [{"title": p.get("title",""), "year": p.get("year",""),
                         "citations": p.get("citationCount",0),
                         "doi": doi_from_paper(p),
                         "authors": [a.get("name","") for a in p.get("authors",[])[:3]]}
                        for p in similar],
            "top_citing": [{"title": p.get("title",""), "year": p.get("year",""),
                            "citations": p.get("citationCount",0),
                            "doi": doi_from_paper(p),
                            "authors": [a.get("name","") for a in p.get("authors",[])[:3]]}
                           for p in top_citing],
        })

        time.sleep(1)  # be polite to the API

    # Save full results
    out_path = Path("/home/ubuntu/k12-education-research/analysis/semantic_scholar_results.json")
    out_path.parent.mkdir(exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n\nFull results saved to {out_path}")

    # Now load our existing bib keys to check what's already covered
    bib_path = "/home/ubuntu/k12-education-research/drafts/k12_references.bib"
    with open(bib_path) as f:
        bib_text = f.read().lower()

    # Extract all DOIs already in our bib
    existing_dois = set(re.findall(r'doi\s*=\s*\{([^}]+)\}', bib_text))
    existing_dois = {d.lower().strip() for d in existing_dois}

    print("\n=== CANDIDATE PAPERS NOT IN CURRENT REVIEW ===\n")
    missing = []
    for doi, paper in sorted(all_candidate_papers.items(),
                              key=lambda x: x[1].get("citationCount", 0), reverse=True):
        doi_lower = doi.lower().strip()
        if doi_lower not in existing_dois:
            cites = paper.get("citationCount", 0)
            title = paper.get("title", "")
            year = paper.get("year", "")
            authors = [a.get("name", "") for a in paper.get("authors", [])[:2]]
            if cites >= 100:  # only flag highly-cited papers
                print(f"  [{cites:>5} cites] {authors[0] if authors else '?'} ({year}): {title[:80]}")
                missing.append({"doi": doi, "title": title, "year": year,
                                "authors": authors, "citations": cites})

    # Save missing papers report
    missing_path = Path("/home/ubuntu/k12-education-research/analysis/missing_papers_report.json")
    with open(missing_path, "w") as f:
        json.dump(missing, f, indent=2)
    print(f"\nMissing papers report saved to {missing_path}")
    print(f"\nTotal candidate papers surfaced: {len(all_candidate_papers)}")
    print(f"Highly-cited papers not in review (>=100 cites): {len(missing)}")

if __name__ == "__main__":
    main()
