#!/usr/bin/env python3
"""
Claude API verification pass - Batch 1 (Clusters 1 & 2)
Uses Anthropic API with PDF document blocks for direct PDF reading.
"""

import anthropic
import base64
import os
from pathlib import Path

LIBDIR = Path("/home/ubuntu/k12-education-research/literature/papers/consolidated")
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

BATCH1_PDFS = {
    "rivkin2005": "Rivkin, Hanushek & Kain (2005) - Teachers, Schools, and Academic Achievement",
    "rockoff2004": "Rockoff (2004) - The Impact of Individual Teachers on Student Achievement",
    "nye2004": "Nye, Konstantopoulos & Hedges (2004) - How Large Are Teacher Effects?",
    "chetty2014a": "Chetty, Friedman & Rockoff (2014a) - Measuring the Impacts of Teachers I",
    "chetty2014b": "Chetty, Friedman & Rockoff (2014b) - Measuring the Impacts of Teachers II",
    "rothstein2010": "Rothstein (2010) - Teacher Quality in Educational Production",
    "goldhaber2015": "Goldhaber & Chaplin (2015) - Assessing the Rothstein Falsification Test",
    "jackson2018b": "Jackson (2018) - What Do Test Scores Miss? Non-cognitive Teacher Effects",
    "heckman2010": "Heckman et al. (2010) - The Rate of Return to the HighScope Perry Preschool Program",
    "heckman2006": "Heckman (2006) - Skill Formation and the Economics of Investing in Disadvantaged Children",
    "campbell2014": "Campbell et al. (2014) - Early Childhood Investments Substantially Boost Adult Health",
    "puma2010_excerpt": "Puma et al. (2010) - Head Start Impact Study Final Report (Executive Summary + Key Findings, pp.1-40)",
    "lipsey2018": "Lipsey et al. (2018) - Effects of the Tennessee Voluntary Prekindergarten Program",
}

CLAIMS_PROMPT = """You are conducting an independent verification pass on a K-12 education systematic literature review. I have provided the source PDFs for Clusters 1 (Teacher Quality & VAMs) and 2 (Early Childhood Education). Please read each PDF carefully and verify the following specific claims made in the manuscript.

For each claim, state:
1. CONFIRMED, INCORRECT, or UNVERIFIABLE
2. The exact text or data you found in the PDF supporting or contradicting the claim
3. The page number where you found it
4. Any corrections needed, with the precise corrected text

**Cluster 1 — Teacher Quality & VAMs**

CLAIM 1.1 (rivkin2005): "A one standard deviation improvement in teacher quality raises student achievement by approximately 0.10–0.20 standard deviations per year"

CLAIM 1.2 (rockoff2004): "A one standard deviation increase in teacher quality raises math and reading scores by approximately 0.10 standard deviations"

CLAIM 1.3 (nye2004): "The interquartile range of teacher effects spans 0.34–0.48 standard deviations" and that this represents an upper bound relative to other studies in the literature

CLAIM 1.4 (chetty2014a): "A one standard deviation increase in VAM is associated with a 0.54% increase in earnings at age 28, based on a sample of more than one million students"

CLAIM 1.5 (chetty2014b): "Replacing a teacher in the bottom 5% of the VAM distribution with an average teacher raises the lifetime earnings of a classroom of students by approximately $250,000 per year of teaching"

CLAIM 1.6 (rothstein2010): "Pre-trends in student achievement predict future teacher assignments, suggesting VAMs capture selection effects rather than true causal impacts" — and that this finding is contested by Chetty et al. and Goldhaber & Chaplin

CLAIM 1.7 (goldhaber2015): "Rothstein's falsification test produces false positives even when VAMs are unbiased, and the bias in VAMs is approximately 3%"

CLAIM 1.8 (jackson2018b): "Teacher effects on non-cognitive outcomes (high school graduation and college-going) are largely uncorrelated (r ≈ 0.15–0.30) with teacher effects on test scores"

**Cluster 2 — Early Childhood Education**

CLAIM 2.1 (heckman2010): "The Perry Preschool Program, a randomized trial with n=58 deeply disadvantaged children, produced a 7–12% annual return on investment through age 40"

CLAIM 2.2 (heckman2006): "Non-cognitive skills are highly malleable in early childhood and are strong predictors of adult success"

CLAIM 2.3 (campbell2014): "The Abecedarian Project produced significant improvements in adult health outcomes in a randomized trial"

CLAIM 2.4 (puma2010): "Head Start produces significant short-term cognitive gains that largely fade out by the end of first grade"

CLAIM 2.5 (lipsey2018): "Tennessee's Voluntary Pre-K program produced significant short-term gains that faded out by kindergarten entry"

Please be thorough and precise. Cite page numbers. If a claim is approximately correct but uses imprecise language, note the more precise formulation."""


def load_pdf_as_base64(key: str) -> str:
    # Handle excerpt files
    actual_key = key
    pdf_path = LIBDIR / f"{actual_key}.pdf"
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    with open(pdf_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def run_batch1_verification():
    client = anthropic.Anthropic(api_key=API_KEY)
    
    print("Loading PDFs as base64...")
    content = []
    
    for key, description in BATCH1_PDFS.items():
        print(f"  Loading {key}.pdf ({description[:50]}...)")
        try:
            pdf_b64 = load_pdf_as_base64(key)
            content.append({
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": pdf_b64,
                },
                "title": f"{key}: {description}",
                "citations": {"enabled": True}
            })
        except FileNotFoundError as e:
            print(f"  WARNING: {e}")
    
    # Add the claims prompt as the final text block
    content.append({
        "type": "text",
        "text": CLAIMS_PROMPT
    })
    
    print(f"\nSending {len(content)-1} PDFs to Claude claude-opus-4-5 for verification...")
    print("This may take several minutes...\n")
    
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=8192,
        messages=[
            {
                "role": "user",
                "content": content
            }
        ]
    )
    
    result = response.content[0].text
    
    # Save the response
    output_path = Path("/home/ubuntu/k12-education-research/claude_pdf_review_batch1.md")
    with open(output_path, "w") as f:
        f.write("# Claude PDF-Grounded Verification — Batch 1 (Clusters 1 & 2)\n\n")
        f.write(f"Model: {response.model}\n")
        f.write(f"Input tokens: {response.usage.input_tokens}\n")
        f.write(f"Output tokens: {response.usage.output_tokens}\n\n")
        f.write("---\n\n")
        f.write(result)
    
    print(f"Response saved to: {output_path}")
    print(f"\n{'='*60}")
    print("CLAUDE'S RESPONSE:")
    print('='*60)
    print(result[:3000])
    if len(result) > 3000:
        print(f"\n... [truncated, full response saved to file] ...")
    
    return result


if __name__ == "__main__":
    if not API_KEY:
        print("ERROR: ANTHROPIC_API_KEY not set")
        exit(1)
    run_batch1_verification()
