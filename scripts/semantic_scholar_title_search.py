"""
Supplementary Semantic Scholar search by title for papers that failed DOI lookup.
Also produces a clean, curated missing-papers report filtered to education-relevant papers.
"""

import requests
import json
import time
import re
from pathlib import Path

BASE_URL = "https://api.semanticscholar.org/graph/v1"

# Papers that failed DOI lookup — search by title instead
TITLE_SEARCHES = [
    ("Cluster 2: Early Childhood Ed",    "heckman2011",  "The Rate of Return to the HighScope Perry Preschool Program"),
    ("Cluster 3: Class Size",            "krueger1999",  "Experimental Estimates of Education Production Functions"),
    ("Cluster 4: School Choice",         "abdulkadiroglu2011", "Accountability and Flexibility in Public Schools Evidence from Boston's Charters and Pilots"),
    ("Cluster 5: Charter Schools",       "angrist2013",  "Stand and Deliver Impact of Boston's Charter High Schools on College Preparation"),
    ("Cross-cutting: School Finance",    "jackson2016",  "The Effects of School Spending on Educational and Economic Outcomes Evidence from School Finance Reforms"),
]

def search_by_title(title, limit=3):
    url = f"{BASE_URL}/paper/search"
    params = {
        "query": title,
        "fields": "paperId,title,authors,year,citationCount,externalIds",
        "limit": limit
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            return r.json().get("data", [])
        return []
    except Exception as e:
        print(f"  [ERROR] search '{title[:50]}': {e}")
        return []

def get_similar_papers(paper_id, limit=20):
    url = f"{BASE_URL}/paper/{paper_id}/recommendations"
    params = {"fields": "paperId,title,authors,year,citationCount,externalIds", "limit": limit}
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            return r.json().get("recommendedPapers", [])
        return []
    except Exception as e:
        return []

def get_top_citing_papers(paper_id, limit=20):
    url = f"{BASE_URL}/paper/{paper_id}/citations"
    params = {"fields": "paperId,title,authors,year,citationCount,externalIds", "limit": 300}
    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code == 200:
            citations = r.json().get("data", [])
            papers = [c["citingPaper"] for c in citations if "citingPaper" in c]
            papers.sort(key=lambda x: x.get("citationCount") or 0, reverse=True)
            return papers[:limit]
        return []
    except Exception as e:
        return []

def doi_from_paper(paper):
    ext = paper.get("externalIds", {})
    return ext.get("DOI", ext.get("doi", ""))

# Education-relevant keywords to filter out spurious candidates
EDUCATION_KEYWORDS = [
    "school", "student", "teacher", "education", "learning", "classroom",
    "curriculum", "preschool", "kindergarten", "literacy", "math", "reading",
    "achievement", "academic", "charter", "voucher", "tutoring", "instruction",
    "pedagogy", "childhood", "adolescent", "college", "university", "skill",
    "cognitive", "noncognitive", "socioeconomic", "income", "poverty", "race",
    "equity", "gap", "test score", "grit", "mindset", "sel", "social emotional"
]

def is_education_relevant(title):
    title_lower = title.lower()
    return any(kw in title_lower for kw in EDUCATION_KEYWORDS)

def main():
    # Load existing results
    results_path = Path("/home/ubuntu/k12-education-research/analysis/semantic_scholar_results.json")
    with open(results_path) as f:
        existing_results = json.load(f)

    all_candidate_papers = {}

    # Collect candidates from existing results
    for r in existing_results:
        for p in r.get("similar", []) + r.get("top_citing", []):
            d = p.get("doi", "").lower().strip()
            if d:
                all_candidate_papers[d] = p

    print("=== Title-based searches for failed DOI lookups ===\n")

    new_results = []
    for cluster, key, title in TITLE_SEARCHES:
        print(f"\n--- {cluster} ({key}) ---")
        print(f"  Searching: '{title[:60]}...'")
        results = search_by_title(title, limit=3)
        time.sleep(0.5)

        if not results:
            print("  [SKIP] No results found")
            continue

        # Take the first result as the best match
        paper = results[0]
        paper_id = paper.get("paperId")
        found_title = paper.get("title", "")
        cites = paper.get("citationCount", 0)
        print(f"  Found: '{found_title[:70]}' | Citations: {cites:,}")

        similar = get_similar_papers(paper_id, limit=20)
        time.sleep(0.5)
        top_citing = get_top_citing_papers(paper_id, limit=20)
        time.sleep(0.5)

        for p in similar + top_citing:
            d = doi_from_paper(p).lower().strip()
            if d:
                all_candidate_papers[d] = p

        new_results.append({
            "cluster": cluster, "key": key, "found_title": found_title,
            "citation_count": cites,
            "similar": [{"title": p.get("title",""), "year": p.get("year",""),
                         "citations": p.get("citationCount",0), "doi": doi_from_paper(p),
                         "authors": [a.get("name","") for a in p.get("authors",[])[:3]]}
                        for p in similar],
            "top_citing": [{"title": p.get("title",""), "year": p.get("year",""),
                            "citations": p.get("citationCount",0), "doi": doi_from_paper(p),
                            "authors": [a.get("name","") for a in p.get("authors",[])[:3]]}
                           for p in top_citing],
        })

    # Save combined results
    combined_path = Path("/home/ubuntu/k12-education-research/analysis/semantic_scholar_combined.json")
    with open(combined_path, "w") as f:
        json.dump(existing_results + new_results, f, indent=2)

    # Load existing bib DOIs
    bib_path = "/home/ubuntu/k12-education-research/drafts/k12_references.bib"
    with open(bib_path) as f:
        bib_text = f.read().lower()
    existing_dois = set(re.findall(r'doi\s*=\s*\{([^}]+)\}', bib_text))
    existing_dois = {d.lower().strip() for d in existing_dois}

    # Also check titles already in bib (for papers without DOIs)
    bib_titles = set(re.findall(r'title\s*=\s*\{([^}]+)\}', bib_text))
    bib_titles = {t.lower().strip()[:40] for t in bib_titles}

    print("\n\n=== CURATED MISSING PAPERS (Education-relevant, >=100 cites) ===\n")
    curated_missing = []
    for doi, paper in sorted(all_candidate_papers.items(),
                              key=lambda x: x[1].get("citations", x[1].get("citationCount", 0)) or 0,
                              reverse=True):
        doi_lower = doi.lower().strip()
        title = paper.get("title", "")
        if not is_education_relevant(title):
            continue
        cites = paper.get("citations", paper.get("citationCount", 0)) or 0
        if cites < 100:
            continue
        if doi_lower in existing_dois:
            continue
        # Check if title already in bib
        title_key = title.lower().strip()[:40]
        if title_key in bib_titles:
            continue

        year = paper.get("year", "")
        authors = paper.get("authors", [])
        author_str = authors[0] if isinstance(authors[0], str) else authors[0].get("name", "") if authors else "?"
        print(f"  [{cites:>5} cites] {author_str} ({year}): {title[:90]}")
        curated_missing.append({
            "doi": doi, "title": title, "year": year,
            "first_author": author_str, "citations": cites
        })

    # Save curated report
    curated_path = Path("/home/ubuntu/k12-education-research/analysis/curated_missing_papers.json")
    with open(curated_path, "w") as f:
        json.dump(curated_missing, f, indent=2)

    print(f"\nTotal education-relevant missing papers (>=100 cites): {len(curated_missing)}")
    print(f"Saved to {curated_path}")

if __name__ == "__main__":
    main()
