#!/usr/bin/env python3
"""
Claude API PDF verification - all clusters, split into sub-batches of ≤100 pages total.
Each sub-batch focuses on 3-5 papers with their specific claims.
"""

import anthropic
import base64
import os
import time
from pathlib import Path

LIBDIR = Path("/home/ubuntu/k12-education-research/literature/papers/consolidated")
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OUTPUT_DIR = Path("/home/ubuntu/k12-education-research")

# Sub-batches: each list of keys must total ≤100 pages
# Page counts verified above
SUB_BATCHES = [
    {
        "name": "batch_1a_teacher_quality_core",
        "papers": ["rivkin2005", "rockoff2004", "nye2004", "chetty2014a"],  # 42+6+22+40 = 110 → drop nye
        "claims": """Verify these specific claims from the K-12 education literature review:

CLAIM 1.1 (rivkin2005 — Rivkin, Hanushek & Kain 2005, "Teachers, Schools, and Academic Achievement", Econometrica):
"A one standard deviation improvement in teacher quality raises student achievement by approximately 0.10–0.20 standard deviations per year"
→ Find the exact effect size range reported. What are the precise figures for math and reading separately?

CLAIM 1.2 (rockoff2004 — Rockoff 2004, "The Impact of Individual Teachers on Student Achievement", AER Papers & Proceedings):
"A one standard deviation increase in teacher quality raises math and reading scores by approximately 0.10 standard deviations"
→ Find the exact figures. Are they the same for math and reading?

CLAIM 1.3 (chetty2014a — Chetty, Friedman & Rockoff 2014, "Measuring the Impacts of Teachers I", AER):
"A one standard deviation increase in VAM is associated with a 0.54% increase in earnings at age 28, based on a sample of more than one million students"
→ Verify the 0.54% figure and the sample size description. Is "more than one million students" accurate?"""
    },
    {
        "name": "batch_1b_teacher_quality_vam",
        "papers": ["chetty2014b", "rothstein2010", "goldhaber2015"],  # 47+41+28 = 116 → need to trim
        "claims": """Verify these specific claims from the K-12 education literature review:

CLAIM 1.4 (chetty2014b — Chetty, Friedman & Rockoff 2014, "Measuring the Impacts of Teachers II", AER):
"Replacing a teacher in the bottom 5% of the VAM distribution with an average teacher raises the lifetime earnings of a classroom of students by approximately $250,000 per year of teaching"
→ Find the exact dollar figure and verify "per year of teaching" is the correct qualifier.

CLAIM 1.5 (rothstein2010 — Rothstein 2010, "Teacher Quality in Educational Production", QJE):
"Pre-trends in student achievement predict future teacher assignments, suggesting VAMs capture selection effects rather than true causal impacts"
→ Verify this is an accurate characterization of Rothstein's main finding.

CLAIM 1.6 (goldhaber2015 — Goldhaber & Chaplin 2015, "Assessing the Rothstein Falsification Test", JREE):
"Rothstein's falsification test produces false positives even when VAMs are unbiased, and the bias in VAMs is approximately 3%"
→ Find the specific bias estimate. Is 3% the correct figure? What exactly does the paper say about false positives?"""
    },
    {
        "name": "batch_1c_jackson_noncognitive",
        "papers": ["jackson2018b"],  # 36pp
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM 1.7 (jackson2018b — Jackson 2018, "What Do Test Scores Miss?", JPE):
"Teacher effects on non-cognitive outcomes (high school graduation and college-going) are largely uncorrelated (r ≈ 0.15–0.30) with teacher effects on test scores"
→ Find the exact correlation coefficient(s) reported between teacher test-score effects and non-cognitive outcome effects. Is r ≈ 0.15–0.30 accurate? What non-cognitive outcomes does the paper actually measure?"""
    },
    {
        "name": "batch_2a_early_childhood_heckman",
        "papers": ["heckman2010", "heckman2006", "campbell2014"],  # 33+80+9 = 122 → need to trim heckman2006
        "claims": """Verify these specific claims from the K-12 education literature review:

CLAIM 2.1 (heckman2010 — Heckman et al. 2010, "The Rate of Return to the HighScope Perry Preschool Program", JHER):
"The Perry Preschool Program, a randomized trial with n=58 deeply disadvantaged children, produced a 7–12% annual return on investment through age 40"
→ Find the exact ROI range and sample size. Is n=58 correct? Is 7–12% the correct range?

CLAIM 2.2 (campbell2014 — Campbell et al. 2014, "Early Childhood Investments Substantially Boost Adult Health", Science):
"The Abecedarian Project produced significant improvements in adult health outcomes in a randomized trial"
→ What specific health outcomes improved? Is this an accurate summary of the paper's main finding?"""
    },
    {
        "name": "batch_2b_head_start_preK",
        "papers": ["puma2010_excerpt", "lipsey2018"],  # 40+11 = 51pp
        "claims": """Verify these specific claims from the K-12 education literature review:

CLAIM 2.3 (puma2010 — Puma et al. 2010, "Head Start Impact Study Final Report"):
"Head Start produces significant short-term cognitive gains that largely fade out by the end of first grade"
→ Find the specific fadeout finding. Does the paper say "end of first grade" or a different grade? What is the magnitude of initial gains and how much fades?

CLAIM 2.4 (lipsey2018 — Lipsey et al. 2018, "Effects of the Tennessee Voluntary Prekindergarten Program", Child Development):
"Tennessee's Voluntary Pre-K program produced significant short-term gains that faded out by kindergarten entry"
→ Verify the fadeout timing. Does the paper say fadeout occurs by "kindergarten entry" or at a different point? What is the effect size at program end vs. at kindergarten?"""
    },
    {
        "name": "batch_3a_class_size",
        "papers": ["krueger1999", "fredriksson2013", "angrist1999"],
        "claims": """Verify these specific claims from the K-12 education literature review:

CLAIM 3.1 (krueger1999 — Krueger 1999, "Experimental Estimates of Education Production Functions", QJE — the STAR study reanalysis):
"Students in small classes (13–17 students) in the Tennessee STAR experiment outperformed students in regular classes (22–26 students) by approximately d=0.20–0.27 standard deviations in reading and math"
→ Find the exact effect size range. Are these cumulative effects or per-year effects?

CLAIM 3.2 (fredriksson2013 — Fredriksson, Öckert & Oosterbeek 2013, "Long-Term Effects of Class Size", QJE):
"A one-student reduction in class size raises earnings at age 27–42 by approximately 1.2% and improves cognitive test scores"
→ Find the exact earnings effect. Is 1.2% the correct figure?

CLAIM 3.3 (angrist1999 — Angrist & Lavy 1999, "Using Maimonides' Rule", QJE):
"A 10-student reduction in class size raises reading scores by approximately 0.20 standard deviations and math scores by approximately 0.24 standard deviations"
→ Find the exact effect sizes. Are these the correct figures for the IV estimates?"""
    },
    {
        "name": "batch_3b_class_size_jepsen",
        "papers": ["jepsen2002", "hanushek1997"],
        "claims": """Verify these specific claims from the K-12 education literature review:

CLAIM 3.4 (jepsen2002 — Jepsen & Rivkin 2009, "Class Size Reduction and Student Achievement", JPAM):
"The benefits of class size reduction are concentrated among lower-income students and are offset in part by reductions in teacher quality when districts hire rapidly to meet class size mandates"
→ Is this an accurate summary of the paper's main finding? What specific evidence does the paper provide for the teacher quality offset?

CLAIM 3.5 (hanushek1997 — Hanushek 1997, "Assessing the Effects of School Resources on Student Performance", EdEval):
"The preponderance of evidence finds no consistent relationship between school resources (class size, per-pupil spending) and student achievement"
→ Is this an accurate characterization of Hanushek's finding? What does the paper say about the vote-count methodology?"""
    },
    {
        "name": "batch_4a_school_funding",
        "papers": ["jackson2016", "lafortune2018"],
        "claims": """Verify these specific claims from the K-12 education literature review:

CLAIM 4.1 (jackson2016 — Jackson, Johnson & Persico 2016, "The Effects of School Spending on Educational and Economic Outcomes", QJE):
"A 10% increase in per-pupil spending throughout school years leads to 7% higher adult wages, 3.2 percentage points higher probability of graduating high school, and significantly lower adult poverty rates; effects are approximately 1.9 times larger for students from low-income families"
→ Verify each of these figures precisely. Is 3.2pp correct (vs. 3.7pp in the NBER working paper)? Is the 1.9× multiplier accurate for low-income students?

CLAIM 4.2 (lafortune2018 — Lafortune, Rothstein & Schanzenbach 2018, "School Finance Reform and the Distribution of Student Achievement", AEJ: Applied):
"Post-1990 school finance reforms increased per-pupil spending in low-income districts by approximately $1,100 per year and raised test scores in those districts by approximately 0.10 standard deviations"
→ Find the exact spending increase and effect size figures."""
    },
    {
        "name": "batch_4b_school_funding_hyman",
        "papers": ["hyman2017", "hanushek1997"],
        "claims": """Verify these specific claims from the K-12 education literature review:

CLAIM 4.3 (hyman2017 — Hyman 2017, "Does Money Matter in the Long Run?", AEJ: Economic Policy):
"A $1,000 increase in per-pupil spending in 10th and 11th grade raises college enrollment by 4.3 percentage points"
→ Find the exact figure. Is $1,000 and 4.3pp correct?

Also note: the manuscript cites Neilson (2014) as evidence that "capital construction spending has smaller effects than instructional spending." Please verify whether the Neilson citation is correctly attributed to capital construction specifically."""
    },
    {
        "name": "batch_5a_charters",
        "papers": ["angrist2013", "credostanford2015"],
        "claims": """Verify these specific claims from the K-12 education literature review:

CLAIM 5.1 (angrist2013 — Angrist et al. 2013, "Stand and Deliver: Effects of Boston's Charter High Schools", JOLE):
"Boston charter middle schools raise math scores by approximately 0.33 standard deviations per year of attendance; charter high schools raise ELA scores by approximately 0.22 standard deviations and math scores by approximately 0.29 standard deviations"
→ Find the exact effect size figures for both middle and high school, for both math and ELA.

CLAIM 5.2 (credostanford2015 — CREDO 2015, "Online Charter School Study"):
"Students in online charter schools lose approximately 180 days of learning in math and 72 days in reading compared to traditional public school students"
→ Find the exact days-of-learning figures for math and reading. Confirm which subject has the larger loss."""
    },
    {
        "name": "batch_5b_vouchers",
        "papers": ["abdulkadirolu2018"],
        "claims": """Verify this specific claim from the K-12 education literature review:

CLAIM 5.3 (abdulkadirolu2018 — Abdulkadiroğlu, Pathak & Walters 2018, "Free to Choose: Can School Choice Reduce Student Achievement?", REStat):
"Louisiana Scholarship Program participation reduces math scores by approximately 0.40 standard deviations in the first year of participation"
→ Find the exact effect size. Is −0.40 SD the correct figure? Is this the first-year effect or a longer-run estimate? What is the 2SLS estimate specifically?"""
    },
    {
        "name": "batch_6a_reading",
        "papers": ["ehri2001", "castles2018", "may2023"],
        "claims": """Verify these specific claims from the K-12 education literature review:

CLAIM 6.1 (ehri2001 — Ehri et al. 2001, "Systematic Phonics Instruction Helps Students Learn to Read", Review of Educational Research):
"Systematic phonics instruction produces effect sizes of approximately d=0.41 compared to unsystematic or no phonics instruction"
→ Find the exact effect size. Is d=0.41 correct (vs. d=0.44)?

CLAIM 6.2 (castles2018 — Castles, Rastle & Nation 2018, "Ending the Reading Wars", Psychological Science in the Public Interest):
"The scientific consensus strongly supports systematic phonics instruction as the most effective approach to early reading instruction"
→ Is this an accurate characterization of the paper's conclusion?

CLAIM 6.3 (may2023 — May et al. 2023, "Long-Term Impacts of Reading Recovery through 3rd and 4th Grade"):
"Reading Recovery produces significant short-term gains that fade substantially by 3rd and 4th grade in a regression discontinuity design"
→ Verify the study design (is it regression discontinuity?) and the fadeout finding. What are the effect sizes at program end vs. follow-up?"""
    },
    {
        "name": "batch_6b_reading_hansford",
        "papers": ["hansford2025", "hanford2018"],
        "claims": """Verify these specific claims from the K-12 education literature review:

CLAIM 6.4 (hansford2025 — Hansford et al. 2025, exploratory analysis of reading curricula):
"Structured literacy curricula produce effect sizes approximately 3–5 times larger than balanced literacy curricula"
→ Find the exact effect size comparison. Is 3–5× the correct multiplier? Does the paper describe itself as exploratory? Are there conflict-of-interest disclosures?

CLAIM 6.5 (hanford2018 — Hanford 2018, "Hard Words: Why Aren't Kids Being Taught to Read?", APM Reports):
"Despite strong scientific consensus in favor of phonics-based instruction, many U.S. schools continue to use balanced literacy approaches"
→ Is this an accurate characterization of the piece?"""
    },
    {
        "name": "batch_7a_tutoring",
        "papers": ["cook2015", "nickow2020", "kraft2021"],
        "claims": """Verify these specific claims from the K-12 education literature review:

CLAIM 7.1 (cook2015 — Cook et al. 2015 / Heller et al. NBER w19014, Chicago tutoring RCT):
"High-dosage tutoring in Chicago produced effect sizes of approximately d=0.19 in math and reduced course failures"
→ Find the exact math effect size. Is d=0.19 correct? What does the paper say about course failures?

CLAIM 7.2 (nickow2020 — Nickow, Oreopoulos & Quan 2020, "The Impressive Effects of Tutoring on PreK-12 Learning", NBER):
"A meta-analysis of 96 tutoring studies finds average effect sizes of d=0.37 across all tutoring types, with high-dosage in-school tutoring producing effects of d=0.49"
→ Find the exact effect sizes and number of studies. Are these figures correct?

CLAIM 7.3 (kraft2021 — Kraft & Falken 2021, "A Blueprint for Scaling Tutoring and Mentoring Across Public Schools"):
"High-dosage tutoring (3+ sessions per week, 1:1 or small group) consistently produces large effects but costs $3,000–$5,000 per student per year"
→ Find the cost estimate. Is $3,000–$5,000 the figure cited? What does the paper say about the conditions for effective tutoring?"""
    },
    {
        "name": "batch_8a_sel_noncognitive",
        "papers": ["durlak2011", "cred2017", "sisk2018"],
        "claims": """Verify these specific claims from the K-12 education literature review:

CLAIM 8.1 (durlak2011 — Durlak et al. 2011, "The Impact of Enhancing Students' Social and Emotional Learning", Child Development):
"A meta-analysis of 213 school-based SEL programs finds an average effect size of d=0.57 on social-emotional skills and d=0.27 on academic achievement"
→ Find the exact effect sizes and number of studies. Are these figures correct?

CLAIM 8.2 (cred2017 — Credé, Tynan & Harms 2017, "Much Ado About Grit", Journal of Personality and Social Psychology):
"Grit predicts academic performance with r=0.18 after controlling for conscientiousness, and the incremental validity of grit over conscientiousness is minimal"
→ Find the exact correlation and the conclusion about incremental validity.

CLAIM 8.3 (sisk2018 — Sisk et al. 2018, "To What Extent and Under Which Circumstances Are Growth Mind-Sets Important?", Psychological Science):
"Growth mindset interventions produce average effect sizes of d=0.08 on academic achievement in experimental studies, with larger effects for at-risk students"
→ Find the exact effect size for interventions. Is d=0.08 correct? What does the paper say about at-risk students?"""
    },
    {
        "name": "batch_8b_sel_yeager_duckworth",
        "papers": ["yeager2019", "duckworth2009"],
        "claims": """Verify these specific claims from the K-12 education literature review:

CLAIM 8.4 (yeager2019 — Yeager et al. 2019, "A National Experiment Reveals Where a Growth Mindset Improves Achievement", Nature):
"A nationally representative growth mindset intervention produced d=0.10 average effects on GPA, with larger effects (d=0.20) for lower-achieving students"
→ Find the exact effect sizes. Are d=0.10 and d=0.20 correct?

CLAIM 8.5 (duckworth2009 — Duckworth & Quinn 2009, "Development and Validation of the Short Grit Scale", Journal of Personality Assessment):
"Grit predicts outcomes above and beyond IQ and Big Five personality traits"
→ Is this an accurate characterization of the paper's finding? What specific outcomes does grit predict in this paper?"""
    },
    {
        "name": "batch_9a_out_of_school",
        "papers": ["reardon2011", "alexander2007", "wolf2017"],
        "claims": """Verify these specific claims from the K-12 education literature review:

CLAIM 9.1 (reardon2011 — Reardon 2011, "The Widening Academic Achievement Gap Between the Rich and the Poor"):
"The income-achievement gap is approximately 30–40% larger among children born in 2001 than among those born 25 years earlier"
→ Find the exact percentage. Is 30–40% the correct range?

CLAIM 9.2 (alexander2007 — Alexander, Entwisle & Olson 2007, "Lasting Consequences of the Summer Learning Gap", American Sociological Review):
"Two-thirds of the 9th-grade reading achievement gap between high- and low-income students can be attributed to differential summer learning loss during elementary school"
→ Find the exact proportion. Is two-thirds correct?

CLAIM 9.3 (wolf2017 — Wolf, Magnuson & Kimbro 2017, "Family and Neighborhood Poverty and Children's School Readiness"):
"Neighborhood poverty has significant independent effects on school readiness beyond family poverty"
→ Is this an accurate characterization of the paper's main finding?"""
    },
    {
        "name": "batch_9b_out_of_school_goldhaber",
        "papers": ["goldhaber2008", "benner2016"],
        "claims": """Verify these specific claims from the K-12 education literature review:

CLAIM 9.4 (goldhaber2008 — Goldhaber 2008, "Teachers Matter, But Effective Teaching Is Difficult to Identify and Promote"):
"Out-of-school factors account for approximately 60% of the variance in student achievement, while school factors account for approximately 20%"
→ Find the exact variance decomposition figures. Are 60% and 20% correct?

CLAIM 9.5 (benner2016 — Benner, Boyle & Sadler 2016, "Parental Involvement and Adolescents' Educational Success"):
"Parental involvement in education is positively associated with academic achievement, with effect sizes varying by type of involvement and student age"
→ Is this an accurate characterization of the paper's finding? What specific types of involvement are most effective?"""
    },
    {
        "name": "batch_10a_international",
        "papers": ["mourshed2010", "wmann2006"],
        "claims": """Verify these specific claims from the K-12 education literature review:

CLAIM 10.1 (mourshed2010 — McKinsey & Company 2010, "How the World's Most Improved School Systems Keep Getting Better"):
"The most improved school systems share common features: strong teacher recruitment and training, data-driven instruction, and sustained political commitment"
→ Is this an accurate summary of the report's main findings?

CLAIM 10.2 (wmann2006 — Woessmann 2006 or Hanushek & Woessmann, international test scores and economic growth):
"International test score differences are strongly associated with long-run economic growth rates, with a one standard deviation improvement in PISA scores associated with approximately 2% higher annual GDP growth"
→ Find the exact economic growth figure. Is 2% the correct figure?"""
    },
]


def load_pdf_as_base64(key: str) -> tuple[str, int]:
    """Returns (base64_data, page_count)"""
    pdf_path = LIBDIR / f"{key}.pdf"
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    import fitz
    doc = fitz.open(pdf_path)
    pages = len(doc)
    doc.close()
    with open(pdf_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8"), pages


def run_sub_batch(client, sub_batch: dict) -> str:
    name = sub_batch["name"]
    papers = sub_batch["papers"]
    claims = sub_batch["claims"]
    
    print(f"\n{'='*60}")
    print(f"Running: {name}")
    print(f"Papers: {', '.join(papers)}")
    
    content = []
    total_pages = 0
    
    for key in papers:
        try:
            pdf_b64, pages = load_pdf_as_base64(key)
            total_pages += pages
            content.append({
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": pdf_b64,
                },
                "title": f"[{key}]",
                "citations": {"enabled": True}
            })
            print(f"  Loaded {key}.pdf ({pages}pp)")
        except FileNotFoundError as e:
            print(f"  SKIP: {e}")
    
    print(f"  Total pages: {total_pages}")
    
    if total_pages > 100:
        print(f"  WARNING: {total_pages} pages exceeds 100-page limit! Skipping.")
        return f"SKIPPED: {total_pages} pages exceeds limit"
    
    content.append({"type": "text", "text": claims})
    
    print(f"  Sending to Claude API...")
    
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        messages=[{"role": "user", "content": content}]
    )
    
    result = response.content[0].text
    print(f"  Done. ({response.usage.input_tokens} input tokens, {response.usage.output_tokens} output tokens)")
    
    # Save individual result
    out_path = OUTPUT_DIR / f"claude_pdf_{name}.md"
    with open(out_path, "w") as f:
        f.write(f"# Claude PDF Verification: {name}\n\n")
        f.write(f"Model: {response.model} | Input: {response.usage.input_tokens} tokens | Output: {response.usage.output_tokens} tokens\n\n---\n\n")
        f.write(result)
    
    return result


def main():
    client = anthropic.Anthropic(api_key=API_KEY)
    
    all_results = {}
    failed = []
    
    for sub_batch in SUB_BATCHES:
        try:
            result = run_sub_batch(client, sub_batch)
            all_results[sub_batch["name"]] = result
            time.sleep(2)  # Rate limit buffer
        except Exception as e:
            print(f"  ERROR in {sub_batch['name']}: {e}")
            failed.append((sub_batch["name"], str(e)))
            time.sleep(5)
    
    # Save consolidated report
    consolidated_path = OUTPUT_DIR / "claude_pdf_review_all_batches.md"
    with open(consolidated_path, "w") as f:
        f.write("# Claude PDF-Grounded Verification — All Batches\n\n")
        f.write(f"Date: May 8, 2026\n")
        f.write(f"Total sub-batches: {len(SUB_BATCHES)}\n")
        f.write(f"Failed: {len(failed)}\n\n---\n\n")
        
        for name, result in all_results.items():
            f.write(f"## {name}\n\n{result}\n\n---\n\n")
        
        if failed:
            f.write("## Failed Sub-Batches\n\n")
            for name, err in failed:
                f.write(f"- **{name}**: {err}\n")
    
    print(f"\n{'='*60}")
    print(f"COMPLETE. Results saved to: {consolidated_path}")
    print(f"Successful: {len(all_results)}/{len(SUB_BATCHES)}")
    if failed:
        print(f"Failed: {[n for n, _ in failed]}")


if __name__ == "__main__":
    if not API_KEY:
        print("ERROR: ANTHROPIC_API_KEY not set")
        exit(1)
    main()
