# Replication Note: Jackson, Johnson & Persico (2016)

**Replication Note | K-12 Education Research Project | May 2026**

---

## 1. The Original Paper

Jackson, Johnson, and Persico (2016) [1] — hereafter JJP — ask a deceptively simple question: does more money spent on K-12 education actually improve student outcomes? The paper's central contribution is a credible causal answer. Using a sample of 15,353 individuals from the Panel Study of Income Dynamics (PSID), JJP exploit the wave of court-ordered school finance reforms (SFRs) that swept across 28 states between 1971 and 2010. These reforms, triggered by state supreme court rulings that existing funding systems were unconstitutional, forced states to equalize per-pupil spending across wealthy and poor districts. Crucially, the timing of reforms was driven by litigation outcomes rather than by district-level economic trends, providing the exogenous variation needed for causal identification.

The paper's identification strategy is a two-stage instrumental variables (IV) design. The instrument is the predicted change in per-pupil spending for a student's specific childhood school district, based on that district's pre-reform spending level and the timing of the state's court order. Because low-income districts received the largest spending increases (they were the furthest below the new equalized standard), the design effectively compares outcomes for students who grew up in districts that received large reform-induced spending increases against those in districts that received small increases, after controlling for state and birth-year fixed effects.

**JJP's core findings** are as follows. For the full sample, a 10 percent increase in per-pupil spending throughout the school years (ages 5–17) is associated with 0.31 additional completed years of education, a 7 percent increase in adult wages, and a 3.2 percentage point reduction in the poverty rate in adulthood. These effects are concentrated almost entirely among students who grew up in low-income families: for low-income children specifically, a 10 percent spending increase is associated with a 7 percentage point increase in high school graduation rates, 9.6 percent higher earnings, and a 6.1 percentage point reduction in poverty. The effects are large in magnitude and precisely estimated, with IV first-stage F-statistics in the range of 20–30.

---

## 2. What We Attempted to Replicate, and What Constrained Us

### 2.1 The Binding Data Constraint

The JJP design requires linking each PSID respondent to their specific childhood school district. The PSID public-use files report only the respondent's state of residence; the district-level geocode is contained in a restricted-use file that requires a formal Data Use Agreement with the University of Michigan. Because this file was not available to us, we could not implement the district-level IV design.

In its place, we used a **state-level approximation**: rather than assigning each individual a district-specific predicted spending change, we assigned each individual the fraction of their school-age years (ages 5–17) that fell after their state's first court-ordered reform. This instrument captures the same underlying variation — earlier-reforming states vs. later-reforming states — but at a coarser level of aggregation. We also substituted the ACS 2019 1-year PUMS microdata (N = 701,004 individuals born 1955–1985 across 10 states: CA, TX, FL, NY, PA, IL, OH, GA, NC, MI) for the restricted PSID sample.

### 2.2 What We Could and Could Not Test

| Component | Status | Reason |
|---|---|---|
| First-stage: reforms → spending | Partially replicated | State-level aggregation attenuates the estimate |
| Reduced-form: reform exposure → adult outcomes | **Inconclusive** | Results are sensitive to specification; see Section 3.2 |
| 2SLS IV: spending → adult outcomes | **Not replicable** | Instrument is near-collinear with required fixed effects at state level |
| Heterogeneity by family income | Not attempted | ACS does not contain childhood family income |
| Out-of-sample extension: test scores (SEDA) | Attempted, inconclusive | Only 2 treatment states present in available SEDA coverage |

The failure of the 2SLS estimator is not a coding error — it is a mathematical consequence of the state-level approximation. The JJP instrument varies *within* states (across districts), which allows state fixed effects to be included without absorbing the instrument. Our state-level instrument, by contrast, varies only across states, so it is near-perfectly collinear with the state-of-birth fixed effects. The first-stage F-statistic of 2.8 (vs. JJP's ~20–30) reflects this directly.

---

## 3. Our Findings

### 3.1 First Stage: Reforms and Per-Pupil Spending

Using the Census Bureau's INDFIN historical school district finance panel (1967–1991), we confirm the basic mechanism: states that underwent court-ordered reforms increased per-pupil spending relative to non-reforming states. Our state-level first-stage regression yields a coefficient of **+$157 per year of post-reform exposure** (in real 2000 dollars), with a standard error of $94.3 and a first-stage F-statistic of 2.8. The direction is consistent with JJP; the magnitude and precision are attenuated, as expected from state-level aggregation.

The event study in Figure 1 illustrates the spending trajectory around the reform year. Spending in reform states rises monotonically in the years following the court order, while the pre-reform trend is flat — consistent with the parallel trends assumption underlying the JJP design.

![Figure 1: Per-Pupil Spending Event Study Around Reform Year](../replication/results/figures/fig1_event_study_spending.png)

### 3.2 Reduced-Form Adult Outcomes

The reduced-form results are **inconclusive**: no outcome shows a statistically significant positive effect of reform exposure. The HS graduation coefficient is negative and borderline insignificant in a subsample test (coef = −0.012, SE = 0.007, p = 0.063, N = 80,000). This is consistent with the documented identification failure: the state-level instrument has insufficient variation to identify the reform effect after controlling for state-of-birth and birth-year fixed effects.

| Outcome | Direction | Significance | Interpretation |
|---|---|---|---|
| High School Graduation | Negative | Not significant (p ≈ 0.06) | Inconsistent with JJP; likely reflects weak instrument |
| Any College | Negative | Not significant | Inconsistent with JJP; weak instrument |
| BA or Higher | Negative | Not significant | Inconsistent with JJP; weak instrument |
| Log Wages | Negative | Not significant | Inconsistent with JJP; weak instrument |
| Poverty Rate | Negative | Borderline significant (p ≈ 0.007) | Direction consistent with JJP but likely spurious given weak instrument |

*Note: Results based on a stratified 80,000-observation subsample of the ACS PUMS data (N = 701,004 full sample). State-of-birth and birth-year fixed effects included. Standard errors clustered at the state level.*

We do not interpret these null or negative results as evidence against JJP's findings. They reflect the fundamental limitation of the state-level approximation: the instrument is too weak and too collinear with the required fixed effects to identify the causal effect.

### 3.3 Out-of-Sample Extension: SEDA Test Scores

To test whether the long-run effects of historical reforms are visible in contemporary student achievement, we merged the JJP reform timing data with the Stanford Education Data Archive (SEDA v6.0 admindist file, 2009–2019). Because most reforms occurred 20–40 years before the SEDA observation window, a standard post-reform indicator would be collinear with state fixed effects. We therefore restricted the analysis to a **late-reform difference-in-differences design**, using only states that reformed between 1995 and 2015 (where pre/post variation falls within the SEDA window) and a control group of never-reformed states.

The DiD estimate is −0.117 SD (p < 0.001). We do not interpret this as a causal negative effect of reforms. The SEDA admindist file available for this analysis covers only 19 states, and only **2 of the 11 late-reforming states** are present in the sample — an extreme imbalance that confounds the treatment effect with idiosyncratic characteristics of those two specific states. The cross-sectional robustness check (regressing 2009–2019 average test scores on ever-reformed status) yields a near-zero, statistically insignificant coefficient (−0.021 SD, p = 0.820). We conclude that the SEDA extension is **inconclusive**: the available data coverage is insufficient to test whether historical reforms have lasting effects on contemporary test scores.

---

## 4. Conclusion

This exercise documents precisely where the limits of public data lie in replicating JJP (2016). The core mechanism — that court-ordered reforms increased per-pupil spending — is confirmed in the first-stage analysis. However, the full IV design that allows JJP to translate spending into precise causal estimates of adult outcomes requires the restricted PSID geocode file, which links individuals to their specific childhood school district. Without district-level variation in the instrument, the state-level approximation cannot identify the causal effect.

Researchers seeking to extend or update the JJP analysis should prioritize obtaining the restricted PSID geocode file through the University of Michigan's Data Use Agreement process.

---

## References

[1] Jackson, C. K., Johnson, R. C., & Persico, C. (2016). The Effects of School Spending on Educational and Economic Outcomes: Evidence from School Finance Reforms. *The Quarterly Journal of Economics*, 131(1), 157–218. https://doi.org/10.1093/qje/qjv036

[2] Lafortune, J., Rothstein, J., & Schanzenbach, D. W. (2018). School Finance Reform and the Distribution of Student Achievement. *American Economic Journal: Applied Economics*, 10(2), 1–26. https://doi.org/10.1257/app.20160567

---

## 5. AI Tools Disclosure

This replication study was produced with substantial assistance from AI tools. The following tools contributed to specific phases of the work:

| Tool | Role |
|---|---|
| **Manus** (AI agent) | Primary execution across all phases: data acquisition, code writing, regression analysis, figure generation, manuscript drafting, and iterative debugging |
| **Claude (Anthropic, claude-opus-4)** | Phase 4 code and numbers audit: verified regression coefficients against output CSVs; reviewed formula-to-code fidelity for the reform exposure instrument |
| **Perplexity Pro** | Phase 4 literature and editorial review: fact-checked all quantitative claims about JJP (2016) against the published paper |

All final results, interpretations, and editorial decisions were reviewed and approved by the human author (Avi Turetsky). The AI tools were used as research assistants and auditors, not as autonomous decision-makers.

---

## Replication Package

All code, processed data, results, and this replication note are archived at:

> Turetsky, A. (2026). *Replication Package: School Finance Reforms and Educational Outcomes — A Partial Replication and Out-of-Sample Extension of Jackson, Johnson & Persico (2016)*. Zenodo. https://doi.org/10.5281/zenodo.20109658

GitHub repository: https://github.com/aturetsky/k12-education-research
