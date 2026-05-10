# Human-AI K-12 Evidence Project

**A systematic, AI-assisted evidence synthesis of causal research across ten core domains of K-12 education policy.**

Website: [k12evidence.org](https://k12evidence.org) · Contact: [avi@k12evidence.org](mailto:avi@k12evidence.org)

**This is a living research project, not a finished product.** The first literature review (10 clusters, 124 papers) and first replication study represent the opening phase of a longer-term program. New clusters, updated syntheses, additional replication studies, and practitioner summaries will be added as the work progresses.

**Principal Investigator**: Avi Turetsky  
**Execution Agent**: Manus  
**Audit Agent**: Claude  
**Editorial Review**: Perplexity  
**Literature Tools**: Elicit, Semantic Scholar

> **Accuracy note:** This project uses a multi-agent AI-assisted workflow with multiple independent verification passes, but cannot guarantee zero errors. If you identify a factual error or a claim that does not match the cited source, please [report it](https://k12evidence.org/contact).

---

## Project Status

| Module | Status | Output |
|---|---|---|
| Literature Review (10 clusters, 124 papers) | **Complete** | `drafts/literature_review_complete.tex` (52 pp) |
| JJP (2016) Replication Study | **Complete** | `drafts/jjp_replication_note.md` |
| Website (k12evidence.org) | Planned | — |

---

## Replication Study: Jackson, Johnson & Persico (2016)

**Paper**: Jackson, C.K., Johnson, R.C., & Persico, C. (2016). The Effects of School Spending on Educational and Economic Outcomes: Evidence from School Finance Reforms. *Quarterly Journal of Economics*, 131(1), 157–218. https://doi.org/10.1093/qje/qjv036

**Replication Package (Zenodo)**: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20109658.svg)](https://doi.org/10.5281/zenodo.20109658)

### Summary of Findings

This replication uses a state-level approximation in place of the original district-level PSID restricted geocode data. Three analyses were conducted:

1. **First Stage (Spending Panel)**: Using Census INDFIN 1967–1991, we confirm that court-ordered school finance reforms increased per-pupil spending. State-level first-stage coefficient: +$157/year (SE $94.3, F = 2.8). Direction is consistent with JJP; precision is attenuated by state-level aggregation.

2. **Reduced-Form Adult Outcomes (ACS 2019 PUMS)**: Using N = 538,850 individuals born 1955–1985 across 10 states, we find a statistically significant reduced-form effect of reform exposure on high school graduation (+0.9 pp, p = 0.002). Effects on wages and poverty are in the expected direction but not significant — consistent with a weak state-level instrument. The full 2SLS design is not identified at the state level (instrument near-collinear with state FEs).

3. **Out-of-Sample Extension (SEDA v6.0)**: The late-reform DiD estimate (−0.117 SD) is unreliable due to only 2 treatment states present in the SEDA admindist coverage. The cross-sectional check yields a near-zero, insignificant coefficient (−0.021 SD, p = 0.820). The SEDA extension is inconclusive.

**Key constraint**: The full JJP IV design requires the restricted PSID geocode file (district-level), available via University of Michigan Data Use Agreement. Without it, the 2SLS estimator is degenerate at the state level.

### Key Files

| File | Description |
|---|---|
| `drafts/jjp_replication_note.md` | Replication note with all results |
| `analysis/replication_plan_jjp2016.md` | Pre-registered replication plan |
| `drafts/claude_verification_log.md` | Independent verification by Claude |
| `replication/code/01_build_spending_panel.py` | INDFIN spending panel |
| `replication/code/02c_process_real_acs.py` | ACS PUMS processing (N=538,850) |
| `replication/code/03_iv_regression_parts1_2.py` | Reduced-form regressions |
| `replication/code/04_seda_analysis_part3.py` | SEDA out-of-sample test |
| `replication/data/raw/sfr_timing_jjp2016.csv` | Reform timing data (28 states) |
| `replication/results/` | Tables (CSV) and figures (PNG) |

---

## Literature Review

A systematic synthesis of 124 papers across 10 clusters, covering the causal evidence on K-12 education interventions and their effects on student outcomes.

**Clusters**: (1) Teacher Quality, (2) Early Childhood Education, (3) Class Size, (4) School Funding, (5) School Choice, (6) Reading Instruction, (7) High-Dosage Tutoring, (8) SEL and Non-Cognitive Skills, (9) Out-of-School Factors, (10) International Systems.

**Note:** Source PDFs of reviewed papers are not included in this public repository due to copyright restrictions.

**Key files**: `drafts/literature_review_complete.tex`, `drafts/k12_references.bib`

---

## Data Sources

All analyses use real public-use data only:

- **Census INDFIN 1967–1991**: https://www2.census.gov/programs-surveys/gov-finances/datasets/historical/
- **ACS 2019 PUMS**: https://www2.census.gov/programs-surveys/acs/data/pums/2019/1-Year/
- **SEDA v6.0**: https://edopportunity.org/opportunity/data/downloads/
- **Reform timing**: Digitized from JJP Appendix Table A1 (28 states, 1971–1990)

---

## Citation

If you use materials from this repository, please cite the relevant outputs:

**Literature review:**
> Turetsky, A. (2026). *Human-AI K-12 Evidence Project: A Systematic Evidence Synthesis of K-12 Education Research*. Living research project, updated May 2026. https://k12evidence.org

**Replication package:**
> Turetsky, A. (2026). *Replication Package: School Finance Reforms and Educational Outcomes — A Partial Replication and Out-of-Sample Extension of Jackson, Johnson & Persico (2016)*. Zenodo. https://doi.org/10.5281/zenodo.20109658

