#!/usr/bin/env python3
"""
fetch_missing_papers.py
Attempts to download missing papers via Unpaywall and Semantic Scholar APIs.
For each paper with a DOI, queries Unpaywall for an open-access PDF URL,
then downloads it to the correct cluster folder.
"""

import json, os, glob, requests, time, re, shutil
from pathlib import Path

REGISTRY_PATH = '/home/ubuntu/k12-education-research/literature/citation_registry_expanded.json'
PAPERS_DIR = '/home/ubuntu/k12-education-research/literature/papers'
EMAIL = 'ait11@case.edu'  # required by Unpaywall API

with open(REGISTRY_PATH) as f:
    registry = json.load(f)

# Build set of first_author+year combos already on disk
pdf_files = []
for f in glob.glob(f'{PAPERS_DIR}/**/*.pdf', recursive=True):
    pdf_files.append(os.path.basename(f).lower())

def already_have(entry):
    authors = entry.get('authors', [])
    year = str(entry.get('year', ''))
    if not authors:
        return False
    first_author = authors[0].split()[-1].lower()
    for pf in pdf_files:
        if first_author in pf and year in pf:
            return True
    return False

# Cluster folder mapping
CLUSTER_FOLDERS = {
    'Teacher Quality': 'cluster1_teacher_quality',
    'Early Childhood': 'cluster2_early_childhood',
    'Class Size': 'cluster3_class_size',
    'School Funding': 'cluster4_school_funding',
    'Charter Schools': 'cluster5_charter_vouchers',
    'Vouchers': 'cluster5_charter_vouchers',
    'Reading': 'cluster6_reading_instruction',
    'Tutoring': 'cluster7_tutoring',
    'SEL': 'cluster8_sel_noncognitive',
    'Non-Cognitive': 'cluster8_sel_noncognitive',
    'Out-of-School': 'cluster9_oos_factors',
    'International': 'cluster10_international',
}

def get_cluster_folder(entry):
    cluster = entry.get('cluster', '')
    for key, folder in CLUSTER_FOLDERS.items():
        if key.lower() in cluster.lower():
            return folder
    return 'misc'

def make_filename(entry):
    authors = entry.get('authors', [])
    year = str(entry.get('year', ''))
    title = entry.get('title', '')
    if authors:
        last = authors[0].split()[-1].lower()
        if len(authors) > 1:
            last2 = authors[1].split()[-1].lower()
            author_part = f"{last}_{last2}"
        else:
            author_part = last
    else:
        author_part = 'unknown'
    # Shorten title
    title_words = re.sub(r'[^a-z0-9 ]', '', title.lower()).split()[:5]
    title_part = '_'.join(title_words)
    return f"{author_part}_{year}_{title_part}.pdf"

def try_unpaywall(doi):
    """Query Unpaywall for open-access PDF URL."""
    if not doi:
        return None
    url = f"https://api.unpaywall.org/v2/{doi}?email={EMAIL}"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            # Try best_oa_location first
            best = data.get('best_oa_location')
            if best and best.get('url_for_pdf'):
                return best['url_for_pdf']
            # Try all oa_locations
            for loc in data.get('oa_locations', []):
                if loc.get('url_for_pdf'):
                    return loc['url_for_pdf']
    except Exception as e:
        print(f"  Unpaywall error: {e}")
    return None

def try_semantic_scholar(doi, title):
    """Query Semantic Scholar for open-access PDF URL."""
    pdf_url = None
    try:
        if doi:
            url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=openAccessPdf,externalIds"
        else:
            query = title[:80].replace(' ', '+')
            url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&fields=openAccessPdf,externalIds&limit=1"
        r = requests.get(url, timeout=15, headers={'User-Agent': 'k12-research/1.0'})
        if r.status_code == 200:
            data = r.json()
            if 'data' in data and data['data']:
                data = data['data'][0]
            oa = data.get('openAccessPdf')
            if oa and oa.get('url'):
                pdf_url = oa['url']
    except Exception as e:
        print(f"  S2 error: {e}")
    return pdf_url

def download_pdf(pdf_url, dest_path):
    """Download PDF from URL to dest_path."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; research-bot/1.0)',
            'Accept': 'application/pdf,*/*'
        }
        r = requests.get(pdf_url, timeout=30, headers=headers, allow_redirects=True)
        if r.status_code == 200 and len(r.content) > 10000:
            # Check it's actually a PDF
            if r.content[:4] == b'%PDF' or 'pdf' in r.headers.get('content-type', '').lower():
                with open(dest_path, 'wb') as f:
                    f.write(r.content)
                return True
            else:
                print(f"  Not a PDF (content-type: {r.headers.get('content-type', 'unknown')})")
        else:
            print(f"  HTTP {r.status_code}, size {len(r.content)}")
    except Exception as e:
        print(f"  Download error: {e}")
    return False

# Main loop
missing = [e for e in registry if not already_have(e)]
print(f"Papers already on disk: {len(registry) - len(missing)}")
print(f"Papers to fetch: {len(missing)}")
print()

downloaded = []
failed = []

for entry in missing:
    eid = entry.get('id')
    doi = entry.get('doi', '')
    title = entry.get('title', '')
    authors = entry.get('authors', [])
    year = entry.get('year', '')
    cluster = entry.get('cluster', '')
    
    author_str = authors[0] if authors else 'Unknown'
    print(f"[{eid}] {author_str} ({year}) — {title[:55]}...")
    
    # Try Unpaywall
    pdf_url = try_unpaywall(doi)
    source = 'Unpaywall'
    
    # Try Semantic Scholar if Unpaywall fails
    if not pdf_url:
        pdf_url = try_semantic_scholar(doi, title)
        source = 'SemanticScholar'
    
    if pdf_url:
        print(f"  Found via {source}: {pdf_url[:80]}")
        folder = get_cluster_folder(entry)
        dest_dir = os.path.join(PAPERS_DIR, folder)
        os.makedirs(dest_dir, exist_ok=True)
        filename = make_filename(entry)
        dest_path = os.path.join(dest_dir, filename)
        
        if download_pdf(pdf_url, dest_path):
            print(f"  ✓ Saved: {folder}/{filename}")
            downloaded.append({'id': eid, 'title': title, 'file': filename, 'source': source})
            pdf_files.append(filename.lower())  # update in-memory list
        else:
            print(f"  ✗ Download failed")
            failed.append({'id': eid, 'doi': doi, 'title': title, 'reason': 'download_failed', 'url': pdf_url})
    else:
        print(f"  ✗ No open-access version found")
        failed.append({'id': eid, 'doi': doi, 'title': title, 'reason': 'no_oa_version'})
    
    time.sleep(0.5)  # be polite to APIs

print(f"\n{'='*60}")
print(f"Downloaded: {len(downloaded)}")
print(f"Failed/No OA: {len(failed)}")
print()
print("FAILED (need CWRU download):")
for f in failed:
    print(f"  [{f['id']}] {f['title'][:60]} | DOI: {f['doi']} | Reason: {f['reason']}")

# Save results
with open('/home/ubuntu/k12-education-research/literature/fetch_results.json', 'w') as f:
    json.dump({'downloaded': downloaded, 'failed': failed}, f, indent=2)

print("\nResults saved to literature/fetch_results.json")
