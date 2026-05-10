#!/usr/bin/env python3
"""Deep-dive manual check on the 4 not-found claims and 5 no-PDF claims."""

import fitz
from pathlib import Path

CONSOLIDATED = Path("/home/ubuntu/k12-education-research/literature/papers/consolidated")

def extract_text(key):
    pdf_path = CONSOLIDATED / f"{key}.pdf"
    if not pdf_path.exists():
        print(f"  [NO PDF] {key}.pdf not found")
        return ""
    doc = fitz.open(str(pdf_path))
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    print(f"  [OK] {key}.pdf extracted ({len(text)} chars, {len(doc)} pages... wait, doc closed)")
    return text

def search_and_show(text, terms, context=300):
    text_lower = text.lower()
    for term in terms:
        idx = text_lower.find(term.lower())
        if idx >= 0:
            start = max(0, idx - context//2)
            end = min(len(text), idx + len(term) + context//2)
            snippet = text[start:end].replace('\n', ' ').strip()
            print(f"    FOUND '{term}': ...{snippet}...")
            return True
    print(f"    NOT FOUND: {terms}")
    return False

print("="*70)
print("DEEP CHECK 1: nye2004 - Teacher quality gap d=0.34-0.48")
print("="*70)
doc = fitz.open(str(CONSOLIDATED / "nye2004.pdf"))
text = "".join(page.get_text() for page in doc)
doc.close()
print(f"PDF has {len(text)} chars")
# Look for the actual numbers in the paper
for term in ["0.34", "0.35", "0.36", "0.37", "0.38", "0.39", "0.40", "0.41", "0.42", "0.43", "0.44", "0.45", "0.46", "0.47", "0.48", "75th", "25th", "percentile", "quartile", "effect size", "standard deviation"]:
    idx = text.lower().find(term.lower())
    if idx >= 0:
        start = max(0, idx-100)
        end = min(len(text), idx+len(term)+100)
        snippet = text[start:end].replace('\n', ' ').strip()
        print(f"  FOUND '{term}': ...{snippet}...")
        break
# Show first 1000 chars to understand paper structure
print("\nFirst 500 chars of nye2004:")
print(text[:500].replace('\n', ' '))
print("\nLooking for any decimal numbers in paper:")
import re
decimals = re.findall(r'\b0\.\d{2,3}\b', text)
unique_decimals = sorted(set(decimals))
print(f"All decimal values found: {unique_decimals[:30]}")

print("\n" + "="*70)
print("DEEP CHECK 2: may2023 - Reading Recovery 4th grade lower than control")
print("="*70)
doc = fitz.open(str(CONSOLIDATED / "may2023.pdf"))
text = "".join(page.get_text() for page in doc)
doc.close()
print(f"PDF has {len(text)} chars")
for term in ["fourth", "4th", "lower", "control", "grade 4", "Reading Recovery", "fadeout", "fade", "negative", "worse"]:
    idx = text.lower().find(term.lower())
    if idx >= 0:
        start = max(0, idx-150)
        end = min(len(text), idx+len(term)+150)
        snippet = text[start:end].replace('\n', ' ').strip()
        print(f"  FOUND '{term}': ...{snippet}...")
        break
print("\nFirst 500 chars of may2023:")
print(text[:500].replace('\n', ' '))

print("\n" + "="*70)
print("DEEP CHECK 3: cook2015 - Chicago tutoring d=0.65")
print("="*70)
doc = fitz.open(str(CONSOLIDATED / "cook2015.pdf"))
text = "".join(page.get_text() for page in doc)
doc.close()
print(f"PDF has {len(text)} chars")
for term in ["0.65", "0.6", "Chicago", "math", "tutoring", "course failure", "high school", "male"]:
    idx = text.lower().find(term.lower())
    if idx >= 0:
        start = max(0, idx-150)
        end = min(len(text), idx+len(term)+150)
        snippet = text[start:end].replace('\n', ' ').strip()
        print(f"  FOUND '{term}': ...{snippet}...")
        break
print("\nFirst 500 chars of cook2015:")
print(text[:500].replace('\n', ' '))
decimals = re.findall(r'\b0\.\d{2,3}\b', text)
unique_decimals = sorted(set(decimals))
print(f"All decimal values found: {unique_decimals[:30]}")

print("\n" + "="*70)
print("DEEP CHECK 4: kraft2021 - During-school tutoring more effective")
print("="*70)
doc = fitz.open(str(CONSOLIDATED / "kraft2021.pdf"))
text = "".join(page.get_text() for page in doc)
doc.close()
print(f"PDF has {len(text)} chars")
for term in ["during school", "after school", "school day", "attendance", "paraprofessional", "tutor", "dosage", "in-school"]:
    idx = text.lower().find(term.lower())
    if idx >= 0:
        start = max(0, idx-150)
        end = min(len(text), idx+len(term)+150)
        snippet = text[start:end].replace('\n', ' ').strip()
        print(f"  FOUND '{term}': ...{snippet}...")
        break
print("\nFirst 500 chars of kraft2021:")
print(text[:500].replace('\n', ' '))

print("\n" + "="*70)
print("ALSO CHECKING: jackson2016 exact figures (7.25% wages, 3.67pp poverty)")
print("="*70)
doc = fitz.open(str(CONSOLIDATED / "jackson2016.pdf"))
text = "".join(page.get_text() for page in doc)
doc.close()
for term in ["7.25", "3.67", "7 percent", "3.7 percent", "7%", "wages"]:
    idx = text.lower().find(term.lower())
    if idx >= 0:
        start = max(0, idx-200)
        end = min(len(text), idx+len(term)+200)
        snippet = text[start:end].replace('\n', ' ').strip()
        print(f"  FOUND '{term}': ...{snippet}...")
        break

print("\n" + "="*70)
print("ALSO CHECKING: abdulkadirolu2018 exact d=-0.40 figure")
print("="*70)
doc = fitz.open(str(CONSOLIDATED / "abdulkadirolu2018.pdf"))
text = "".join(page.get_text() for page in doc)
doc.close()
for term in ["-0.4", "−0.4", "0.4", "Louisiana", "math", "decline", "negative"]:
    idx = text.lower().find(term.lower())
    if idx >= 0:
        start = max(0, idx-200)
        end = min(len(text), idx+len(term)+200)
        snippet = text[start:end].replace('\n', ' ').strip()
        print(f"  FOUND '{term}': ...{snippet}...")
        break

print("\n" + "="*70)
print("ALSO CHECKING: angrist2013 exact d=0.40 per year Boston charters")
print("="*70)
doc = fitz.open(str(CONSOLIDATED / "angrist2013.pdf"))
text = "".join(page.get_text() for page in doc)
doc.close()
for term in ["0.40", "0.4 ", "Boston", "charter", "math", "per year", "annual"]:
    idx = text.lower().find(term.lower())
    if idx >= 0:
        start = max(0, idx-200)
        end = min(len(text), idx+len(term)+200)
        snippet = text[start:end].replace('\n', ' ').strip()
        print(f"  FOUND '{term}': ...{snippet}...")
        break

print("\n" + "="*70)
print("ALSO CHECKING: credostanford2015 72 days math, 180 days reading")
print("="*70)
doc = fitz.open(str(CONSOLIDATED / "credostanford2015.pdf"))
text = "".join(page.get_text() for page in doc)
doc.close()
for term in ["72", "180", "days", "virtual", "learning"]:
    idx = text.lower().find(term.lower())
    if idx >= 0:
        start = max(0, idx-200)
        end = min(len(text), idx+len(term)+200)
        snippet = text[start:end].replace('\n', ' ').strip()
        print(f"  FOUND '{term}': ...{snippet}...")
        break

print("\n" + "="*70)
print("ALSO CHECKING: reardon2011 exact 30-40% larger figure")
print("="*70)
doc = fitz.open(str(CONSOLIDATED / "reardon2011.pdf"))
text = "".join(page.get_text() for page in doc)
doc.close()
for term in ["30 to 40", "30-40", "40 percent", "30 percent", "larger", "income", "achievement gap", "2001"]:
    idx = text.lower().find(term.lower())
    if idx >= 0:
        start = max(0, idx-200)
        end = min(len(text), idx+len(term)+200)
        snippet = text[start:end].replace('\n', ' ').strip()
        print(f"  FOUND '{term}': ...{snippet}...")
        break
