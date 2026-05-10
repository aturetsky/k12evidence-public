#!/usr/bin/env python3
"""Deep read of cook2015, nye2004, angrist2013 to find exact effect sizes."""

import fitz
import re
from pathlib import Path

CONSOLIDATED = Path("/home/ubuntu/k12-education-research/literature/papers/consolidated")

def find_all_contexts(text, term, context=300):
    """Find all occurrences of a term with surrounding context."""
    results = []
    text_lower = text.lower()
    term_lower = term.lower()
    start = 0
    while True:
        idx = text_lower.find(term_lower, start)
        if idx < 0:
            break
        s = max(0, idx - context//2)
        e = min(len(text), idx + len(term) + context//2)
        snippet = text[s:e].replace('\n', ' ').strip()
        results.append(snippet)
        start = idx + 1
    return results

print("="*70)
print("COOK 2015 - Looking for actual effect size on math/course failure")
print("="*70)
doc = fitz.open(str(CONSOLIDATED / "cook2015.pdf"))
text = "".join(page.get_text() for page in doc)
doc.close()

# Look for standard deviation / effect size language
for term in ["standard deviation", "effect size", "0.65", "0.66", "0.67", "0.68", "0.69", "0.70", "0.71", "0.72", "0.73", "0.74", "0.75", "sigma", "SD units"]:
    contexts = find_all_contexts(text, term, 250)
    if contexts:
        print(f"\n  '{term}' found {len(contexts)} times:")
        for ctx in contexts[:2]:
            print(f"    ...{ctx}...")
        break

# Also look for the main results table
for term in ["math GPA", "math grade", "course failure", "math score", "test score", "achievement"]:
    contexts = find_all_contexts(text, term, 200)
    if contexts:
        print(f"\n  '{term}' ({len(contexts)} occurrences):")
        for ctx in contexts[:1]:
            print(f"    ...{ctx}...")

print("\n\n" + "="*70)
print("NYE 2004 - Looking for 75th/25th percentile teacher gap d=0.34-0.48")
print("="*70)
doc = fitz.open(str(CONSOLIDATED / "nye2004.pdf"))
text = "".join(page.get_text() for page in doc)
doc.close()

# Look for the key claim about teacher quality gap
for term in ["75th", "25th", "percentile", "quartile", "difference between", "gap between", "effective teacher", "ineffective"]:
    contexts = find_all_contexts(text, term, 250)
    if contexts:
        print(f"\n  '{term}' found {len(contexts)} times:")
        for ctx in contexts[:2]:
            print(f"    ...{ctx}...")

# Find all effect sizes in the paper
all_decimals = re.findall(r'\b0\.[3-5]\d\b', text)
unique = sorted(set(all_decimals))
print(f"\n  Effect sizes in range 0.30-0.59: {unique}")

# Look for the main results
for term in ["teacher effect", "teacher variance", "between-teacher", "sigma_t", "sigma_u"]:
    contexts = find_all_contexts(text, term, 200)
    if contexts:
        print(f"\n  '{term}':")
        for ctx in contexts[:1]:
            print(f"    ...{ctx}...")

print("\n\n" + "="*70)
print("ANGRIST 2013 - Looking for d=0.40 per year Boston charters")
print("="*70)
doc = fitz.open(str(CONSOLIDATED / "angrist2013.pdf"))
text = "".join(page.get_text() for page in doc)
doc.close()

# Look for the effect size
for term in ["0.40", "0.4 ", "standard deviation", "effect", "math score", "per year", "annual gain", "lottery"]:
    contexts = find_all_contexts(text, term, 250)
    if contexts:
        print(f"\n  '{term}' found {len(contexts)} times:")
        for ctx in contexts[:2]:
            print(f"    ...{ctx}...")
        if term in ["0.40", "0.4 "]:
            break

# Find all effect sizes
all_decimals = re.findall(r'\b0\.[3-5]\d\b', text)
unique = sorted(set(all_decimals))
print(f"\n  Effect sizes in range 0.30-0.59: {unique}")

print("\n\n" + "="*70)
print("ALSO: ABDULKADIROLU 2018 - Checking d=-0.40 Louisiana vouchers")
print("="*70)
doc = fitz.open(str(CONSOLIDATED / "abdulkadirolu2018.pdf"))
text = "".join(page.get_text() for page in doc)
doc.close()

for term in ["-0.4", "−0.4", "0.4 standard", "math", "Louisiana", "voucher", "negative effect"]:
    contexts = find_all_contexts(text, term, 250)
    if contexts:
        print(f"\n  '{term}' found {len(contexts)} times:")
        for ctx in contexts[:1]:
            print(f"    ...{ctx}...")
        if "-0.4" in term or "−0.4" in term:
            break

all_decimals = re.findall(r'-?0\.[3-5]\d\b', text)
unique = sorted(set(all_decimals))
print(f"\n  Effect sizes in range -0.59 to -0.30 or 0.30-0.59: {unique}")

print("\n\n" + "="*70)
print("ALSO: CREDOSTANFORD2015 - Checking 72 days math, 180 days reading")
print("="*70)
doc = fitz.open(str(CONSOLIDATED / "credostanford2015.pdf"))
text = "".join(page.get_text() for page in doc)
doc.close()
print(f"  PDF has {len(text)} chars (if 0, it's a scanned image PDF)")
if len(text) < 100:
    print("  CONFIRMED: Scanned image PDF - cannot extract text")
    print("  Will need to note this as unverifiable from PDF")
else:
    for term in ["72", "180", "days", "virtual"]:
        contexts = find_all_contexts(text, term, 200)
        if contexts:
            print(f"\n  '{term}':")
            for ctx in contexts[:1]:
                print(f"    ...{ctx}...")
