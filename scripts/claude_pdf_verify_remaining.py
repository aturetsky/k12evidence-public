#!/usr/bin/env python3
"""
Verify the remaining 8 papers that failed due to credit exhaustion or token limits.
Uses aggressive page trimming for oversized papers to stay under 200K tokens.
"""

import anthropic
import base64
import os
import time
import fitz
import io
from pathlib import Path

LIBDIR = Path("/home/ubuntu/k12-education-research/literature/papers/consolidated")
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OUTPUT_DIR = Path("/home/ubuntu/k12-education-research")

REMAINING_TASKS = [
    {
        "name": "single_jackson2016_trimmed",
        "key": "jackson2016",
        "max_pages": 50,  # Trim to 50pp to stay under token limit
        "claims": """Verify this specific claim from the K-12 education literature review.
The PDF provided is the first 50 pages of Jackson, Johnson & Persico (2016), "The Effects of School Spending on Educational and Economic Outcomes", QJE.

CLAIM (jackson2016):
"A 10% increase in per-pupil spending throughout school years leads to 7% higher adult wages, 3.2 percentage points higher probability of graduating high school, and significantly lower adult poverty rates; effects are approximately 1.9 times larger for students from low-income families"

→ Find the main results table. Verify:
1. Is 7% the correct wage effect for a 10% spending increase?
2. Is 3.2pp the correct high school graduation effect (the NBER WP reported 3.7pp)?
3. Is the 1.9× multiplier for low-income students accurate?
4. What does the paper say about poverty rates?"""
    },
    {
        "name": "single_lafortune2018_trimmed",
        "key": "lafortune2018",
        "max_pages": 50,
        "claims": """Verify this specific claim from the K-12 education literature review.
The PDF provided is the first 50 pages of Lafortune, Rothstein & Schanzenbach (2018), "School Finance Reform and the Distribution of Student Achievement", AEJ: Applied.

CLAIM (lafortune2018):
"Post-1990 school finance reforms increased per-pupil spending in low-income districts by approximately $1,100 per year and raised test scores in those districts by approximately 0.10 standard deviations"

→ Find the main results. Are $1,100 and 0.10 SD the correct figures?"""
    },
    {
        "name": "single_credostanford2015_trimmed",
        "key": "credostanford2015",
        "max_pages": 50,
        "claims": """Verify this specific claim from the K-12 education literature review.
The PDF provided is the first 50 pages of CREDO (2015), "Online Charter School Study", Stanford University.

CLAIM (credostanford2015):
"Students in online charter schools lose approximately 180 days of learning in math and 72 days in reading compared to traditional public school students"

→ Find the days-of-learning figures. Verify which subject (math or reading) has the larger loss and the exact figures."""
    },
    {
        "name": "single_nickow2020_trimmed",
        "key": "nickow2020",
        "max_pages": 50,
        "claims": """Verify this specific claim from the K-12 education literature review.
The PDF provided is the first 50 pages of Nickow, Oreopoulos & Quan (2020), "The Impressive Effects of Tutoring on PreK-12 Learning", NBER Working Paper.

CLAIM (nickow2020):
"A meta-analysis of 96 tutoring studies finds average effect sizes of d=0.37 across all tutoring types, with high-dosage in-school tutoring producing effects of d=0.49"

→ Find the exact effect sizes and number of studies. Are d=0.37, d=0.49, and 96 studies the correct figures?"""
    },
    {
        "name": "single_sisk2018",
        "key": "sisk2018",
        "max_pages": 90,
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM (sisk2018 — Sisk et al. 2018, "To What Extent and Under Which Circumstances Are Growth Mind-Sets Important?", Psychological Science):
"Growth mindset interventions produce average effect sizes of d=0.08 on academic achievement in experimental studies, with larger effects for at-risk students"

→ Find the exact effect size for interventions. Is d=0.08 correct? What does the paper say about at-risk students specifically?"""
    },
    {
        "name": "single_reardon2011",
        "key": "reardon2011",
        "max_pages": 90,
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM (reardon2011 — Reardon 2011, "The Widening Academic Achievement Gap Between the Rich and the Poor"):
"The income-achievement gap is approximately 30–40% larger among children born in 2001 than among those born 25 years earlier"

→ Find the exact percentage. Is 30–40% the correct range? What is the exact figure reported?"""
    },
    {
        "name": "single_alexander2007",
        "key": "alexander2007",
        "max_pages": 90,
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM (alexander2007 — Alexander, Entwisle & Olson 2007, "Lasting Consequences of the Summer Learning Gap", American Sociological Review):
"Two-thirds of the 9th-grade reading achievement gap between high- and low-income students can be attributed to differential summer learning loss during elementary school"

→ Find the exact proportion. Is two-thirds correct? What specific figure does the paper report?"""
    },
    {
        "name": "single_mourshed2010_trimmed",
        "key": "mourshed2010",
        "max_pages": 50,
        "claims": """Verify this specific claim from the K-12 education literature review.
The PDF provided is the first 50 pages of McKinsey & Company (2010), "How the World's Most Improved School Systems Keep Getting Better".

CLAIM (mourshed2010):
"The most improved school systems share common features: strong teacher recruitment and training, data-driven instruction, and sustained political commitment"

→ Is this an accurate summary of the report's main findings? What are the specific features the report identifies as common to improved systems?"""
    },
]


def load_pdf_trimmed(key: str, max_pages: int) -> tuple[str, int]:
    pdf_path = LIBDIR / f"{key}.pdf"
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    src = fitz.open(pdf_path)
    total_pages = len(src)
    pages_to_use = min(total_pages, max_pages)
    
    if pages_to_use < total_pages:
        out = fitz.open()
        out.insert_pdf(src, from_page=0, to_page=pages_to_use - 1)
        buf = io.BytesIO()
        out.save(buf)
        buf.seek(0)
        data = buf.read()
        src.close()
        out.close()
        print(f"    (using {pages_to_use} of {total_pages} pages)")
    else:
        src.close()
        with open(pdf_path, "rb") as f:
            data = f.read()
    
    return base64.standard_b64encode(data).decode("utf-8"), pages_to_use


def run_task(client, task: dict) -> str:
    name = task["name"]
    key = task["key"]
    max_pages = task.get("max_pages", 90)
    claims = task["claims"]
    
    print(f"\n{'='*50}")
    print(f"Running: {name}")
    
    try:
        pdf_b64, pages = load_pdf_trimmed(key, max_pages)
        print(f"  Loaded {key}.pdf ({pages}pp)")
    except FileNotFoundError as e:
        print(f"  SKIP: {e}")
        return f"SKIPPED: {e}"
    
    content = [
        {
            "type": "document",
            "source": {
                "type": "base64",
                "media_type": "application/pdf",
                "data": pdf_b64,
            },
            "title": f"[{key}]",
            "citations": {"enabled": True}
        },
        {"type": "text", "text": claims}
    ]
    
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[{"role": "user", "content": content}]
    )
    
    result = response.content[0].text
    print(f"  Done. ({response.usage.input_tokens} in, {response.usage.output_tokens} out tokens)")
    
    out_path = OUTPUT_DIR / f"claude_pdf_{name}.md"
    with open(out_path, "w") as f:
        f.write(f"# Claude PDF Verification: {name}\n\n")
        f.write(f"Model: {response.model} | In: {response.usage.input_tokens} | Out: {response.usage.output_tokens}\n\n---\n\n")
        f.write(result)
    
    return result


def main():
    client = anthropic.Anthropic(api_key=API_KEY)
    
    all_results = {}
    failed = []
    
    for task in REMAINING_TASKS:
        try:
            result = run_task(client, task)
            all_results[task["name"]] = result
            time.sleep(1)
        except Exception as e:
            print(f"  ERROR in {task['name']}: {e}")
            failed.append((task["name"], str(e)))
            time.sleep(3)
    
    # Append to consolidated report
    consolidated_path = OUTPUT_DIR / "claude_pdf_review_all_batches.md"
    with open(consolidated_path, "a") as f:
        f.write("\n\n# Remaining Papers Verification\n\n")
        for name, result in all_results.items():
            f.write(f"## {name}\n\n{result}\n\n---\n\n")
        if failed:
            f.write("## Failed\n\n")
            for name, err in failed:
                f.write(f"- **{name}**: {err}\n")
    
    print(f"\n{'='*50}")
    print(f"COMPLETE. Successful: {len(all_results)}/{len(REMAINING_TASKS)}")
    if failed:
        print(f"Failed: {[n for n, _ in failed]}")


if __name__ == "__main__":
    if not API_KEY:
        print("ERROR: ANTHROPIC_API_KEY not set")
        exit(1)
    main()
