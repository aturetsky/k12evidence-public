#!/usr/bin/env python3
"""
populate_dois_and_fetch.py
Step 1: Look up missing DOIs via Crossref API
Step 2: Re-run Unpaywall + Semantic Scholar to download open-access PDFs
Step 3: Report what still needs CWRU download
"""

import json, os, glob, requests, time, re, sys
from pathlib import Path
from urllib.parse import quote

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

REGISTRY_PATH = '/home/ubuntu/k12-education-research/literature/citation_registry_expanded.json'
PAPERS_DIR = '/home/ubuntu/k12-education-research/literature/papers'
EMAIL = 'ait11@case.edu'

with open(REGISTRY_PATH) as f:
    registry = json.load(f)

# ── Build accurate set of PDFs already on disk ──────────────────────────────
pdf_on_disk = {}  # id -> filepath
for fpath in glob.glob(f'{PAPERS_DIR}/**/*.pdf', recursive=True):
    pdf_on_disk[os.path.basename(fpath)] = fpath

def already_have_by_id(entry_id):
    """Check if any PDF file in any cluster folder matches this registry ID."""
    # We'll match by checking if the file exists with the canonical name
    for fname in pdf_on_disk:
        # canonical names include the ID or author+year
        pass
    return False

# More reliable: check by canonical filename we would assign
def canonical_filename(entry):
    authors = entry.get('authors', [])
    year = str(entry.get('year', ''))
    title = entry.get('title', '')
    if authors:
        last = re.sub(r'[^a-z]', '', authors[0].split()[-1].lower())
        if len(authors) > 1:
            last2 = re.sub(r'[^a-z]', '', authors[1].split()[-1].lower())
            author_part = f"{last}_{last2}"
        else:
            author_part = last
    else:
        author_part = 'unknown'
    title_words = re.sub(r'[^a-z0-9 ]', '', title.lower()).split()[:5]
    title_part = '_'.join(title_words)
    return f"{author_part}_{year}_{title_part}.pdf"

def already_have(entry):
    """Check if this entry's PDF is already on disk (by author+year match)."""
    authors = entry.get('authors', [])
    year = str(entry.get('year', ''))
    if not authors:
        return False
    first_author_last = re.sub(r'[^a-z]', '', authors[0].split()[-1].lower())
    for fname in pdf_on_disk:
        fname_lower = fname.lower()
        if first_author_last in fname_lower and year in fname_lower:
            return True
    return False

# ── Cluster folder mapping ───────────────────────────────────────────────────
CLUSTER_MAP = {
    'teacher': 'cluster1_teacher_quality',
    'early childhood': 'cluster2_early_childhood',
    'class size': 'cluster3_class_size',
    'school funding': 'cluster4_school_funding',
    'charter': 'cluster5_charter_vouchers',
    'voucher': 'cluster5_charter_vouchers',
    'reading': 'cluster6_reading_instruction',
    'tutoring': 'cluster7_tutoring',
    'sel': 'cluster8_sel_noncognitive',
    'noncognitive': 'cluster8_sel_noncognitive',
    'non-cognitive': 'cluster8_sel_noncognitive',
    'out-of-school': 'cluster9_oos_factors',
    'summer': 'cluster9_oos_factors',
    'neighborhood': 'cluster9_oos_factors',
    'international': 'cluster10_international',
}

def get_folder(entry):
    cluster = entry.get('cluster', '').lower()
    for key, folder in CLUSTER_MAP.items():
        if key in cluster:
            return folder
    # fallback by title keywords
    title = entry.get('title', '').lower()
    for key, folder in CLUSTER_MAP.items():
        if key in title:
            return folder
    return 'misc'

# ── Step 1: Look up missing DOIs via Crossref ────────────────────────────────
print("=" * 60)
print("STEP 1: Populating missing DOIs via Crossref")
print("=" * 60)

missing_entries = [e for e in registry if not already_have(e)]
print(f"Entries needing PDFs: {len(missing_entries)}")
print(f"PDFs already on disk: {len(registry) - len(missing_entries)}")
print()

doi_found = 0
doi_updated = []

for entry in missing_entries:
    eid = entry.get('id')
    doi = entry.get('doi', '').strip()
    title = entry.get('title', '')
    authors = entry.get('authors', [])
    year = entry.get('year', '')
    
    if doi:
        continue  # already has DOI
    
    # Query Crossref
    author_query = authors[0].split()[-1] if authors else ''
    query = f"{title[:80]}"
    url = f"https://api.crossref.org/works?query.title={quote(query)}&query.author={quote(author_query)}&filter=from-pub-date:{year},until-pub-date:{year}&rows=3&mailto={EMAIL}"
    
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            items = r.json().get('message', {}).get('items', [])
            for item in items:
                item_doi = item.get('DOI', '')
                item_title = item.get('title', [''])[0].lower()
                # Check title similarity
                if title.lower()[:30] in item_title or item_title[:30] in title.lower():
                    entry['doi'] = item_doi
                    doi_found += 1
                    doi_updated.append({'id': eid, 'title': title[:50], 'doi': item_doi})
                    print(f"  [ID {eid}] Found DOI: {item_doi} — {title[:50]}")
                    break
    except Exception as e:
        pass
    
    time.sleep(0.3)

print(f"\nDOIs found: {doi_found}")

# Save updated registry with new DOIs
with open(REGISTRY_PATH, 'w') as f:
    json.dump(registry, f, indent=2)
print("Registry updated with new DOIs.")

# ── Step 2: Fetch via Unpaywall + Semantic Scholar ───────────────────────────
print()
print("=" * 60)
print("STEP 2: Fetching open-access PDFs")
print("=" * 60)

def try_unpaywall(doi):
    if not doi:
        return None, None
    url = f"https://api.unpaywall.org/v2/{doi}?email={EMAIL}"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            best = data.get('best_oa_location')
            if best and best.get('url_for_pdf'):
                return best['url_for_pdf'], 'Unpaywall'
            for loc in data.get('oa_locations', []):
                if loc.get('url_for_pdf'):
                    return loc['url_for_pdf'], 'Unpaywall'
    except:
        pass
    return None, None

def try_semantic_scholar(doi, title):
    try:
        if doi:
            url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=openAccessPdf"
        else:
            q = quote(title[:80])
            url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={q}&fields=openAccessPdf&limit=1"
        r = requests.get(url, timeout=15, headers={'User-Agent': 'k12-research/1.0'})
        if r.status_code == 200:
            data = r.json()
            if 'data' in data and data['data']:
                data = data['data'][0]
            oa = data.get('openAccessPdf')
            if oa and oa.get('url'):
                return oa['url'], 'SemanticScholar'
    except:
        pass
    return None, None

def download_pdf(pdf_url, dest_path):
    try:
        headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/pdf,*/*'}
        r = requests.get(pdf_url, timeout=45, headers=headers, allow_redirects=True)
        if r.status_code == 200 and len(r.content) > 5000:
            if r.content[:4] == b'%PDF' or 'pdf' in r.headers.get('content-type', '').lower():
                with open(dest_path, 'wb') as f:
                    f.write(r.content)
                return True
    except Exception as e:
        pass
    return False

downloaded = []
still_needed = []

# Re-read missing entries (DOIs may have been updated)
missing_entries = [e for e in registry if not already_have(e)]

for entry in missing_entries:
    eid = entry.get('id')
    doi = entry.get('doi', '').strip()
    title = entry.get('title', '')
    authors = entry.get('authors', [])
    year = entry.get('year', '')
    
    author_str = authors[0] if authors else 'Unknown'
    print(f"\n[{eid}] {author_str} ({year}) — {title[:55]}...")
    if doi:
        print(f"  DOI: {doi}")
    
    # Try Unpaywall
    pdf_url, source = try_unpaywall(doi)
    
    # Try Semantic Scholar
    if not pdf_url:
        pdf_url, source = try_semantic_scholar(doi, title)
    
    if pdf_url:
        print(f"  Found via {source}: {pdf_url[:90]}")
        folder = get_folder(entry)
        dest_dir = os.path.join(PAPERS_DIR, folder)
        os.makedirs(dest_dir, exist_ok=True)
        filename = canonical_filename(entry)
        dest_path = os.path.join(dest_dir, filename)
        
        if download_pdf(pdf_url, dest_path):
            size_kb = os.path.getsize(dest_path) // 1024
            print(f"  ✓ Saved ({size_kb} KB): {folder}/{filename}")
            downloaded.append({'id': eid, 'title': title, 'file': filename, 'source': source})
            pdf_on_disk[filename] = dest_path
        else:
            print(f"  ✗ Download failed (URL may require auth)")
            still_needed.append({'id': eid, 'doi': doi, 'title': title, 'authors': authors, 'year': year, 'journal': entry.get('journal','')})
    else:
        print(f"  ✗ No open-access version found")
        still_needed.append({'id': eid, 'doi': doi, 'title': title, 'authors': authors, 'year': year, 'journal': entry.get('journal','')})
    
    time.sleep(0.5)

# ── Step 3: Generate EZproxy links for remaining ─────────────────────────────
print()
print("=" * 60)
print(f"RESULTS: Downloaded {len(downloaded)}, Still needed: {len(still_needed)}")
print("=" * 60)

print("\n✓ DOWNLOADED:")
for d in downloaded:
    print(f"  [{d['id']}] {d['title'][:60]} ({d['source']})")

print("\n✗ STILL NEEDED (EZproxy links):")
EZPROXY = "https://ezproxy.case.edu/login?url="
for s in still_needed:
    doi = s.get('doi', '')
    if doi:
        publisher_url = f"https://doi.org/{doi}"
        ezproxy_url = f"{EZPROXY}{publisher_url}"
    else:
        ezproxy_url = f"Search manually: {s['title'][:60]}"
    print(f"  [{s['id']}] {s['authors'][0] if s['authors'] else '?'} ({s['year']}) — {s['title'][:50]}")
    print(f"         {ezproxy_url}")

# Save results
results = {'downloaded': downloaded, 'still_needed': still_needed}
with open('/home/ubuntu/k12-education-research/literature/fetch_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("\nFull results saved to literature/fetch_results.json")
