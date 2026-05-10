#!/usr/bin/env python3
"""
Handle skipped/failed batches by sending one paper at a time.
Papers that exceeded 100 pages or 200K tokens.
"""

import anthropic
import base64
import os
import time
import fitz
from pathlib import Path

LIBDIR = Path("/home/ubuntu/k12-education-research/literature/papers/consolidated")
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OUTPUT_DIR = Path("/home/ubuntu/k12-education-research")

SINGLE_PAPER_TASKS = [
    {
        "name": "single_krueger1999",
        "key": "krueger1999",
        "claims": """Verify this specific claim from the K-12 education literature review about the Tennessee STAR experiment:

CLAIM (krueger1999 — Krueger 1999, "Experimental Estimates of Education Production Functions", QJE):
"Students in small classes (13–17 students) in the Tennessee STAR experiment outperformed students in regular classes (22–26 students) by approximately d=0.20–0.27 standard deviations in reading and math"

→ Find the exact effect size range. Are these cumulative effects or per-year effects? What are the figures for reading and math separately? Is d=0.20–0.27 the correct range?"""
    },
    {
        "name": "single_fredriksson2013",
        "key": "fredriksson2013",
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM (fredriksson2013 — Fredriksson, Öckert & Oosterbeek 2013, "Long-Term Effects of Class Size", QJE):
"A one-student reduction in class size raises earnings at age 27–42 by approximately 1.2% and improves cognitive test scores"

→ Find the exact earnings effect. Is 1.2% the correct figure? What age range is covered? What are the test score effects?"""
    },
    {
        "name": "single_angrist1999",
        "key": "angrist1999",
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM (angrist1999 — Angrist & Lavy 1999, "Using Maimonides' Rule to Estimate the Effect of Class Size on Scholastic Achievement", QJE):
"A 10-student reduction in class size raises reading scores by approximately 0.20 standard deviations and math scores by approximately 0.24 standard deviations"

→ Find the exact IV effect size estimates. Are 0.20 and 0.24 the correct figures? Are these per-student or per-10-student effects?"""
    },
    {
        "name": "single_jackson2016",
        "key": "jackson2016",
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM (jackson2016 — Jackson, Johnson & Persico 2016, "The Effects of School Spending on Educational and Economic Outcomes", QJE):
"A 10% increase in per-pupil spending throughout school years leads to 7% higher adult wages, 3.2 percentage points higher probability of graduating high school, and significantly lower adult poverty rates; effects are approximately 1.9 times larger for students from low-income families"

→ Verify each figure precisely:
1. Is 7% the correct wage effect?
2. Is 3.2pp the correct high school graduation effect (vs. 3.7pp in the NBER working paper)?
3. Is the 1.9× multiplier for low-income students accurate?
4. What does the paper say about poverty rates specifically?"""
    },
    {
        "name": "single_lafortune2018",
        "key": "lafortune2018",
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM (lafortune2018 — Lafortune, Rothstein & Schanzenbach 2018, "School Finance Reform and the Distribution of Student Achievement", AEJ: Applied):
"Post-1990 school finance reforms increased per-pupil spending in low-income districts by approximately $1,100 per year and raised test scores in those districts by approximately 0.10 standard deviations"

→ Find the exact spending increase and effect size. Are $1,100 and 0.10 SD the correct figures?"""
    },
    {
        "name": "single_angrist2013",
        "key": "angrist2013",
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM (angrist2013 — Angrist et al. 2013, "Stand and Deliver: Effects of Boston's Charter High Schools", JOLE):
"Boston charter middle schools raise math scores by approximately 0.33 standard deviations per year of attendance; charter high schools raise ELA scores by approximately 0.22 standard deviations and math scores by approximately 0.29 standard deviations"

→ Find the exact effect size figures for:
1. Middle school math (per year)
2. High school ELA
3. High school math
Are 0.33, 0.22, and 0.29 the correct figures?"""
    },
    {
        "name": "single_credostanford2015",
        "key": "credostanford2015",
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM (credostanford2015 — CREDO 2015, "Online Charter School Study", Stanford):
"Students in online charter schools lose approximately 180 days of learning in math and 72 days in reading compared to traditional public school students"

→ Find the exact days-of-learning figures for math and reading. Confirm which subject has the larger loss. How is the days-of-learning conversion calculated?"""
    },
    {
        "name": "single_ehri2001",
        "key": "ehri2001",
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM (ehri2001 — Ehri et al. 2001, "Systematic Phonics Instruction Helps Students Learn to Read", Review of Educational Research):
"Systematic phonics instruction produces effect sizes of approximately d=0.41 compared to unsystematic or no phonics instruction"

→ Find the exact effect size. Is d=0.41 correct (vs. d=0.44)? What comparison groups are used? Is this the overall effect or a specific subgroup?"""
    },
    {
        "name": "single_castles2018",
        "key": "castles2018",
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM (castles2018 — Castles, Rastle & Nation 2018, "Ending the Reading Wars", Psychological Science in the Public Interest):
"The scientific consensus strongly supports systematic phonics instruction as the most effective approach to early reading instruction"

→ Is this an accurate characterization of the paper's conclusion? Does the paper use the phrase "scientific consensus"? What nuances does it add?"""
    },
    {
        "name": "single_cook2015",
        "key": "cook2015",
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM (cook2015 — Heller, Pollack, Ander & Ludwig NBER w19014, Chicago tutoring/mentoring RCT):
"High-dosage tutoring in Chicago produced effect sizes of approximately d=0.19 in math and reduced course failures"

→ Find the exact math effect size. Is d=0.19 correct? What does the paper say about course failures specifically? What was the tutoring dosage?"""
    },
    {
        "name": "single_nickow2020",
        "key": "nickow2020",
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM (nickow2020 — Nickow, Oreopoulos & Quan 2020, "The Impressive Effects of Tutoring on PreK-12 Learning", NBER):
"A meta-analysis of 96 tutoring studies finds average effect sizes of d=0.37 across all tutoring types, with high-dosage in-school tutoring producing effects of d=0.49"

→ Find the exact effect sizes and number of studies. Are d=0.37, d=0.49, and 96 studies the correct figures?"""
    },
    {
        "name": "single_durlak2011",
        "key": "durlak2011",
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM (durlak2011 — Durlak et al. 2011, "The Impact of Enhancing Students' Social and Emotional Learning", Child Development):
"A meta-analysis of 213 school-based SEL programs finds an average effect size of d=0.57 on social-emotional skills and d=0.27 on academic achievement"

→ Find the exact effect sizes and number of studies. Are d=0.57, d=0.27, and 213 programs the correct figures?"""
    },
    {
        "name": "single_cred2017",
        "key": "cred2017",
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM (cred2017 — Credé, Tynan & Harms 2017, "Much Ado About Grit", JPSP):
"Grit predicts academic performance with r=0.18 after controlling for conscientiousness, and the incremental validity of grit over conscientiousness is minimal"

→ Find the exact correlation. Is r=0.18 correct? What does the paper say about incremental validity over conscientiousness specifically?"""
    },
    {
        "name": "single_sisk2018",
        "key": "sisk2018",
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM (sisk2018 — Sisk et al. 2018, "To What Extent and Under Which Circumstances Are Growth Mind-Sets Important?", Psychological Science):
"Growth mindset interventions produce average effect sizes of d=0.08 on academic achievement in experimental studies, with larger effects for at-risk students"

→ Find the exact effect size for interventions. Is d=0.08 correct? What does the paper say about at-risk students specifically?"""
    },
    {
        "name": "single_reardon2011",
        "key": "reardon2011",
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM (reardon2011 — Reardon 2011, "The Widening Academic Achievement Gap Between the Rich and the Poor"):
"The income-achievement gap is approximately 30–40% larger among children born in 2001 than among those born 25 years earlier"

→ Find the exact percentage. Is 30–40% the correct range? What is the exact figure reported?"""
    },
    {
        "name": "single_alexander2007",
        "key": "alexander2007",
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM (alexander2007 — Alexander, Entwisle & Olson 2007, "Lasting Consequences of the Summer Learning Gap", American Sociological Review):
"Two-thirds of the 9th-grade reading achievement gap between high- and low-income students can be attributed to differential summer learning loss during elementary school"

→ Find the exact proportion. Is two-thirds correct? What specific figure does the paper report?"""
    },
    {
        "name": "single_mourshed2010",
        "key": "mourshed2010",
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM (mourshed2010 — McKinsey & Company 2010, "How the World's Most Improved School Systems Keep Getting Better"):
"The most improved school systems share common features: strong teacher recruitment and training, data-driven instruction, and sustained political commitment"

→ Is this an accurate summary of the report's main findings? What are the specific features the report identifies as common to improved systems?"""
    },
]


def load_pdf_excerpt_as_base64(key: str, max_pages: int = 90) -> tuple[str, int]:
    """Load PDF, truncating to max_pages if needed."""
    pdf_path = LIBDIR / f"{key}.pdf"
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    src = fitz.open(pdf_path)
    total_pages = len(src)
    
    if total_pages <= max_pages:
        src.close()
        with open(pdf_path, "rb") as f:
            return base64.standard_b64encode(f.read()).decode("utf-8"), total_pages
    else:
        # Extract first max_pages pages
        out = fitz.open()
        out.insert_pdf(src, from_page=0, to_page=max_pages-1)
        import io
        buf = io.BytesIO()
        out.save(buf)
        buf.seek(0)
        data = buf.read()
        src.close()
        out.close()
        print(f"    (truncated to {max_pages} of {total_pages} pages)")
        return base64.standard_b64encode(data).decode("utf-8"), max_pages


def run_single(client, task: dict) -> str:
    name = task["name"]
    key = task["key"]
    claims = task["claims"]
    
    print(f"\n{'='*50}")
    print(f"Running: {name}")
    
    try:
        pdf_b64, pages = load_pdf_excerpt_as_base64(key)
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
    
    for task in SINGLE_PAPER_TASKS:
        try:
            result = run_single(client, task)
            all_results[task["name"]] = result
            time.sleep(1)
        except Exception as e:
            print(f"  ERROR in {task['name']}: {e}")
            failed.append((task["name"], str(e)))
            time.sleep(3)
    
    # Append to consolidated report
    consolidated_path = OUTPUT_DIR / "claude_pdf_review_all_batches.md"
    with open(consolidated_path, "a") as f:
        f.write("\n\n# Single-Paper Verification Results\n\n")
        for name, result in all_results.items():
            f.write(f"## {name}\n\n{result}\n\n---\n\n")
        if failed:
            f.write("## Failed\n\n")
            for name, err in failed:
                f.write(f"- **{name}**: {err}\n")
    
    print(f"\n{'='*50}")
    print(f"COMPLETE. Successful: {len(all_results)}/{len(SINGLE_PAPER_TASKS)}")
    if failed:
        print(f"Failed: {[n for n, _ in failed]}")


if __name__ == "__main__":
    if not API_KEY:
        print("ERROR: ANTHROPIC_API_KEY not set")
        exit(1)
    main()
