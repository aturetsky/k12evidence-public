#!/usr/bin/env python3
"""Targeted section reads to find specific claims."""

import fitz
import re
from pathlib import Path

CONSOLIDATED = Path("/home/ubuntu/k12-education-research/literature/papers/consolidated")

def get_page_text(key, page_nums):
    """Get text from specific pages."""
    doc = fitz.open(str(CONSOLIDATED / f"{key}.pdf"))
    texts = {}
    for pn in page_nums:
        if pn < doc.page_count:
            texts[pn] = doc[pn].get_text()
    doc.close()
    return texts

def search_all(key, terms, context=400):
    """Search for all terms and return first match with context."""
    doc = fitz.open(str(CONSOLIDATED / f"{key}.pdf"))
    text = "".join(page.get_text() for page in doc)
    doc.close()
    for term in terms:
        idx = text.lower().find(term.lower())
        if idx >= 0:
            s = max(0, idx - context//2)
            e = min(len(text), idx + len(term) + context//2)
            return term, text[s:e].replace('\n', ' ').strip()
    return None, None

print("="*70)
print("COOK 2015 - Finding actual math effect size")
print("="*70)
doc = fitz.open(str(CONSOLIDATED / "cook2015.pdf"))
text = "".join(page.get_text() for page in doc)
doc.close()

# Look for the results section - math GPA or standardized test
for term in ["math GPA", "math grade point", "standardized math", "math test", 
             "grade point average", "GPA", "course grade", "0.48", "0.49", "0.50",
             "0.51", "0.52", "0.53", "0.54", "0.55", "0.56", "0.57", "0.58", "0.59",
             "0.60", "0.61", "0.62", "0.63", "0.64"]:
    idx = text.lower().find(term.lower())
    if idx >= 0:
        s = max(0, idx - 200)
        e = min(len(text), idx + len(term) + 300)
        snippet = text[s:e].replace('\n', ' ').strip()
        print(f"\n  '{term}': ...{snippet}...")
        break

# Print pages 15-20 which likely contain main results
print("\n--- Pages 15-20 of cook2015 (results section) ---")
for pn in range(14, 20):
    if pn < doc.page_count:
        doc2 = fitz.open(str(CONSOLIDATED / "cook2015.pdf"))
        pg_text = doc2[pn].get_text()
        doc2.close()
        if any(x in pg_text.lower() for x in ["effect", "standard deviation", "math", "gpa", "0."]):
            print(f"\n[Page {pn+1}]: {pg_text[:600].replace(chr(10), ' ')}")

print("\n\n" + "="*70)
print("NYE 2004 - Finding 75th/25th percentile teacher gap")
print("="*70)
doc = fitz.open(str(CONSOLIDATED / "nye2004.pdf"))
text = "".join(page.get_text() for page in doc)
doc.close()

# Look for the key result about teacher quality gap
for term in ["75th percentile", "25th percentile", "top quartile", "bottom quartile",
             "most effective", "least effective", "difference between teachers",
             "teacher at the 75", "teacher at the 25", "0.34", "0.48"]:
    idx = text.lower().find(term.lower())
    if idx >= 0:
        s = max(0, idx - 200)
        e = min(len(text), idx + len(term) + 400)
        snippet = text[s:e].replace('\n', ' ').strip()
        print(f"\n  '{term}': ...{snippet}...")
        break

# Print the abstract and conclusion
print("\n--- Abstract/intro of nye2004 ---")
doc2 = fitz.open(str(CONSOLIDATED / "nye2004.pdf"))
for pn in range(min(3, doc2.page_count)):
    pg = doc2[pn].get_text()
    print(f"\n[Page {pn+1}]: {pg[:800].replace(chr(10), ' ')}")
doc2.close()

print("\n\n" + "="*70)
print("ABDULKADIROLU 2018 - Verifying this is the Louisiana voucher paper")
print("="*70)
doc = fitz.open(str(CONSOLIDATED / "abdulkadirolu2018.pdf"))
text = "".join(page.get_text() for page in doc)
doc.close()

print(f"First 600 chars: {text[:600].replace(chr(10), ' ')}")
for term in ["Louisiana", "voucher", "scholarship", "negative", "-0.4", "−0.4", "decline"]:
    idx = text.lower().find(term.lower())
    if idx >= 0:
        s = max(0, idx - 150)
        e = min(len(text), idx + len(term) + 200)
        snippet = text[s:e].replace('\n', ' ').strip()
        print(f"\n  '{term}': ...{snippet}...")
        break

print("\n\n" + "="*70)
print("CREDOSTANFORD2015 - Attempting to get readable version")
print("="*70)
import requests, time

# Try the CREDO national charter school study text version
urls = [
    "https://credo.stanford.edu/wp-content/uploads/2021/08/2015-national-charter-school-study-executive-summary.pdf",
    "https://credo.stanford.edu/wp-content/uploads/2021/08/ncss_2015_executive_summary.pdf",
    "https://credo.stanford.edu/wp-content/uploads/2021/08/national_charter_school_study_2015.pdf",
    "https://credo.stanford.edu/wp-content/uploads/2021/08/ncss2015_execsummary.pdf",
]

headers = {"User-Agent": "Mozilla/5.0 (compatible; research bot)"}
for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200 and r.content[:4] == b'%PDF' and len(r.content) > 50000:
            dest = CONSOLIDATED / "credostanford2015.pdf"
            with open(dest, 'wb') as f:
                f.write(r.content)
            doc = fitz.open(str(dest))
            text = "".join(page.get_text() for page in doc)
            doc.close()
            print(f"  ✓ Downloaded from {url}")
            print(f"  {len(text)} chars extracted")
            # Search for key claims
            for term in ["72", "180", "days", "virtual", "learning"]:
                idx = text.lower().find(term.lower())
                if idx >= 0:
                    s = max(0, idx-150)
                    e = min(len(text), idx+len(term)+150)
                    print(f"  '{term}': ...{text[s:e].replace(chr(10),' ')}...")
                    break
            break
        else:
            print(f"  ✗ {url}: HTTP {r.status_code}, {len(r.content)} bytes")
    except Exception as e:
        print(f"  ✗ {url}: {e}")
    time.sleep(1)
