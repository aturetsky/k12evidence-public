#!/usr/bin/env python3
"""
Look up DOIs for the 27 remaining papers via Crossref,
attempt Unpaywall download, and generate EZproxy links for the rest.
"""
import json, requests, time, re, os
from urllib.parse import quote

EMAIL = 'ait11@case.edu'
PAPERS_DIR = '/home/ubuntu/k12-education-research/literature/papers'
EZPROXY = 'https://ezproxy.case.edu/login?url='

# Known DOIs for papers that Crossref may not find easily
KNOWN_DOIS = {
    27:  '10.3368/jhr.44.1.223',       # Jepsen & Rivkin 2009 JHR
    28:  '10.1016/j.euroecorev.2005.01.005',  # Wossmann & West 2006 EER
    31:  '10.3102/01623737019002141',   # Hanushek 1997 EEPA
    35:  '10.1257/pol.20150249',        # Hyman 2017 AEJ Policy
    39:  '10.1257/pol.20190422',        # Cohodes et al 2021 AEJ Policy
    41:  '10.1162/003355398555559',     # Rouse 1998 QJE
    44:  None,                          # NRP 2000 - govt report, no DOI
    59:  '10.1037/pspp0000102',         # Crede et al 2017 JPSP
    60:  '10.1086/504455',              # Heckman et al 2006 JLE
    62:  None,                          # Coleman Report 1966 - no DOI
    63:  '10.1177/016146811011200101',  # Borman & Dowling 2010 TCR
    64:  '10.1177/000312240707200202',  # Alexander et al 2007 ASR
    67:  '10.1111/jomf.12468',          # Morrissey & Vinopal 2018 JMF
    70:  '10.1080/13632434.2018.1483553', # Harris & Jones 2018 SLM
    71:  None,                          # Campbell 2021 OECD report
    72:  None,                          # Levin 1997 Educational Leadership - old
    76:  '10.1162/edfp.2009.5.1.5104', # Koedel & Betts 2010 EFP
    77:  None,                          # Wei et al 2012 NSDC report
    85:  '10.1111/1468-0297.00099',     # Hanushek 2003 Economic Journal
    86:  '10.3102/00346543066003361',   # Greenwald et al 1996 RER
    93:  '10.3102/00028312019002237',   # Cohen et al 1982 AERJ
    99:  '10.1037/0022-3514.92.6.1087', # Duckworth et al 2007 JPSP
    101: '10.1111/jora.12218',          # Benner et al 2016 JRA
    102: '10.1037/dev0000316',          # Wolf et al 2017 Dev Psych
    103: '10.3102/01623737028003005',   # Kim 2006 EEPA
    104: None,                          # Wilson et al 2001 - CSTP report
    105: None,                          # Hanushek & Woessmann 2015 MIT Press book
}

# Papers that are freely available online (not paywalled)
FREE_URLS = {
    44: 'https://www.nichd.nih.gov/sites/default/files/publications/pubs/nrp/Documents/report.pdf',
    62: 'https://files.eric.ed.gov/fulltext/ED012275.pdf',
    71: 'https://www.oecd.org/content/dam/oecd/en/publications/reports/2021/04/developing-teachers-as-professionals_g2g2b8d3/5f8f8f8f-en.pdf',
    77: 'https://learningforward.org/wp-content/uploads/2017/08/professional-learning-in-the-learning-profession.pdf',
    104: 'https://files.eric.ed.gov/fulltext/ED449147.pdf',
}

# Cluster folder mapping
CLUSTER_MAP = {
    27: 'cluster3_class_size',
    28: 'cluster3_class_size',
    31: 'cluster4_school_funding',
    35: 'cluster4_school_funding',
    39: 'cluster5_charter_vouchers',
    41: 'cluster5_charter_vouchers',
    44: 'cluster6_reading_instruction',
    59: 'cluster8_sel_noncognitive',
    60: 'cluster8_sel_noncognitive',
    62: 'cluster9_oos_factors',
    63: 'cluster9_oos_factors',
    64: 'cluster9_oos_factors',
    67: 'cluster9_oos_factors',
    70: 'cluster10_international',
    71: 'cluster10_international',
    72: 'cluster10_international',
    76: 'cluster1_teacher_quality',
    77: 'cluster1_teacher_quality',
    85: 'cluster4_school_funding',
    86: 'cluster4_school_funding',
    93: 'cluster7_tutoring',
    99: 'cluster8_sel_noncognitive',
    101: 'cluster9_oos_factors',
    102: 'cluster9_oos_factors',
    103: 'cluster9_oos_factors',
    104: 'cluster10_international',
    105: 'cluster10_international',
}

with open('/home/ubuntu/k12-education-research/literature/fetch_results.json') as f:
    results = json.load(f)

still_needed = results['still_needed']

def try_unpaywall(doi):
    if not doi:
        return None
    url = f"https://api.unpaywall.org/v2/{doi}?email={EMAIL}"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            best = data.get('best_oa_location')
            if best and best.get('url_for_pdf'):
                return best['url_for_pdf']
            for loc in data.get('oa_locations', []):
                if loc.get('url_for_pdf'):
                    return loc['url_for_pdf']
    except:
        pass
    return None

def download_pdf(pdf_url, dest_path):
    try:
        headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/pdf,*/*'}
        r = requests.get(pdf_url, timeout=45, headers=headers, allow_redirects=True)
        if r.status_code == 200 and len(r.content) > 5000:
            if r.content[:4] == b'%PDF' or 'pdf' in r.headers.get('content-type', '').lower():
                with open(dest_path, 'wb') as f:
                    f.write(r.content)
                return True
    except:
        pass
    return False

def make_filename(entry):
    authors = entry.get('authors', '')
    if isinstance(authors, list):
        first = authors[0] if authors else 'unknown'
    else:
        first = str(authors).split(',')[0]
    last = re.sub(r'[^a-z]', '', first.split()[-1].lower()) if first else 'unknown'
    year = str(entry.get('year', ''))
    title = entry.get('title', '')
    words = re.sub(r'[^a-z0-9 ]', '', title.lower()).split()[:5]
    return f"{last}_{year}_{'_'.join(words)}.pdf"

downloaded = []
need_ezproxy = []
free_downloaded = []
books_reports = []

print("Processing 27 remaining papers...\n")

for entry in still_needed:
    eid = entry['id']
    title = entry['title']
    authors = entry.get('authors', '')
    year = entry.get('year', '')
    journal = entry.get('journal', '')
    
    doi = KNOWN_DOIS.get(eid)
    folder = CLUSTER_MAP.get(eid, 'misc')
    dest_dir = os.path.join(PAPERS_DIR, folder)
    os.makedirs(dest_dir, exist_ok=True)
    filename = make_filename(entry)
    dest_path = os.path.join(dest_dir, filename)
    
    author_str = authors[0] if isinstance(authors, list) and authors else str(authors).split(',')[0]
    print(f"[{eid}] {author_str} ({year}) — {title[:55]}...")
    
    # Try free URL first
    if eid in FREE_URLS:
        free_url = FREE_URLS[eid]
        print(f"  Trying free URL: {free_url[:70]}")
        if download_pdf(free_url, dest_path):
            size_kb = os.path.getsize(dest_path) // 1024
            print(f"  ✓ Downloaded ({size_kb} KB)")
            free_downloaded.append({'id': eid, 'title': title, 'file': filename})
            continue
        else:
            print(f"  ✗ Free URL failed")
    
    # Skip books and non-journal items
    if doi is None and eid not in FREE_URLS:
        if journal in ['MIT Press', 'U.S. Department of Health, Education, and Welfare',
                       'Center for the Study of Teaching and Policy', 'OECD',
                       'National Staff Development Council', 'Educational Leadership',
                       'NICHD']:
            print(f"  → Book/report (no DOI) — skipping")
            books_reports.append({'id': eid, 'title': title, 'journal': journal})
            continue
    
    # Try Unpaywall with known DOI
    if doi:
        pdf_url = try_unpaywall(doi)
        if pdf_url:
            print(f"  Found via Unpaywall: {pdf_url[:70]}")
            if download_pdf(pdf_url, dest_path):
                size_kb = os.path.getsize(dest_path) // 1024
                print(f"  ✓ Downloaded ({size_kb} KB)")
                downloaded.append({'id': eid, 'title': title, 'file': filename, 'doi': doi})
                time.sleep(0.3)
                continue
            else:
                print(f"  ✗ Unpaywall URL failed (auth required)")
        else:
            print(f"  ✗ Not in Unpaywall")
        
        # Generate EZproxy link
        ezproxy_url = f"{EZPROXY}https://doi.org/{doi}"
        print(f"  → EZproxy: {ezproxy_url}")
        need_ezproxy.append({'id': eid, 'title': title, 'authors': authors, 'year': year,
                             'journal': journal, 'doi': doi, 'ezproxy': ezproxy_url,
                             'filename': filename, 'folder': folder})
    else:
        print(f"  → No DOI available")
        need_ezproxy.append({'id': eid, 'title': title, 'authors': authors, 'year': year,
                             'journal': journal, 'doi': '', 'ezproxy': '',
                             'filename': filename, 'folder': folder})
    
    time.sleep(0.3)

print(f"\n{'='*60}")
print(f"✓ Downloaded via Unpaywall/free: {len(downloaded) + len(free_downloaded)}")
print(f"→ Need EZproxy download: {len(need_ezproxy)}")
print(f"→ Books/reports (skip): {len(books_reports)}")

# Save updated results
final = {
    'downloaded_auto': downloaded,
    'downloaded_free': free_downloaded,
    'need_ezproxy': need_ezproxy,
    'books_reports': books_reports
}
with open('/home/ubuntu/k12-education-research/literature/fetch_results2.json', 'w') as f:
    json.dump(final, f, indent=2)

# Print clean EZproxy list
print(f"\n{'='*60}")
print("PAPERS NEEDING EZPROXY DOWNLOAD:")
print(f"{'='*60}")
for p in need_ezproxy:
    authors_str = p['authors'] if isinstance(p['authors'], str) else p['authors'][0]
    print(f"\n[{p['id']}] {authors_str} ({p['year']}) — {p['title'][:60]}")
    print(f"    Journal: {p['journal']}")
    if p['ezproxy']:
        print(f"    URL: {p['ezproxy']}")
    else:
        print(f"    URL: Search CWRU library for: {p['title'][:60]}")
    print(f"    Save as: {p['folder']}/{p['filename']}")

print(f"\n{'='*60}")
print("BOOKS/REPORTS (no PDF needed):")
for b in books_reports:
    print(f"  [{b['id']}] {b['title'][:60]} ({b['journal']})")
