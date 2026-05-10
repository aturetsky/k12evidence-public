#!/usr/bin/env python3
"""
Claude API verification pass — chunked by cluster.
Sends one section at a time to avoid timeout/context issues.
"""

import os
import time
import anthropic
from pathlib import Path

REPO_DIR = Path("/home/ubuntu/k12-education-research")
DRAFTS_DIR = REPO_DIR / "drafts"

# Read the manuscript
with open(DRAFTS_DIR / "literature_review_complete.tex") as f:
    manuscript = f.read()

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

SYSTEM = """You are an expert academic reviewer specializing in K-12 education research and causal inference. 
You are conducting an independent verification of a systematic literature review.
Be specific, cite section names, and distinguish CRITICAL errors from IMPORTANT issues from MINOR suggestions.
Focus on: accuracy of effect sizes, correct attribution of findings, missing caveats, and policy neutrality."""

# Define the clusters/sections to review
sections = [
    {
        "name": "Methodological Framework + Teacher Quality (Clusters 1-2)",
        "lines": (69, 165),
        "key_claims": [
            "Rivkin et al. (2005): SD of teacher effects ~0.10-0.15",
            "Rockoff (2004): SD of teacher effects ~0.10",
            "Nye et al. (2004): 75th vs 25th percentile teacher gap = 0.35 reading, ~0.48 math",
            "Chetty et al. (2014a): VAM unbiased, 2.5M students",
            "Chetty et al. (2014b): replacing bottom-5% teacher = $250,000 lifetime earnings per classroom",
            "Rothstein (2010): VAMs fail falsification tests",
        ]
    },
    {
        "name": "Early Childhood + Class Size (Clusters 3-4)",
        "lines": (166, 255),
        "key_claims": [
            "Heckman (2010): Perry Preschool 7-12% annual ROI, effects to age 40",
            "Campbell et al. (2014): Abecedarian - lower hypertension/diabetes at age 35",
            "Puma et al. (2010): Head Start gains fade by 3rd grade",
            "Lipsey et al. (2018): Tennessee Pre-K - by 3rd grade, pre-K scored lower than control",
            "Krueger (1999): STAR - d=0.22 reading, d=0.27 math in kindergarten",
            "Fredriksson et al. (2013): one fewer student → ~3% higher adult earnings",
            "Jepsen & Rivkin (2009): California CSR - near-zero net benefits for disadvantaged",
        ]
    },
    {
        "name": "School Finance + School Choice (Clusters 5-6)",
        "lines": (256, 360),
        "key_claims": [
            "Jackson et al. (2016): 10% spending increase → 7.25% higher wages, 3.67pp poverty reduction",
            "Angrist et al. (2013): Boston charters - d=0.40 ELA, ~0.60 math per year at high school level",
            "CREDO (2015): virtual charters - 180 days lost in math, 72 days lost in reading",
            "Abdulkadiroğlu et al. (2018): Louisiana vouchers - math scores down 0.40 SD",
        ]
    },
    {
        "name": "Literacy + Tutoring + SEL (Clusters 7-9)",
        "lines": (361, 450),
        "key_claims": [
            "Ehri et al. (2001): systematic phonics d=0.44",
            "May et al. (2016): Reading Recovery i3 RCT d=0.30-0.42",
            "May et al. (2023): Reading Recovery - by 4th grade, participants scored lower than control",
            "Nickow et al. (2024): tutoring meta-analysis pooled d=0.37",
            "Durlak et al. (2011): SEL meta-analysis 213 programs, d=0.27 academic achievement",
            "Credé et al. (2017): grit redundant with conscientiousness, near-zero incremental validity",
            "Sisk et al. (2018): growth mindset d=0.10 overall",
            "Sims et al. (2023): promising trials bias - 52% exaggeration",
        ]
    },
    {
        "name": "Inequality + International + Policy Synthesis (Clusters 10-12)",
        "lines": (451, 600),
        "key_claims": [
            "Reardon (2011): income-achievement gap 30-40% larger for children born 2001 vs 25 years earlier",
            "Goldhaber et al. (2022): COVID learning loss - 4th grade reading -3 NAEP, 8th grade math -8 NAEP",
            "Policy neutrality: does the review maintain appropriate neutrality?",
            "Cross-cutting synthesis: are the 5 themes accurately derived from the evidence?",
        ]
    },
]

all_reviews = []

for i, section in enumerate(sections):
    print(f"\n{'='*60}")
    print(f"Reviewing section {i+1}/{len(sections)}: {section['name']}")
    print(f"{'='*60}")
    
    # Extract the relevant lines
    lines = manuscript.split('\n')
    start, end = section["lines"]
    section_text = '\n'.join(lines[start-1:end])
    
    claims_list = '\n'.join(f"- {c}" for c in section["key_claims"])
    
    prompt = f"""Review this section of a K-12 education systematic literature review:

**Section:** {section['name']}

**Key claims to verify:**
{claims_list}

**Manuscript text:**
```latex
{section_text}
```

Please provide:
1. **CRITICAL ERRORS** (factual errors requiring correction)
2. **IMPORTANT ISSUES** (imprecisions, missing caveats, misleading framing)
3. **MINOR SUGGESTIONS** (clarity, style)
4. **POLICY NEUTRALITY** (does this section maintain appropriate neutrality for a lit review?)

Be specific about line references and exact claim wording."""

    try:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=3000,
            system=SYSTEM,
            messages=[{"role": "user", "content": prompt}]
        )
        review = response.content[0].text
        print(f"  ✓ Response: {len(review)} chars, {response.usage.output_tokens} output tokens")
        all_reviews.append({
            "section": section["name"],
            "review": review,
            "tokens": response.usage.output_tokens
        })
    except Exception as e:
        print(f"  ✗ Error: {e}")
        # Try claude-3-5-sonnet as fallback
        try:
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=3000,
                system=SYSTEM,
                messages=[{"role": "user", "content": prompt}]
            )
            review = response.content[0].text
            print(f"  ✓ Fallback response: {len(review)} chars")
            all_reviews.append({
                "section": section["name"],
                "review": review,
                "tokens": response.usage.output_tokens,
                "model": "claude-3-5-sonnet-20241022"
            })
        except Exception as e2:
            print(f"  ✗ Fallback also failed: {e2}")
            all_reviews.append({
                "section": section["name"],
                "review": f"ERROR: {e2}",
                "tokens": 0
            })
    
    # Brief pause between requests
    if i < len(sections) - 1:
        time.sleep(3)

# Save combined review
output_path = DRAFTS_DIR / "claude_verification_v3.md"
with open(output_path, 'w') as f:
    f.write("# Claude Independent Verification Pass — v3 (Chunked)\n\n")
    f.write(f"**Date:** May 08, 2026\n")
    f.write(f"**Model:** claude-opus-4-5\n")
    f.write(f"**Sections reviewed:** {len(all_reviews)}\n\n")
    f.write("---\n\n")
    
    for r in all_reviews:
        f.write(f"## {r['section']}\n\n")
        f.write(r['review'])
        f.write("\n\n---\n\n")

print(f"\n\nFull review saved to: {output_path}")
print("\n" + "="*60)
print("SUMMARY OF CRITICAL ERRORS FOUND:")
print("="*60)
for r in all_reviews:
    if "CRITICAL" in r['review'].upper():
        print(f"\n### {r['section']}")
        # Find and print the critical section
        lines = r['review'].split('\n')
        in_critical = False
        for line in lines:
            if 'CRITICAL' in line.upper():
                in_critical = True
            elif line.startswith('##') and in_critical:
                in_critical = False
            if in_critical:
                print(f"  {line}")
