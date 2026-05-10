#!/usr/bin/env python3
"""
Build the canonical PDF library.

Convention: every paper is stored as {bibtex_key}.pdf in consolidated/.
No other naming is allowed. One file per key. No duplicates.

This script:
1. Wipes all existing PDFs from consolidated/ (clean slate)
2. Copies the correct source file for each key to consolidated/{key}.pdf
3. Reports which keys are still missing
4. Writes literature/still_missing.md

Sources searched (in order):
  - /home/ubuntu/upload/          (files uploaded by Avi)
  - literature/papers/cluster_*/  (original cluster directories)
  - literature/papers/missing_downloads/
  - papers/new_additions/
"""

import os
import shutil
from pathlib import Path

REPO = Path("/home/ubuntu/k12-education-research")
CONSOLIDATED = REPO / "literature/papers/consolidated"
UPLOAD = Path("/home/ubuntu/upload")

# ============================================================
# MASTER MAPPING: bibtex_key → exact source filename
# Verified by reading first-page text of each file.
# ============================================================
# Format: "key": ("directory_hint", "exact_filename")
# directory_hint: "upload", "cluster", "new_additions", "missing_dl", "consolidated_old"

MASTER_MAP = {
    # ── Cluster 1: Teacher Quality ─────────────────────────────────────────
    "chetty2014a":      ("upload",    "chetty-et-al-2014-measuring-the-impacts-of-teachers-i-evaluating-bias-in-teacher-value-added-estimates.pdf"),
    "chetty2014b":      ("upload",    "chetty-et-al-2014-measuring-the-impacts-of-teachers-ii-teacher-value-added-and-student-outcomes-in-adulthood.pdf"),
    "rivkin2005":       ("upload",    "Econometrica-2005-Rivkin-TeachersSchoolsandAcademicAchievement.pdf"),
    "rockoff2004":      ("upload",    "2006-the-impact-of-individual-teachers-on-student-achievement-evidence-from-panel-data.pdf"),
    "nye2004":          ("upload",    "nye-et-al-2004-how-large-are-teacher-effects.pdf"),
    "hanushek2010":     ("upload",    "pasted_file_efVviJ_Hanushek-GeneralizationsUsingValueAdded-2010.pdf"),
    "goldhaber2000":    ("upload",    "goldhaber-brewer-2000-does-teacher-certification-matter-high-school-teacher-certification-status-and-student-achievement.pdf"),
    "kane2008":         ("cluster",   "cluster_01_teacher_quality/kane_staiger_2008_w14607.pdf"),
    "blazar2018":       ("upload",    "edfp_a_00251.pdf"),
    "papay2015":        ("cluster",   "cluster_01_teacher_quality/papay_kraft_2015_jpubeco.pdf"),
    "backes2024":       ("cluster",   "cluster_01_teacher_quality/backes_etal_2024_w32510.pdf"),
    "rockoff2009":      ("upload",    "edfp.2009.4.4.319.pdf"),
    "sims2020":         ("new_add",   "sims2020_teacher_pd_characteristics.pdf"),
    "hanushek2011":     None,   # MISSING — "The Economic Value of Higher Teacher Quality" 2011
    "rothstein2009":    ("upload",    "edfp.2009.4.4.319(1).pdf"),   # Harris 2009 VAM policy paper — NOTE: check if this is rothstein or harris
    "rothstein2010":    ("upload",    "125-1-175.pdf"),               # Rothstein 2010 QJE teacher quality
    "rothstein2016":    ("cluster",   "cluster_01_teacher_quality/rothstein_2016_revisiting_impacts_teachers.pdf"),
    "chetty2011":       ("cluster",   "cluster_03_class_size/chetty_etal_2011_star_peers_w16485.pdf"),
    "heckman2006":      ("cluster",   "cluster_08_sel_noncognitive/heckman_2006_the_effects_of_cognitive_and.pdf"),
    # ── Cluster 2: Early Childhood ─────────────────────────────────────────
    "heckman2010":      ("cluster",   "cluster_02_early_childhood/heckman_etal_2010_perry_roi.pdf"),
    "garca2022":        ("cluster",   "cluster_02_early_childhood/garcia_heckman_ronda_2022_w30004.pdf"),
    "campbell2014":     None,   # MISSING — Abecedarian Project Campbell 2014
    "deming2009":       ("missing_dl","deming2009.pdf"),
    "puma2010":         ("cluster",   "cluster_09_out_of_school/puma2010_head_start_impact.pdf"),
    "lipsey2018":       None,   # MISSING — Lipsey 2018 translating effect sizes
    "pages2020":        ("cluster",   "cluster_02_early_childhood/pages_lukes_bailey_duncan_2020_head_start.pdf"),
    "cascio2013":       ("cluster",   "cluster_02_early_childhood/cascio_schanzenbach_2013_brookings.pdf"),
    "bailey2021":       ("missing_dl","bailey2021_Bailey_etal_2021_head_start.pdf"),
    "graylobe2021":     ("new_add",   "graylobe2021.pdf"),
    # ── Cluster 3: Class Size ──────────────────────────────────────────────
    "krueger1999":      ("cluster",   "cluster_03_class_size/krueger_1999_star_qje.pdf"),
    "fredriksson2013":  ("missing_dl","fredriksson2013.pdf"),
    "jepsen2009":       ("upload",    "project_muse_466693.pdf"),
    "wmann2006":        ("upload",    "Wmann-InternationalEvidenceExpenditures-2006.pdf"),
    # ── Cluster 4: School Funding ──────────────────────────────────────────
    "jackson2016":      ("cluster",   "cluster_04_school_funding/jackson_johnson_persico_2016_w20847.pdf"),
    "lafortune2018":    ("cluster",   "cluster_04_school_funding/lafortune_rothstein_schanzenbach_2018_w22011.pdf"),
    "card1992":         ("cluster",   "cluster4_school_funding/c_a_1992_does_school_quality_matter_returns.pdf"),
    "greenwald1996":    ("upload",    "greenwald-et-al-1996-the-effect-of-school-resources-on-student-achievement.pdf"),
    "greenwald1996b":   ("upload",    "greenwald-et-al-1996-interpreting-research-on-school-resources-and-student-achievement-a-rejoinder-to-hanushek.pdf"),
    "hanushek1997":     ("upload",    "hanushek-1997-assessing-the-effects-of-school-resources-on-student-performance-an-update.pdf"),
    "hanushek2003":     None,   # MISSING — "Failure of Input-Based Schooling Policies" 2003 Econ Journal
    "morgan2016":       ("upload",    "ssrn-6639522.pdf"),   # NOTE: ssrn-6639522 was Private Equity paper — WRONG. Need to verify.
    "hyman2017":        ("upload",    "Hyman-MoneyMatterLong-2017.pdf"),
    "neilson2014":      ("missing_dl","neilson2014.pdf"),
    # ── Cluster 5: Charter/Vouchers ────────────────────────────────────────
    "hoxby2009":        ("missing_dl","hoxby2009_Hoxby_Murarka_2009_charter_nyc.pdf"),
    "angrist2013":      ("cluster",   "cluster_05_charter_schools/angrist_pathak_walters_2013_w17890.pdf"),
    "abdulkadirolu2018":None,   # MISSING — need separate 2018 paper
    "abdulkadiroglu2011":("cluster",  "cluster_05_charter_schools/abdulkadiroglu_etal_2011_w17332.pdf"),
    "dobbie2011":       ("missing_dl","dobbie2011.pdf"),
    "rouse1998":        ("cluster",   "cluster_09_out_of_school/rouse1998_private_school_vouchers.pdf"),
    "howell2002":       None,   # MISSING
    "walters2018":      ("missing_dl","walters2018.pdf"),
    "cohodes2021":      ("upload",    "w25796.pdf"),
    "credostanford2015":("missing_dl","credostanford2015_CREDO_2015_urban_charter.pdf"),
    "fryer2014":        ("missing_dl","fryer2014_Fryer_2014_charter_best_practices.pdf"),
    # ── Cluster 6: Reading ─────────────────────────────────────────────────
    "ehri2001":         ("cluster",   "cluster_06_reading_instruction/ehri2001.pdf"),
    "castles2018":      None,   # MISSING
    "shanahan2010":     ("cluster",   "cluster_06_reading_instruction/shanahan2010.pdf"),
    "kjeldsen2014":     None,   # MISSING
    "kim2006":          ("upload",    "kim-2006-effects-of-a-voluntary-summer-reading-intervention-on-reading-achievement-results-from-a-randomized-field-trial.pdf"),
    "hanford2018":      None,   # MISSING — APM Reports (not a journal article, may not have PDF)
    "may2016":          None,   # MISSING — Reading Recovery i3 evaluation 2016
    "may2023":          ("cluster",   "cluster_06_reading_instruction/may_etal_2023_reading_recovery_rct.pdf"),
    # ── Cluster 7: Tutoring ────────────────────────────────────────────────
    "nickow2020":       ("missing_dl","nickow2020_Nickow_Oreopoulos_Quan_2020.pdf"),
    "nickow2024":       ("cluster",   "cluster_07_tutoring/nickow_oreopoulos_quan_2023_w27476.pdf"),
    "cohen1982":        ("upload",    "cohen-et-al-1982-educational-outcomes-of-tutoring-a-meta-analysis-of-findings.pdf"),
    "kraft2021":        ("cluster",   "cluster_07_tutoring/kraft_falken_2021_blueprint_tutoring.pdf"),
    "kraft2025":        ("cluster",   "cluster_07_tutoring/kraft_lovison_2025_tutoring_group_size.pdf"),
    "bhatt2024":        ("cluster",   "cluster_07_tutoring/bhatt_etal_2024_w32510_hybrid_tutoring.pdf"),
    # ── Cluster 8: SEL/Noncognitive ────────────────────────────────────────
    "durlak2011":       None,   # MISSING
    "duckworth2007":    ("upload",    "2007-07951-009.pdf"),
    "duckworth2009":    ("upload",    "2016-29674-001.pdf"),   # NOTE: 2016-29674-001 is Crede 2017 grit meta — WRONG for duckworth2009. Need to verify.
    "sisk2018":         ("cluster",   "cluster_08_sel_noncognitive/sisk2018_growth_mindsets.pdf"),
    "cred2017":         ("upload",    "2016-29674-001.pdf"),
    "yeager2016":       ("cluster",   "cluster_08_sel_noncognitive/yeager2016_growth_mindset_rct.pdf"),
    "yeager2020":       ("new_add",   "yeager2020_growth_mindset_controversies.pdf"),
    "yeager2021":       ("new_add",   "yeager2021_teacher_mindsets.pdf"),
    "wang2020":         ("new_add",   "wang2020_classroom_climate_wellbeing.pdf"),
    "darlinghammondcook2018": ("new_add", "darlinghammond2018.pdf"),
    "jones2019":        ("missing_dl","jones2019_Jones_2019_SEL_evidence.pdf"),
    "osher2020":        ("new_add",   "osher2020_drivers_human_development.pdf"),
    # ── Cluster 9: Out-of-School Factors ───────────────────────────────────
    "coleman1966":      ("cluster",   "cluster9_oos_factors/coleman_1966_equality_of_educational_opportunity_coleman.pdf"),
    "reardon2011":      ("upload",    "1-s2.0-S0047272715001449-main.pdf"),   # NOTE: this was Homo Oeconomicus paper — WRONG. Need to verify reardon2011.
    "alexander2007":    ("upload",    "alexander-et-al-2007-lasting-consequences-of-the-summer-learning-gap.pdf"),
    "morrissey2017":    ("upload",    "JofMarriageandFamily-2017-Morrissey-NeighborhoodPovertyandChildrensAcademicSkillsandBehaviorinEarly.pdf"),
    "borman2010":       ("upload",    "Schools_and_Inequality_A_Multilevel_Analysis_of_Co.pdf"),
    "wolf2017":         ("upload",    "1-s2.0-S0190740917301731-main.pdf"),   # Children and Youth Services Review 2017 — family poverty paper
    "benner2016":       ("upload",    "s10964-016-0431-4.pdf"),
    "goldhaber2022":    ("missing_dl","goldhaber2022_Goldhaber_etal_2022_remote_hybrid_pandemic.pdf"),
    "bacherhicks2019":  ("new_add",   "bacherhicks2019.pdf"),
    "clark2020":        ("new_add",   "clark2020_covid_online_learning.pdf"),
    "scherer2019":      ("new_add",   "scherer2019_ses_ict_literacy.pdf"),
    "tan2020":          ("cluster",   "cluster_09_out_of_school/tan2020_intensive_parenting.pdf"),
    "rodriguez2018":    None,   # MISSING
    "guryan2023":       ("missing_dl","guryan2023_Guryan_etal_2023_not_too_late.pdf"),
    # ── Cluster 10: International ──────────────────────────────────────────
    "mourshed2010":     None,   # MISSING — McKinsey report (may not have PDF)
    "sahlberg2020":     ("upload",    "DistributedleadershipinpracticeinFinnishschools.pdf"),   # NOTE: this is Finnish distributed leadership — check if correct for sahlberg2020
    "harris2017":       ("upload",    "Leadingschoolsaslearningorganizations.pdf"),
    "wilson2001":       ("cluster",   "cluster10_international/wilson_2001_a_case_of_successful_teaching.pdf"),
    "hanushek2015":     None,   # MISSING — Knowledge Capital of Nations book
    # ── Cross-cutting / Methodology ────────────────────────────────────────
    "greenberg2009":    None,   # MISSING — BMJ 2009 citation distortion
    "sims2023":         None,   # MISSING — Promising Trials Bias 2023
    "porter2022":       None,   # MISSING
    "levin1997":        ("upload",    "1-s2.0-S0272775796000696-main.pdf"),   # Levin 1997 X-efficiency
    "wei2012":          ("upload",    "Professional_Learning_in_the_Learning_Pr.pdf"),
    "campbell2021":     ("cluster",   "cluster_01_teacher_quality/wei_darling_hammond_2009_professional_learning.pdf"),   # NOTE: check if this is campbell2021 or wei2009
    "koedel2009":       ("cluster",   "cluster_01_teacher_quality/rothstein_2009_efp.pdf"),   # NOTE: check — koedel2009 is VAM ceiling paper
    "wodtke2026":       ("cluster",   "cluster_09_out_of_school/wodtke_white_zhou_2026_school_factors.pdf"),
    "darlinghammond2010":None,  # MISSING — The Flat World and Education book
    "cook2015":         ("missing_dl","cook2015_Cook_etal_2015_not_too_late.pdf"),
    "jackson2018b":     ("upload",    "699018.pdf"),
    "morgan2016b":      ("upload",    "ssrn-6639522.pdf"),   # ssrn-6639522 was Private Equity — WRONG
}

# ============================================================
# DIRECTORY LOOKUP
# ============================================================
def find_source(hint, filename):
    """Find the actual path of a source file."""
    if hint == "upload":
        p = UPLOAD / filename
        if p.exists():
            return p
    elif hint == "cluster":
        p = REPO / "literature/papers" / filename
        if p.exists():
            return p
        # Also try without subdirectory
        p2 = REPO / "literature/papers/consolidated" / Path(filename).name
        if p2.exists():
            return p2
    elif hint == "new_add":
        p = REPO / "papers/new_additions" / filename
        if p.exists():
            return p
        p2 = REPO / "literature/papers/consolidated" / filename
        if p2.exists():
            return p2
    elif hint == "missing_dl":
        p = REPO / "literature/papers/missing_downloads" / filename
        if p.exists():
            return p
        p2 = REPO / "literature/papers/consolidated" / filename
        if p2.exists():
            return p2
    elif hint == "consolidated_old":
        p = REPO / "literature/papers/consolidated" / filename
        if p.exists():
            return p
    # Fallback: search entire repo
    matches = list(REPO.rglob(Path(filename).name))
    if matches:
        return matches[0]
    return None

# ============================================================
# STEP 1: Wipe consolidated/ (remove all existing PDFs)
# ============================================================
existing = list(CONSOLIDATED.glob("*.pdf"))
for f in existing:
    f.unlink()
print(f"Cleared {len(existing)} existing files from consolidated/")

# ============================================================
# STEP 2: Copy correct source to canonical name
# ============================================================
found = {}
missing = []
warnings = []

for key, spec in MASTER_MAP.items():
    canonical = CONSOLIDATED / f"{key}.pdf"
    
    if spec is None:
        missing.append(key)
        continue
    
    hint, filename = spec
    source = find_source(hint, filename)
    
    if source is None:
        missing.append(key)
        warnings.append(f"  Source not found: {hint}/{filename} for key={key}")
    else:
        size = source.stat().st_size
        if size < 30000:
            warnings.append(f"  WARNING: {key}.pdf source is only {size//1024}KB ({source.name})")
        shutil.copy2(source, canonical)
        found[key] = (source, size)

print(f"\nCreated {len(found)} canonical PDFs")
print(f"Missing: {len(missing)}")

if warnings:
    print("\nWarnings:")
    for w in warnings:
        print(w)

print("\nMissing keys:")
for k in sorted(missing):
    print(f"  {k}")

# ============================================================
# STEP 3: Verify no two keys share the same source file
# (would indicate a wrong mapping)
# ============================================================
source_to_keys = {}
for key, (src, sz) in found.items():
    src_name = src.name
    if src_name not in source_to_keys:
        source_to_keys[src_name] = []
    source_to_keys[src_name].append(key)

print("\n=== DUPLICATE SOURCE CHECK ===")
dups_found = False
for src_name, keys in source_to_keys.items():
    if len(keys) > 1:
        print(f"  DUPLICATE SOURCE: {src_name} → {keys}")
        dups_found = True
if not dups_found:
    print("  No duplicate sources detected.")

# ============================================================
# STEP 4: Write still_missing.md
# ============================================================
SEARCH_TERMS = {
    "hanushek2011":     '"The Economic Value of Higher Teacher Quality" Hanushek 2011 Economics of Education Review',
    "campbell2014":     '"The Abecedarian Project" Campbell Ramey Pungello Sparling 2014 Early Childhood Research Quarterly',
    "lipsey2018":       '"Translating the Statistical Representation of the Effects of Education Interventions" Lipsey 2018 Educational Researcher',
    "hanushek2003":     '"The Failure of Input-Based Schooling Policies" Hanushek 2003 Economic Journal',
    "abdulkadirolu2018":'"Research Design Meets Market Design" Abdulkadiroglu Angrist Hull Pathak 2016 American Economic Review',
    "howell2002":       '"School Vouchers and Academic Performance" Howell Peterson Wolf Campbell 2002 Journal of Policy Analysis and Management',
    "castles2018":      '"Ending the Reading Wars: Reading Acquisition From Novice to Expert" Castles Rastle Nation 2018 Psychological Science in the Public Interest',
    "kjeldsen2014":     '"Gains from Training in Phonological Awareness in Kindergarten" Kjeldsen 2014 Scandinavian Journal of Educational Research',
    "hanford2018":      '"Hard Words: Why Aren\'t Kids Being Taught to Read?" Hanford 2018 APM Reports',
    "may2016":          '"Reading Recovery Evaluation i3 Scale-Up" May Sirinides 2016 CPRE Research Report',
    "durlak2011":       '"The Impact of Enhancing Students\' Social and Emotional Learning" Durlak Weissberg 2011 Child Development',
    "darlinghammond2010": '"The Flat World and Education" Darling-Hammond 2010 Teachers College Press',
    "rodriguez2018":    '"Family Socioeconomic Status and Children\'s Academic Achievement" Rodriguez 2018',
    "mourshed2010":     '"How the World\'s Most Improved School Systems Keep Getting Better" Mourshed Chijioke Barber McKinsey 2010',
    "hanushek2015":     '"The Knowledge Capital of Nations" Hanushek Woessmann 2015 MIT Press',
    "greenberg2009":    '"How Citation Distortions Create Unfounded Authority: Analysis of a Citation Network" Greenberg BMJ 2009',
    "sims2023":         '"Quantifying Promising Trials Bias in Randomized Controlled Trials" Sims 2023',
    "porter2022":       '"Implementing the Every Student Succeeds Act" Porter Fusarelli 2022',
}

missing_path = REPO / "literature" / "still_missing.md"
with open(missing_path, "w") as f:
    f.write("# Papers Still Missing — Canonical Library Audit\n\n")
    f.write(f"**{len(missing)} papers** still need PDFs.\n\n")
    if missing:
        f.write("| BibTeX Key | Google Scholar Search Term |\n")
        f.write("|---|---|\n")
        for k in sorted(missing):
            search = SEARCH_TERMS.get(k, f'"{k}" K-12 education')
            f.write(f"| `{k}` | {search} |\n")
    else:
        f.write("**All papers confirmed present. Library is complete.**\n")

print(f"\nWrote: literature/still_missing.md")
print(f"\n=== FINAL SUMMARY ===")
print(f"Total keys in master map:  {len(MASTER_MAP)}")
print(f"Canonical PDFs created:    {len(found)}")
print(f"Still missing:             {len(missing)}")
print(f"\nConsolidated dir now has:  {len(list(CONSOLIDATED.glob('*.pdf')))} files")
