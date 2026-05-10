# Replication Plan: Jackson, Johnson & Persico (2016)

## Overview
This document outlines the plan to replicate and extend Jackson, Johnson, and Persico (2016), "The Effects of School Spending on Educational and Economic Outcomes: Evidence from School Finance Reforms" [1]. The replication will be conducted in three parts: an in-sample replication of the original findings, an extended window analysis incorporating newer cohorts, and an out-of-sample robustness check using Stanford Education Data Archive (SEDA) test scores.

Given the restricted access nature of the Panel Study of Income Dynamics (PSID) geocode data used in the original study to link individuals to their childhood school districts, this replication will employ a state-level approximation for the PSID-based analyses (Parts 1 and 2). This modification will be explicitly documented and its implications discussed.

## Part 1: In-Sample Replication (State-Level Approximation)

### Objective
Reproduce the core findings of Tables 2, 3, and 5 from JJP (2016) using the original PSID cohorts (born 1955–1985) and Common Core of Data (CCD) / Historical Database on Individual Government Finances (INDFIN) spending data.

### Methodology
1.  **Data Acquisition**:
    *   Obtain public-use PSID data (requires registration) containing individual-level outcomes (educational attainment, wages, poverty status) and state of residence during childhood [2].
    *   Download historical school district finance data (INDFIN) for 1967–1991 from the Census Bureau [3].
    *   Download CCD F-33 school district finance data for 1992–2010 from the National Center for Education Statistics (NCES) [4].
    *   Extract court-ordered school finance reform (SFR) timing data from JJP (2016) Appendix Table A1 or the Lafortune et al. (2018) replication package [5].
2.  **Data Processing**:
    *   Aggregate the district-level spending data (INDFIN/CCD) to the state level to match the geographic resolution of the public-use PSID data.
    *   Construct the instrument: state-level exposure to court-ordered reforms based on the timing of the first reform in the individual's state of residence during their school-age years (5–17).
3.  **Estimation**:
    *   Estimate the first-stage relationship between state-level reform exposure and state-average per-pupil spending (analogous to Table 2).
    *   Estimate the reduced-form and Two-Stage Least Squares (2SLS) models for the effect of spending on educational attainment (Table 3) and long-run economic outcomes (Table 5), using the state-level instrument.
    *   Quantify and discuss the expected attenuation bias introduced by using state-level rather than district-level variation.

## Part 2: Extended Window Analysis

### Objective
Extend the analysis to include PSID cohorts born through approximately 2000 and CCD spending data through 2015, testing whether the findings hold for cohorts exposed to the "adequacy" era of school finance reforms.

### Methodology
1.  **Data Extension**:
    *   Incorporate more recent waves of public-use PSID data for cohorts born 1986–2000.
    *   Extend the CCD F-33 spending panel through 2015.
    *   Update the SFR timing data to include any relevant reforms passed after the original study's cutoff.
2.  **Estimation**:
    *   Apply the state-level IV design developed in Part 1 to the extended sample.
    *   Compare the estimated effects for the post-1990 cohorts (adequacy era) with the original pre-1990 cohorts (equity era).

## Part 3: Out-of-Sample Robustness with SEDA

### Objective
Conduct an out-of-sample robustness check using SEDA district-level test score data (2009–2019) as an alternative outcome measure for newer cohorts.

### Methodology
1.  **Data Acquisition**:
    *   Download SEDA Version 6.0 district-level test score data (e.g., `seda_geodist_long_cs_6.0.csv`) [6].
    *   Utilize the CCD F-33 district-level spending data and district-level reform timing data.
2.  **Estimation**:
    *   Because SEDA provides district-level outcomes, we can execute the full district-level IV design originally intended by JJP (2016) for this part of the analysis.
    *   Estimate the effect of district-level per-pupil spending on district-average test scores, using the timing and type of court-ordered reforms as instruments.
    *   Evaluate whether the test score effects align with the earnings-based estimates from Parts 1 and 2.

## Final Deliverables
*   All replication code (Python/Stata scripts) committed to the GitHub repository.
*   Output datasets and visualization files (e.g., CSVs, PNGs).
*   An academic practitioner note summarizing the replication findings, the implications of the state-level approximation, and the results of the extended and out-of-sample analyses.

## References
[1] Jackson, C. K., Johnson, R. C., & Persico, C. (2016). The Effects of School Spending on Educational and Economic Outcomes: Evidence from School Finance Reforms. *The Quarterly Journal of Economics*, 131(1), 157–218. https://academic.oup.com/qje/article/131/1/157/2461148
[2] Panel Study of Income Dynamics (PSID). Public Use Data. University of Michigan. https://simba.isr.umich.edu/data/data.aspx
[3] U.S. Census Bureau. Historical Database on Individual Government Finances (INDFIN). https://www2.census.gov/programs-surveys/gov-finances/datasets/historical/
[4] National Center for Education Statistics (NCES). Common Core of Data (CCD) F-33 School District Finance Survey. https://nces.ed.gov/ccd/files.asp
[5] Lafortune, J., Rothstein, J., & Schanzenbach, D. W. (2018). Replication data for: School Finance Reform and the Distribution of Student Achievement. openICPSR. https://www.openicpsr.org/openicpsr/project/113709/version/V1/view
[6] Reardon, S. F., et al. (2026). Stanford Education Data Archive (Version 6.0). The Educational Opportunity Project at Stanford University. https://edopportunity.org/opportunity/data/downloads/
