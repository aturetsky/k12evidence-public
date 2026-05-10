#!/usr/bin/env python3
"""Precision checks on 6 claims that need closer inspection."""

import fitz
import re
from pathlib import Path

CONSOLIDATED = Path("/home/ubuntu/k12-education-research/literature/papers/consolidated")

def get_text(key):
    doc = fitz.open(str(CONSOLIDATED / f"{key}.pdf"))
    text = "".join(page.get_text() for page in doc)
    doc.close()
    return text

def show_all(text, term, context=300, max_hits=3):
    results = []
    text_lower = text.lower()
    term_lower = term.lower()
    start = 0
    count = 0
    while count < max_hits:
        idx = text_lower.find(term_lower, start)
        if idx < 0:
            break
        s = max(0, idx - context//2)
        e = min(len(text), idx + len(term) + context//2)
        results.append(text[s:e].replace('\n', ' ').strip())
        start = idx + 1
        count += 1
    return results

print("="*70)
print("1. ANGRIST 2013 — Manuscript: 'd=0.40 in math per year'")
print("   Paper actually says: 0.4σ ELA and ~0.6σ math at HIGH SCHOOL level")
print("="*70)
text = get_text("angrist2013")
for term in ["standard deviation", "0.4", "0.6", "per year", "math score", "ELA"]:
    hits = show_all(text, term, 300, 2)
    if hits:
        print(f"\n  '{term}':")
        for h in hits:
            print(f"    ...{h}...")
        break

# Get the key result sentence
for term in ["a third of a standard deviation", "fifth of a standard deviation", "four-tenths", "0.4j", "0.4σ"]:
    hits = show_all(text, term, 400, 2)
    if hits:
        print(f"\n  KEY RESULT '{term}':")
        for h in hits:
            print(f"    ...{h}...")

print("\n\n" + "="*70)
print("2. COOK 2015 — Manuscript: 'd=0.65 math'; need actual effect size")
print("="*70)
text = get_text("cook2015")
# Look for the actual math achievement effect
for term in ["math", "achievement", "standard deviation", "effect size", "0.1", "0.2", "0.3", "0.4", "0.5"]:
    hits = show_all(text, term, 300, 2)
    if hits:
        print(f"\n  '{term}':")
        for h in hits[:1]:
            print(f"    ...{h}...")

# Print pages 20-30 for results
doc = fitz.open(str(CONSOLIDATED / "cook2015.pdf"))
print("\n  --- Pages 20-35 (results section) ---")
for pn in range(19, min(35, doc.page_count)):
    pg = doc[pn].get_text()
    if any(x in pg.lower() for x in ["standard deviation", "effect size", "math gpa", "0.3", "0.4", "0.5", "0.6"]):
        print(f"\n  [Page {pn+1}]: {pg[:600].replace(chr(10), ' ')}")
doc.close()

print("\n\n" + "="*70)
print("3. NYE 2004 — Manuscript: 'd=0.34-0.48 gap between 75th/25th percentile'")
print("="*70)
text = get_text("nye2004")
hits = show_all(text, "75th", 500, 3)
for h in hits:
    print(f"  ...{h}...")

# Find the specific result about teacher quality gap
for term in ["difference between", "gap between", "effective teacher", "0.34", "0.48", "quartile"]:
    hits = show_all(text, term, 400, 2)
    if hits:
        print(f"\n  '{term}':")
        for h in hits[:1]:
            print(f"    ...{h}...")

print("\n\n" + "="*70)
print("4. CREDOSTANFORD2015 — Manuscript: '72 days math, 180 days reading'")
print("="*70)
text = get_text("credostanford2015")
# Find both 72 and 180 days
for term in ["72 days", "180 days", "72-day", "180-day", "days of learning"]:
    hits = show_all(text, term, 400, 3)
    if hits:
        print(f"\n  '{term}':")
        for h in hits[:2]:
            print(f"    ...{h}...")

# Also look for the main result table
for term in ["reading", "math", "online charter", "virtual"]:
    hits = show_all(text, term, 300, 1)
    if hits:
        print(f"\n  '{term}':")
        for h in hits[:1]:
            print(f"    ...{h}...")
        break

print("\n\n" + "="*70)
print("5. ABDULKADIROLU 2018 — Manuscript: 'd=-0.40 math first year'")
print("   Need to confirm it's NEGATIVE 0.4")
print("="*70)
text = get_text("abdulkadirolu2018")
for term in ["-0.4", "−0.4", "lowers math", "lower math", "negative", "0.4 standard"]:
    hits = show_all(text, term, 400, 2)
    if hits:
        print(f"\n  '{term}':")
        for h in hits[:2]:
            print(f"    ...{h}...")
        if "-0.4" in term or "lowers" in term:
            break

print("\n\n" + "="*70)
print("6. HECKMAN 2010 — Manuscript: '7-12% annual ROI, effects to age 40'")
print("="*70)
text = get_text("heckman2010")
for term in ["7 to 12", "7-12", "7 percent", "12 percent", "return on investment", "ROI", "annual return", "age 40"]:
    hits = show_all(text, term, 400, 2)
    if hits:
        print(f"\n  '{term}':")
        for h in hits[:2]:
            print(f"    ...{h}...")
        if "7" in term and ("12" in term or "percent" in term):
            break

print("\n\n" + "="*70)
print("7. CREDOSTANFORD2015 — Finding exact 72 and 180 day figures")
print("="*70)
text = get_text("credostanford2015")
# Find all instances of numbers near "days"
pattern = r'\d+\s*days'
matches = re.findall(pattern, text.lower())
print(f"  All 'N days' patterns: {sorted(set(matches))}")

# Find context around key numbers
for term in ["72", "180"]:
    hits = show_all(text, term, 300, 5)
    relevant = [h for h in hits if "day" in h.lower() or "learn" in h.lower() or "math" in h.lower() or "reading" in h.lower()]
    if relevant:
        print(f"\n  '{term}' with learning/days context:")
        for h in relevant[:2]:
            print(f"    ...{h}...")
