#!/usr/bin/env python3
"""
Claude API independent verification pass.
Sends the full manuscript to Claude with the verification report and asks for:
1. Independent check of all quantitative claims
2. Editorial review of how papers are characterized
3. Identification of any remaining errors or misattributions
4. Structural and logical critique of the lit review
"""

import os
import anthropic
from pathlib import Path

REPO_DIR = Path("/home/ubuntu/k12-education-research")
DRAFTS_DIR = REPO_DIR / "drafts"
REPO_URL = "https://github.com/aturetsky/k12-education-research"

# Read the manuscript
manuscript_path = DRAFTS_DIR / "literature_review_complete.tex"
with open(manuscript_path) as f:
    manuscript = f.read()

# Read the verification report
report_path = REPO_DIR / "verification_report_final.md"
with open(report_path) as f:
    verification_report = f.read()

# Read the BibTeX
bib_path = DRAFTS_DIR / "k12_references.bib"
with open(bib_path) as f:
    bibtex = f.read()

print("Files loaded:")
print(f"  Manuscript: {len(manuscript):,} chars")
print(f"  Verification report: {len(verification_report):,} chars")
print(f"  BibTeX: {len(bibtex):,} chars")

# Initialize Claude client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert academic reviewer specializing in K-12 education research, causal inference methodology, and evidence synthesis. You have deep knowledge of the empirical literature on teacher quality, early childhood education, class size, school finance, charter schools, reading instruction, tutoring, social-emotional learning, and educational inequality.

Your task is to conduct a rigorous independent verification and editorial review of a systematic literature review manuscript. You have access to:
1. The full LaTeX manuscript
2. A prior automated verification report (which confirmed 45/45 claims via text search)
3. The full BibTeX reference list

Your review should be INDEPENDENT — do not simply validate the prior verification report. Look for:
- Quantitative claims that are imprecise, overstated, or misattributed
- Papers that are mischaracterized or whose findings are presented out of context
- Internal inconsistencies within the manuscript
- Claims that are technically true but misleading without important caveats
- Missing important caveats (e.g., effect sizes that are statistically significant but not practically meaningful)
- Any remaining phantom citations or papers that don't match their described findings
- Structural or logical issues in how the evidence is synthesized
- Places where the review inadvertently takes a policy position rather than neutrally synthesizing evidence

Be specific: cite line numbers or section names when flagging issues. Distinguish between:
- CRITICAL: factual errors that must be corrected
- IMPORTANT: imprecisions or missing caveats that should be addressed
- MINOR: stylistic or framing suggestions

The repository is at: """ + REPO_URL

USER_PROMPT = f"""Please conduct a thorough independent verification and editorial review of this K-12 education literature review manuscript.

## MANUSCRIPT (LaTeX source)

```latex
{manuscript}
```

## PRIOR AUTOMATED VERIFICATION REPORT

```markdown
{verification_report[:3000]}
```

## BIBTEX REFERENCE LIST (first 3000 chars)

```bibtex
{bibtex[:3000]}
```

Please provide:

1. **CRITICAL ERRORS** — Any factual errors, wrong effect sizes, misattributed findings, or phantom citations that must be corrected before publication

2. **IMPORTANT ISSUES** — Imprecisions, missing caveats, or misleading characterizations that should be addressed

3. **SPECIFIC CLAIM CHECKS** — For each of these specific claims, tell me whether the characterization is accurate, imprecise, or wrong:
   - Nye (2004): "gap between 75th and 25th percentile teacher is over one third of a standard deviation in reading and almost half a standard deviation in math"
   - Heckman (2010): "7–12% annual return on investment" for Perry Preschool
   - Cook (2015): Chicago tutoring program effect on math
   - Angrist (2013): Boston charter schools "approximately d=0.40 in ELA and nearly d=0.60 in math per year of attendance"
   - CREDO (2015): "180 days of learning in math and 72 days in reading"
   - Sims (2023): "52 percent" exaggeration of effect sizes in promising trials

4. **POLICY NEUTRALITY CHECK** — Does the manuscript maintain appropriate neutrality for a systematic literature review, or does it inadvertently advocate for particular policy positions?

5. **STRUCTURAL CRITIQUE** — Any major structural or logical issues in how the evidence is organized and synthesized

6. **MINOR SUGGESTIONS** — Any smaller improvements to clarity, precision, or framing

Please be specific and cite section names or approximate line numbers where relevant."""

print("\nSending to Claude API...")
print("(This may take 60-90 seconds for a full manuscript review)\n")

try:
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": USER_PROMPT}
        ]
    )
    
    review_text = response.content[0].text
    
    print(f"Claude response received: {len(review_text):,} chars")
    print(f"Input tokens: {response.usage.input_tokens:,}")
    print(f"Output tokens: {response.usage.output_tokens:,}")
    
    # Save the review
    output_path = REPO_DIR / "drafts" / "claude_verification_v3.md"
    with open(output_path, 'w') as f:
        f.write("# Claude Independent Verification Pass — v3\n\n")
        f.write(f"**Date:** May 08, 2026\n")
        f.write(f"**Model:** claude-opus-4-5\n")
        f.write(f"**Input tokens:** {response.usage.input_tokens:,}\n")
        f.write(f"**Output tokens:** {response.usage.output_tokens:,}\n\n")
        f.write("---\n\n")
        f.write(review_text)
    
    print(f"\nReview saved to: {output_path}")
    print("\n" + "="*70)
    print("CLAUDE REVIEW SUMMARY (first 3000 chars):")
    print("="*70)
    print(review_text[:3000])
    
except anthropic.APIError as e:
    print(f"API Error: {e}")
    # Try with claude-3-5-sonnet as fallback
    print("Trying claude-3-5-sonnet-20241022 as fallback...")
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": USER_PROMPT}
        ]
    )
    review_text = response.content[0].text
    output_path = REPO_DIR / "drafts" / "claude_verification_v3.md"
    with open(output_path, 'w') as f:
        f.write("# Claude Independent Verification Pass — v3\n\n")
        f.write(f"**Date:** May 08, 2026\n")
        f.write(f"**Model:** claude-3-5-sonnet-20241022 (fallback)\n\n")
        f.write("---\n\n")
        f.write(review_text)
    print(f"Saved to {output_path}")
    print(review_text[:3000])
