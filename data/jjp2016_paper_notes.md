# JJP (2016) Paper Notes — Jackson, Johnson & Persico (2016)
## "The Effects of School Spending on Educational and Economic Outcomes: Evidence from School Finance Reforms"
## QJE 131(1): 157–218 (NBER WP 20847, January 2015)

---

## Abstract / Key Findings
- Data: PSID children born 1955–1985, followed through 2011
- Instrument: timing of court-mandated school finance reforms (SFRs) + type of funding formula
- Main results (10% increase in per-pupil spending for all 12 years of public school):
  - +0.27 more completed years of education
  - +7.25% higher wages
  - −3.67 pp reduction in annual incidence of adult poverty
- Effects much larger for low-income children:
  - +0.43 years of completed education
  - +9.5% higher earnings
  - −6.8 pp reduction in poverty
- A 25% spending increase over all school-age years sufficient to eliminate attainment gaps between low- and high-income families
- Mechanism: reductions in student-to-teacher ratios, increases in teacher salaries, longer school years

---

## Data Sources
1. **PSID** — Panel Study of Income Dynamics (restricted-use geocode data + public use)
   - Cohorts: born ~1955–1985
   - Outcomes: educational attainment, wages, adult poverty
2. **CCD** — Common Core of Data (NCES): district-level per-pupil spending
3. **Court-ordered SFR timing data** — from JJP (2014a) / appendix
4. **Type of funding formula** — equity vs. adequacy reforms

---

## Identification Strategy
- Quasi-experimental: court-mandated SFRs as instrument for per-pupil spending
- Two-stage approach:
  1. Predict district spending change based on reform timing + type + experiences of similar districts in other states
  2. Compare "treated" cohorts (young enough to be in school during/after reform) vs. "untreated" cohorts
- Controls for: state FE, birth-year FE, district FE, family background characteristics

---

## Tables to Replicate
- **Table 2**: First-stage estimates — effect of SFRs on per-pupil spending
- **Table 3**: Reduced-form estimates — effect of SFRs on adult outcomes
- **Table 5**: IV estimates — effect of per-pupil spending on adult outcomes (main results)

---

## Pages Read
- Pages 1–5 (cover, abstract, introduction pp. 1–3)

---

## Table 1 — Descriptive Statistics (p. 59 of PDF)

All PSID individuals born 1955–1985, N=15,353 from 1,409 school districts (1,031 child counties, 50 states).

| Variable | All (N=15,353) | Low-income (N=9,035) | Non-Poor (N=6,318) |
|---|---|---|---|
| High School Graduate | 0.86 | 0.79 | 0.92 |
| Years of Education | 13.18 | 12.63 | 13.64 |
| Ln(Wages) at age 30 | 2.51 | 2.36 | 2.61 |
| Adult Family Income at age 30 | $49,308 | $35,212 | $55,324 |
| In Poverty at age 30 | 0.08 | 0.13 | 0.04 |
| Per-pupil Spending (avg., ages 5-17) | $4,463 | $4,436 | $4,486 |
| Any Court-ordered SFR, age 5-17 | 0.53 | 0.53 | 0.53 |
| Years of Exposure to SFR, age 5-17 | 4.35 | 4.46 | 4.27 |

---

## Table 2 — Effect of Endogenous and Exogenous Spending on Predicted Outcomes and School Resources (p. 60)

Validates instrument: OLS spending is correlated with SES; IV spending is not.

Key results for low-income children (N=9,035):
- OLS: Spending(age 5-17) → Prob(HS Grad): 0.0164*** (0.0022); Ln(wage): 0.0358*** (0.0043)
- OLS with district FE: Spending → Prob(HS Grad): −0.0044** (0.0019); Ln(wage): −0.0069+ (0.0048)
- 2SLS/IV with district FE: Spending → Pupil-Teacher Ratio: −0.8266** (0.3313)
- 2SLS/IV: ln(Spending) → Pupil-Teacher Ratio: −3.6331** (1.5166)

---

## Table 3 — OLS vs 2SLS Estimates: Effect on Educational Attainment by Childhood Poverty Status (p. 61)

N=15,353 individuals, 4,586 families, 1,409 school districts.

| Specification | Outcome | Estimator | Coefficient | SE |
|---|---|---|---|---|
| Pooled | Years of Education | OLS | −0.0763 | (0.1474) |
| Pooled | Years of Education | 2SLS | 2.7289** | (1.2155) |
| Pooled | Prob(HS Grad) | OLS | 0.0216 | (0.0278) |
| Pooled | Prob(HS Grad) | 2SLS | 0.9523*** | (0.2898) |
| Low-income | Years of Education | 2SLS | 4.3548** | (1.8165) |
| Low-income | Prob(HS Grad) | 2SLS | 1.1948*** | (0.4408) |
| Non-Poor | Years of Education | 2SLS | 0.7564 | (1.9200) |
| Non-Poor | Prob(HS Grad) | 2SLS | 0.6208* | (0.3538) |

---

## Table 4 — OLS vs 2SLS Estimates: Effect on Long-Run Economic Outcomes (p. 62)

N varies: 106,545–151,756 person-year observations; 13,183–14,737 individuals.

| Outcome | Estimator | Specification | Coefficient | SE |
|---|---|---|---|---|
| Ln(Wage) | OLS | Pooled | −0.0504 | (0.0511) |
| Ln(Wage) | 2SLS | Pooled | 0.7257*** | (0.2637) |
| Ln(Wage) | 2SLS | Low-income | 0.9535** | (0.4434) |
| Ln(Wage) | 2SLS | Non-Poor | 0.4333 | (0.3575) |
| Ln(Family Income) | 2SLS | Pooled | 0.9678** | (0.3993) |
| Ln(Family Income) | 2SLS | Low-income | 1.6408*** | (0.6186) |
| Prob(Poverty) | 2SLS | Pooled | −0.3671*** | (0.1281) |
| Prob(Poverty) | 2SLS | Low-income | −0.6856*** | (0.2103) |

---

## Table 5 — Effect Using Only a Single Year of Earnings Data (p. 63)

Tests robustness of earnings estimates to single cross-section vs. panel.

| Survey Year | Ln(Spending) Coefficient | SE |
|---|---|---|
| 2001 only | 0.3699 | (1.001) |
| 2010 only | 0.5014 | (1.1368) |
| All years (panel) | **0.7257*** | **(0.2637)** |

All first-stage F-statistics above 100.

---

## Key Regression Equations

### First Stage (instrument construction):
- Predicted spending change based on: timing of court-ordered reform × type of reform × 1967 within-state district income percentile
- Exposure = years of school age (5–17) spent in post-reform period

### Second Stage (main IV):
- Outcome_i = α + β·ln(Spending_i) + γ·X_i + δ_d + λ_t + ε_i
- Where: δ_d = school district FE, λ_t = race × birth-year FE
- Controls: county desegregation timing × race, War on Poverty rollout, 1960 county characteristics × linear cohort trends, family background

### Instrument:
- Z_i = (years of exposure to SFR, ages 5–17) × (predicted district spending change from reform)
- Predicted spending change = spending change experienced by similar districts in other states after their court-ordered reform

---

## Pages Read
- Pages 1–5 (abstract, introduction)
- Pages 56–65 (Figures 11–15, Tables 1–5)
- Still to read: pages 6–55 (data section, empirical strategy, main results text)

---

## Appendix A — Court-Ordered Reform Timing Data (pp. 68–70)

Table A1 lists all Supreme Court rulings on school finance system constitutionality from 1967–2010, by state. This is the primary source for the reform timing instrument. Key observations:

- States with NO court-ordered reforms: Colorado, Delaware, Florida, Georgia, Hawaii, Illinois, Indiana, Iowa, Louisiana, Maine, Minnesota, Mississippi, Nebraska, Nevada, North Dakota, Oklahoma, Pennsylvania, Rhode Island, South Dakota, Utah, Virginia
- States with first reform in 1970s: California (1971), New Jersey (1973), Kansas (1972), Washington (1977), West Virginia (1979), Wyoming (1980)
- States with first reform in 1980s: Arkansas (1983), Texas (1989), Kentucky (1989), Montana (1989)
- States with first reform in 1990s: New Hampshire (1993), Massachusetts (1993), Missouri (1993), Tennessee (1993), North Carolina (1997), Michigan (1997), Ohio (1997), Vermont (1997), New Mexico (1998)
- States with first reform in 2000s: New York (2003), Maryland (2005), South Carolina (2005), Oregon (2009)

This table can be digitized directly as the reform timing dataset.

---

## Appendix B — Data Coverage (pp. 71–73)

**Spending data sources:**
1. **INDFIN** (Historical Database on Individual Government Finances): annual data 1967–1991 from Census of Governments + National Archives + Individual Government Finances Survey
2. **CCD** (Common Core of Data) School District Finance Survey (F-33): annual from 1992–2010 (NCES)

Combined panel: annual per-pupil spending for each school district, 1967–2010.

**Coverage gaps:** Data missing for 1968–1969 (all states); sparse coverage 1967–1978 (~40% of districts); near-complete coverage after 1979.

**Key data construction notes:**
- Spending deflated to real 2000 dollars using CPI-U
- Missing years filled by linear interpolation (1–2 year gaps only)
- States missing pre-1992 data: Alaska, Hawaii, Maryland, NC, Virginia, DC

---

## Summary: What We Need to Replicate

### Tables 2, 3, and 5 require:

**Table 2** (Endogenous vs. exogenous spending, instrument validity):
- PSID geocode data, low-income subsample (N=9,035)
- Per-pupil spending from INDFIN+CCD, matched to childhood school district
- Predicted earnings index from family/county SES characteristics
- School district FE, birth-year FE
- 2SLS instrument: SFR timing × predicted spending change

**Table 3** (IV estimates, educational attainment):
- Full PSID sample (N=15,353), born 1955–1985
- Outcomes: years of education, Prob(HS grad)
- Same IV design, with poverty status interaction

**Table 5** (Robustness: single-year vs. panel wages):
- PSID wage data from 2001 only, 2010 only, and all years
- Outcome: Ln(wages) at age 30
- Same IV design

### Data required:
1. PSID restricted geocode data (matched to school district) — **requires application to PSID**
2. INDFIN spending data 1967–1991 — available from Census Bureau
3. CCD F-33 spending data 1992–2010 — available from NCES
4. Court-ordered reform timing — can be digitized from Table A1 in paper
5. County-level controls (1960 census, desegregation timing, War on Poverty rollout)

### Critical constraint:
The PSID restricted-use geocode file (which links individuals to school districts) requires a formal data use agreement with the University of Michigan. The public-use PSID only identifies state of residence, not school district. **This is the binding data constraint for exact replication.**

---

## Data Availability Assessment (Phase 3 Findings)

### 1. PSID — Panel Study of Income Dynamics

**Public-use data**: Freely available after registration at https://simba.isr.umich.edu/data/data.aspx. Provides individual-level data on income, education, wages, and family background. Identifies state of residence but NOT school district.

**Restricted geocode data**: Requires formal Data Use Agreement with University of Michigan (PSIDhelp@umich.edu). This file links individuals to their childhood school district (LEAID). **This is the binding constraint for exact replication of Tables 2, 3, and 5.**

**Implication for replication**: Without the restricted geocode file, we cannot match PSID individuals to their specific school district and thus cannot compute their exposure to school finance reforms or their average per-pupil spending during childhood. The public-use PSID only identifies state, not district.

**Feasible alternative**: Use state-level variation in reform timing (rather than district-level variation) as the instrument. This is a weaker instrument but can be estimated with public-use PSID data. This is the approach used by several subsequent papers.

### 2. CCD F-33 School District Finance Data (1992–2015)

**Status**: Publicly available from NCES at https://nces.ed.gov/ccd/files.asp. Select Fiscal → District → School Year. Annual data available from 1992–2015 (and beyond). **Downloadable without restriction.**

### 3. INDFIN Historical School District Finance Data (1967–1991)

**Status**: Publicly available from Census Bureau at https://www2.census.gov/programs-surveys/gov-finances/datasets/historical/. File: `indfin school district finance data fy 1967-91.zip` (30 MB). **Downloadable without restriction.**

Also available: `_IndFin_1967-2012.zip` (250 MB) which extends through 2012.

### 4. Court-Ordered Reform Timing Data

**Source 1 — JJP Appendix Table A1**: Can be digitized directly from the paper (pp. 68–70). Lists all court-ordered SFRs by state, 1967–2010.

**Source 2 — Lafortune, Rothstein & Schanzenbach (2018)**: Replication data at openICPSR project 113709. Contains `censusofgovernments/` and `ccdfinance/` folders. The `rawdata/` folder contains CCD finance data and Census of Governments data. **Requires free openICPSR account to download.**

**Source 3 — School Finance Indicators Database (SFID)**: https://www.schoolfinancedata.org/ — public collection of K-12 school finance data.

### 5. SEDA — Stanford Education Data Archive

**Status**: Freely available at https://edopportunity.org/opportunity/data/downloads/. Version 6.0 available with district-level test scores from 2009–2019. CSV format available. **Downloadable without restriction.**

Key file for Part 3: `seda_geodist_long_cs_6.0` — district-level, long format, CS metric, disaggregated by year/grade/subject.

---

## Replication Strategy Given Data Constraints

Given that the PSID restricted geocode file requires a formal DUA application (typically 2–4 weeks), the replication will proceed as follows:

**Part 1 (In-sample replication)**: Use state-level variation in reform timing as the instrument, matched to PSID public-use data identifying state of residence. This approximates the JJP design but uses state rather than district as the unit of treatment assignment. We will clearly document this as a "state-level IV" approximation and quantify the expected attenuation relative to the district-level IV.

**Part 2 (Extended window)**: Same state-level IV design, extended to cohorts born through ~2000, with CCD spending data through 2015.

**Part 3 (SEDA robustness)**: Use SEDA district-level test scores (2009–2019) merged with CCD spending data and reform timing, without requiring PSID data at all.

**Data to download immediately**:
1. INDFIN 1967–1991 from Census Bureau (30 MB zip)
2. CCD F-33 1992–2015 from NCES (multiple files)
3. SEDA v6.0 district-level data from Stanford (CSV)
4. Lafortune 2018 replication data from openICPSR (for reform timing)
5. PSID public-use data (after registration)
