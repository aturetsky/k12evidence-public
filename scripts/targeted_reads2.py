#!/usr/bin/env python3
"""Targeted section reads - fixed version."""

import fitz
import re
import requests
import time
from pathlib import Path

CONSOLIDATED = Path("/home/ubuntu/k12-education-research/literature/papers/consolidated")

print("="*70)
print("COOK 2015 - Finding actual math effect size (pages 15-30)")
print("="*70)
doc = fitz.open(str(CONSOLIDATED / "cook2015.pdf"))
full_text = "".join(doc[i].get_text() for i in range(doc.page_count))
page_count = doc.page_count

# Print pages 15-25 which likely contain main results
for pn in range(14, min(25, page_count)):
    pg_text = doc[pn].get_text()
    if any(x in pg_text.lower() for x in ["effect size", "standard deviation", "math gpa", "0.6", "0.5", "0.4", "result"]):
        print(f"\n[Page {pn+1}]: {pg_text[:800].replace(chr(10), ' ')}")
doc.close()

# Also search for specific effect size terms
print("\n--- Searching for effect size language in cook2015 ---")
for term in ["effect size", "standard deviation", "math GPA", "0.49", "0.50", "0.51", "0.52", "0.53", "0.54", "0.55", "0.56", "0.57", "0.58", "0.59", "0.60", "0.61", "0.62", "0.63", "0.64", "0.65", "0.66"]:
    idx = full_text.lower().find(term.lower())
    if idx >= 0:
        s = max(0, idx - 200)
        e = min(len(full_text), idx + len(term) + 300)
        snippet = full_text[s:e].replace('\n', ' ').strip()
        print(f"\n  '{term}': ...{snippet}...")
        if term in ["effect size", "standard deviation"]:
            # Find all occurrences
            count = full_text.lower().count(term.lower())
            print(f"  (appears {count} times total)")
        break

print("\n\n" + "="*70)
print("NYE 2004 - Finding 75th/25th percentile teacher gap")
print("="*70)
doc = fitz.open(str(CONSOLIDATED / "nye2004.pdf"))
full_text = "".join(doc[i].get_text() for i in range(doc.page_count))
page_count = doc.page_count

# Print all pages looking for the main result
for pn in range(page_count):
    pg_text = doc[pn].get_text()
    if any(x in pg_text.lower() for x in ["75th", "25th", "percentile", "quartile", "most effective", "least effective"]):
        print(f"\n[Page {pn+1}]: {pg_text[:1000].replace(chr(10), ' ')}")

# Also print pages 5-15 (main results)
print("\n--- Pages 5-15 of nye2004 ---")
for pn in range(4, min(15, page_count)):
    pg_text = doc[pn].get_text()
    if any(x in pg_text.lower() for x in ["0.34", "0.35", "0.36", "0.37", "0.38", "0.39", "0.40", "0.41", "0.42", "0.43", "0.44", "0.45", "0.46", "0.47", "0.48", "teacher effect"]):
        print(f"\n[Page {pn+1}]: {pg_text[:800].replace(chr(10), ' ')}")
doc.close()

print("\n\n" + "="*70)
print("ABDULKADIROLU 2018 - Full first page to identify paper")
print("="*70)
doc = fitz.open(str(CONSOLIDATED / "abdulkadirolu2018.pdf"))
full_text = "".join(doc[i].get_text() for i in range(doc.page_count))
print(f"First 800 chars:\n{full_text[:800].replace(chr(10), ' ')}")
print(f"\nTotal: {len(full_text)} chars, {doc.page_count} pages")

# Search for Louisiana and negative effects
for term in ["Louisiana", "voucher", "scholarship", "negative", "decline", "harmful", "-0.4", "−0.4"]:
    idx = full_text.lower().find(term.lower())
    if idx >= 0:
        s = max(0, idx - 150)
        e = min(len(full_text), idx + len(term) + 250)
        print(f"\n  '{term}': ...{full_text[s:e].replace(chr(10),' ')}...")
doc.close()

print("\n\n" + "="*70)
print("CREDOSTANFORD2015 - Try downloading text version")
print("="*70)
urls = [
    "https://credo.stanford.edu/wp-content/uploads/2021/08/2015-national-charter-school-study-executive-summary.pdf",
    "https://credo.stanford.edu/wp-content/uploads/2021/08/ncss_2015_exec_summary.pdf",
    "https://credo.stanford.edu/wp-content/uploads/2021/08/NCSS_2015_Executive_Summary.pdf",
    "https://credo.stanford.edu/wp-content/uploads/2021/08/ncss2015_exec_summary.pdf",
    "https://credo.stanford.edu/wp-content/uploads/2021/08/National_Charter_School_Study_2015.pdf",
]
headers = {"User-Agent": "Mozilla/5.0 (compatible; research bot)"}
success = False
for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=25)
        if r.status_code == 200 and len(r.content) > 50000 and r.content[:4] == b'%PDF':
            dest = CONSOLIDATED / "credostanford2015.pdf"
            with open(dest, 'wb') as f:
                f.write(r.content)
            doc = fitz.open(str(dest))
            text = "".join(doc[i].get_text() for i in range(doc.page_count))
            doc.close()
            print(f"  ✓ Downloaded: {url}")
            print(f"  {len(text)} chars, searching for key claims...")
            for term in ["72", "180", "days", "virtual", "learning days"]:
                idx = text.lower().find(term.lower())
                if idx >= 0:
                    s = max(0, idx-150)
                    e = min(len(text), idx+len(term)+200)
                    print(f"  '{term}': ...{text[s:e].replace(chr(10),' ')}...")
            success = True
            break
        else:
            print(f"  ✗ {url[:60]}: HTTP {r.status_code}, {len(r.content)} bytes")
    except Exception as e:
        print(f"  ✗ {url[:60]}: {e}")
    time.sleep(1)

if not success:
    print("  All URLs failed. CREDO 2015 full report needs manual download.")
    print("  The 72/180 days claim will be flagged as unverified.")
