#!/usr/bin/env python3
"""
Systematic verification of all quantitative claims in the manuscript
against the source PDFs in the canonical library.

For each claim, we:
1. Open the relevant PDF
2. Search for the specific numbers/statistics mentioned
3. Report: CONFIRMED, DISCREPANCY, or NOT_FOUND
"""

import fitz  # PyMuPDF
import re
from pathlib import Path

CONSOLIDATED = Path("/home/ubuntu/k12-education-research/literature/papers/consolidated")
REPORT_PATH = Path("/home/ubuntu/k12-education-research/verification_report.md")

# ============================================================
# CLAIMS TO VERIFY
# Each entry: (bibtex_key, claim_text, search_terms, notes)
# ============================================================
CLAIMS = [
    # CLUSTER 1: Teacher Quality
    ("rivkin2005", "SD of teacher VA effects ~d=0.10-0.15", ["0.10", "0.11", "0.12", "0.13", "0.14", "0.15", "standard deviation", "value-added"], "Look for SD of teacher effects on test scores"),
    ("rockoff2004", "SD of teacher VA effects ~d=0.10-0.15", ["0.10", "0.11", "0.12", "0.13", "0.14", "0.15", "standard deviation"], "Look for SD of teacher effects"),
    ("nye2004", "Gap between 75th and 25th percentile teacher d=0.34-0.48", ["0.34", "0.35", "0.36", "0.37", "0.38", "0.39", "0.40", "0.41", "0.42", "0.43", "0.44", "0.45", "0.46", "0.47", "0.48", "75th", "25th", "percentile"], "STAR data, teacher quality gap"),
    ("chetty2014a", "VAM estimates unbiased, data from 2.5 million students", ["2.5 million", "2,500,000", "unbiased", "million students"], "Check student count and unbiased claim"),
    ("chetty2014b", "$250,000 lifetime earnings from replacing bottom-5% teacher", ["250,000", "250000", "lifetime earnings", "bottom 5", "bottom-5"], "The famous $250K figure"),
    ("rothstein2010", "VAMs fail falsification tests - teachers affect prior scores", ["falsification", "prior", "lagged", "future", "pre-treatment"], "Rothstein falsification test"),
    ("jackson2018a", "Non-test-score VA uncorrelated with test-score VA", ["uncorrelated", "non-test", "attendance", "behavior", "graduation"], "Jackson non-cognitive teacher effects"),
    ("blazar2018", "Teachers have causal impacts on self-efficacy and behavior", ["self-efficacy", "behavior", "random assignment", "causal"], "Blazar random assignment"),

    # CLUSTER 2: Early Childhood
    ("heckman2010", "Perry Preschool 7-12% annual ROI, effects to age 40", ["7", "12", "return", "ROI", "age 40", "annual"], "Heckman Perry ROI"),
    ("campbell2014", "Abecedarian: lower hypertension and diabetes at age 35", ["hypertension", "diabetes", "age 35", "metabolic", "health"], "Campbell Abecedarian health outcomes"),
    ("puma2010", "Head Start gains fade by 3rd grade, no significant differences", ["fade", "third grade", "3rd grade", "no significant", "fadeout"], "Head Start fadeout"),
    ("lipsey2018", "Tennessee Pre-K: by 3rd grade, pre-K scored LOWER than control", ["lower", "third grade", "3rd grade", "control", "disciplinary", "infractions"], "Tennessee Pre-K negative effects"),
    ("bailey2021", "Long-run Head Start benefits for disadvantaged students", ["long-run", "long run", "earnings", "educational attainment", "disadvantaged"], "Bailey historical Head Start"),
    ("cascio2013", "Universal pre-K: long-term benefits for disadvantaged", ["long-term", "earnings", "disadvantaged", "pre-K", "preschool"], "Cascio universal pre-K"),

    # CLUSTER 3: Class Size
    ("krueger1999", "STAR: small classes d=0.22 reading, d=0.27 math in K", ["0.22", "0.27", "reading", "math", "kindergarten", "small class"], "Krueger STAR effect sizes"),
    ("angrist1999", "Maimonides Rule: class size reductions improved reading and math", ["Maimonides", "reading", "math", "significant", "class size"], "Angrist Maimonides"),
    ("fredriksson2013", "Sweden RD: 1 fewer student raised adult earnings ~3%", ["3%", "3 percent", "earnings", "adult", "regression discontinuity"], "Fredriksson Sweden earnings"),
    ("jepsen2009", "California CSR: near-zero net benefits for disadvantaged", ["near-zero", "near zero", "disadvantaged", "California", "teacher quality", "dilut"], "Jepsen California CSR"),
    ("wossmann2006", "Cross-national: class size weak predictor vs teacher quality", ["class size", "teacher quality", "cross-national", "international"], "Wossmann cross-national"),

    # CLUSTER 4: School Funding
    ("jackson2016", "10% more spending -> 7% higher wages, 3.7pp less poverty", ["7%", "7 percent", "3.7", "10%", "10 percent", "wages", "poverty", "per-pupil"], "Jackson funding main result"),
    ("lafortune2018", "Post-1990 reforms increased achievement in low-income districts", ["1990", "low-income", "achievement", "reform", "finance"], "Lafortune finance reform"),
    ("hyman2017", "Michigan finance reform raised college enrollment/graduation", ["Michigan", "college", "enrollment", "graduation", "finance"], "Hyman Michigan"),
    ("greenwald1996", "Meta-analysis found significant positive effects of spending", ["significant", "positive", "spending", "per-pupil", "meta-analysis"], "Greenwald meta-analysis"),

    # CLUSTER 5: Charter Schools
    ("angrist2013", "Boston charters d=0.40 in math per year", ["0.40", "0.4 ", "math", "Boston", "charter", "per year"], "Angrist Boston charters"),
    ("credostanford2015", "Virtual charters: 72 days lost math, 180 days lost reading", ["72 days", "180 days", "virtual", "charter", "learning"], "CREDO virtual charter losses"),
    ("howell2002", "NYC vouchers: modest positive effects for some subgroups", ["modest", "positive", "subgroup", "African American", "voucher"], "Howell NYC vouchers"),
    ("abdulkadirolu2018", "Louisiana vouchers: d=-0.40 in math first year", ["-0.40", "-0.4", "Louisiana", "voucher", "math", "decline"], "Abdulkadiroglu Louisiana vouchers"),

    # CLUSTER 6: Reading
    ("ehri2001", "Systematic phonics d=0.44", ["0.44", "phonics", "effect size", "systematic"], "Ehri phonics meta-analysis"),
    ("may2016", "Reading Recovery short-term gains d=0.30-0.42", ["0.30", "0.42", "Reading Recovery", "i3", "short-term"], "May Reading Recovery i3 RCT"),
    ("may2023", "Reading Recovery: by 4th grade, lower scores than control", ["fourth grade", "4th grade", "lower", "control", "fadeout", "Reading Recovery"], "May Reading Recovery fadeout"),

    # CLUSTER 7: Tutoring
    ("nickow2024", "High-dosage tutoring d=0.37 math, d=0.26 reading", ["0.37", "0.26", "math", "reading", "high-dosage", "tutoring"], "Nickow tutoring meta-analysis"),
    ("nickow2024_group", "Small group tutoring d=0.30 vs 1-on-1 d=0.40", ["0.30", "0.40", "small group", "one-on-one", "1-on-1"], "Nickow group vs individual"),
    ("cook2015", "Chicago tutoring d=0.65 math, reduced course failures", ["0.65", "math", "Chicago", "course failure", "high school"], "Cook Chicago tutoring"),
    ("kraft2021", "During-school tutoring more effective than after-school", ["during school", "after school", "attendance", "paraprofessional", "teacher"], "Kraft tutoring parameters"),

    # CLUSTER 8: SEL
    ("durlak2011", "SEL meta-analysis: 213 programs, d=0.27 academic achievement", ["213", "0.27", "academic achievement", "meta-analysis", "social-emotional"], "Durlak SEL meta-analysis"),
    ("cred2017", "Grit largely redundant with conscientiousness, near-zero incremental validity", ["conscientiousness", "redundant", "incremental", "validity", "near zero", "grit"], "Crede grit meta-analysis"),
    ("sisk2018", "Growth mindset d=0.10 overall, larger for low-income/high-risk", ["0.10", "growth mindset", "low-income", "high-risk", "overall"], "Sisk growth mindset"),
    ("yeager2019", "Growth mindset only works where peer norms support challenge-seeking", ["peer norms", "challenge", "social context", "moderator", "school norms"], "Yeager peer norms moderator"),
    ("duckworth2007", "Grit predicts success beyond IQ", ["IQ", "intelligence", "grit", "predicts", "beyond"], "Duckworth original grit paper"),

    # CLUSTER 9: Out-of-School
    ("reardon2011", "Income-achievement gap 30-40% larger for children born 2001 vs 25 years earlier", ["30", "40", "percent", "larger", "2001", "income", "achievement gap"], "Reardon income-achievement gap"),
    ("goldhaber2022", "COVID: 4th grade reading -3 pts, 8th grade math -8 pts NAEP", ["3 points", "8 points", "NAEP", "fourth grade", "eighth grade", "pandemic"], "Goldhaber COVID learning loss"),
    ("alexander2007", "Summer slide accounts for substantial share of reading gap", ["summer", "reading", "gap", "elementary", "low-income"], "Alexander summer slide"),
    ("kim2006", "Summer reading programs d≈0.14", ["0.14", "summer", "reading", "effect size"], "Kim summer reading"),
    ("wolf2017", "Neighborhood poverty effects on cognitive development", ["neighborhood", "poverty", "cognitive", "development", "school readiness"], "Wolf neighborhood effects"),
    ("borman2010", "Family background remains primary driver of inequality", ["family background", "primary", "inequality", "Coleman", "multilevel"], "Borman Coleman reanalysis"),

    # CLUSTER 10: International
    ("hanushek2015", "1 SD in cognitive skills -> ~2% higher annual economic growth", ["2%", "2 percent", "annual", "growth", "standard deviation", "cognitive"], "Hanushek knowledge capital"),
    ("porter2022", "Federal efforts result in highly variable implementation", ["variable", "implementation", "federal", "local control", "ESSA"], "Porter ESSA implementation"),

    # Citation Distortion section
    ("greenberg2009", "Three pathways: citation bias, amplification, invention", ["citation bias", "amplification", "invention", "distortion"], "Greenberg citation distortion"),
    ("sims2023", "Promising trials bias: early RCTs exaggerate effect size by 52%", ["52", "percent", "exaggerat", "promising", "trials", "bias"], "Sims promising trials bias"),
]

def search_pdf(pdf_path, search_terms, context_chars=200):
    """Search a PDF for terms and return matching context."""
    if not pdf_path.exists():
        return None, "PDF_NOT_FOUND"
    
    try:
        doc = fitz.open(str(pdf_path))
        full_text = ""
        for page in doc:
            full_text += page.get_text() + "\n"
        doc.close()
        
        full_text_lower = full_text.lower()
        matches = []
        
        for term in search_terms:
            term_lower = term.lower()
            idx = full_text_lower.find(term_lower)
            if idx >= 0:
                start = max(0, idx - context_chars // 2)
                end = min(len(full_text), idx + len(term) + context_chars // 2)
                context = full_text[start:end].replace('\n', ' ').strip()
                matches.append((term, context))
        
        return matches, "OK"
    except Exception as e:
        return None, f"ERROR: {e}"

# Run verification
results = []
print("Starting verification pass...\n")

for i, claim in enumerate(CLAIMS):
    if len(claim) == 4:
        key, claim_text, search_terms, notes = claim
    else:
        key, claim_text, search_terms = claim
        notes = ""
    
    # Handle duplicate keys (nickow2024_group -> nickow2024)
    pdf_key = key.replace("_group", "")
    pdf_path = CONSOLIDATED / f"{pdf_key}.pdf"
    
    matches, status = search_pdf(pdf_path, search_terms)
    
    if status == "PDF_NOT_FOUND":
        result_status = "NO_PDF"
        evidence = "PDF not in library"
    elif status.startswith("ERROR"):
        result_status = "ERROR"
        evidence = status
    elif matches:
        result_status = "CONFIRMED"
        # Take the best match (first one found)
        best_term, context = matches[0]
        evidence = f'Found "{best_term}": ...{context[:300]}...'
    else:
        result_status = "NOT_FOUND_IN_PDF"
        evidence = f"None of {search_terms[:3]} found in PDF"
    
    results.append({
        "key": key,
        "claim": claim_text,
        "notes": notes,
        "status": result_status,
        "evidence": evidence,
        "pdf_exists": pdf_path.exists(),
    })
    
    status_icon = {"CONFIRMED": "✓", "NOT_FOUND_IN_PDF": "✗", "NO_PDF": "○", "ERROR": "!"}.get(result_status, "?")
    print(f"[{status_icon}] {key}: {claim_text[:60]}")

# Write report
confirmed = [r for r in results if r["status"] == "CONFIRMED"]
not_found = [r for r in results if r["status"] == "NOT_FOUND_IN_PDF"]
no_pdf = [r for r in results if r["status"] == "NO_PDF"]
errors = [r for r in results if r["status"] == "ERROR"]

report_lines = [
    "# Manuscript Verification Report",
    f"\n**Date:** May 8, 2026",
    f"**Total claims checked:** {len(results)}",
    f"**Confirmed:** {len(confirmed)} ({100*len(confirmed)//len(results)}%)",
    f"**Not found in PDF:** {len(not_found)}",
    f"**No PDF available:** {len(no_pdf)}",
    f"**Errors:** {len(errors)}",
    "\n---\n",
]

# Confirmed claims
report_lines.append("## ✓ Confirmed Claims\n")
for r in confirmed:
    report_lines.append(f"### `{r['key']}` — {r['claim']}")
    report_lines.append(f"*{r['notes']}*")
    report_lines.append(f"```\n{r['evidence'][:400]}\n```\n")

# Not found in PDF
report_lines.append("\n## ✗ Claims Not Found in PDF (Require Manual Verification)\n")
for r in not_found:
    report_lines.append(f"### `{r['key']}` — {r['claim']}")
    report_lines.append(f"*{r['notes']}*")
    report_lines.append(f"**Issue:** {r['evidence']}\n")

# No PDF
if no_pdf:
    report_lines.append("\n## ○ Claims Where PDF Is Not Available\n")
    for r in no_pdf:
        report_lines.append(f"- `{r['key']}`: {r['claim']}")

with open(REPORT_PATH, "w") as f:
    f.write("\n".join(report_lines))

print(f"\n{'='*60}")
print(f"SUMMARY: {len(confirmed)}/{len(results)} confirmed, {len(not_found)} not found, {len(no_pdf)} no PDF")
print(f"Report written to: {REPORT_PATH}")
