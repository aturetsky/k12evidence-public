#!/usr/bin/env python3
"""
Canonicalize the PDF library — Version 2.
Uses EXPLICIT source→canonical mappings, verified against actual filenames.
Each BibTeX key maps to exactly one canonical file: {key}.pdf
"""

import os
import shutil
from pathlib import Path

REPO = Path("/home/ubuntu/k12-education-research")
CONSOLIDATED = REPO / "literature/papers/consolidated"

# ============================================================
# EXPLICIT MAPPING: bibtex_key → exact source filename in consolidated/
# Verified by checking actual files present.
# ============================================================
EXPLICIT_MAP = {
    # Cluster 1: Teacher Quality
    "chetty2014a":          "chetty2014a_teacher_vam_bias.pdf",
    "chetty2014b":          "chetty2014b_teacher_vam_outcomes.pdf",
    "rivkin2005":           "rivkin2005_teachers_schools_achievement.pdf",
    "rockoff2004":          "rockoff2004_individual_teachers.pdf",
    "nye2004":              "nye2004_teacher_effects.pdf",
    "hanushek2010":         "hanushek2010_vam_generalizations.pdf",
    "goldhaber2000":        "goldhaber2000_teacher_certification.pdf",
    "kane2008":             "kane_staiger_2008_w14607.pdf",
    "blazar2018":           "blazar2018.pdf",
    "papay2015":            "papay2015_teacher_experience.pdf",
    "backes2024":           "backes2024.pdf",
    "rockoff2009":          "rockoff2009_teacher_effectiveness.pdf",
    "sims2020":             "sims2020_teacher_pd_characteristics.pdf",
    "hanushek2011":         "hanushek2011",   # MISSING — no distinct file found
    # Cluster 2: Early Childhood
    "heckman2010":          "heckman_etal_2010_perry_roi.pdf",
    "garca2022":            "garcia_heckman_ronda_2022_w30004.pdf",
    "campbell2014":         "campbell2014",   # MISSING
    "deming2009":           "deming2009.pdf",
    "puma2010":             "puma2010_head_start_impact.pdf",
    "lipsey2018":           "lipsey2018",     # MISSING
    "pages2020":            "pages2020.pdf",
    "cascio2013":           "cascio2013.pdf",
    "bailey2021":           "bailey2021_bailey_2021.pdf",
    "graylobe2021":         "graylobe2021.pdf",
    # Cluster 3: Class Size
    "krueger1999":          "krueger1999_star_experiment.pdf",
    "fredriksson2013":      "fredriksson2013.pdf",
    "jepsen2009":           "jepsen_rivkin_2009_class_size_reduction_achievement.pdf",
    "wmann2006":            "wossmann_west_2006_class_size_effects_international.pdf",
    # Cluster 4: School Funding
    "jackson2016":          "jackson_johnson_persico_2016_w20847.pdf",
    "lafortune2018":        "lafortune_rothstein_schanzenbach_2018_w22011.pdf",
    "card1992":             "card1992.pdf",
    "greenwald1996":        "greenwald_hedges_laine_1996_effect_school_resources.pdf",
    "greenwald1996b":       "greenwald_hedges_laine_1996_rejoinder_hanushek.pdf",
    "hanushek1997":         "hanushek_1997_assessing_effects_school_resources.pdf",
    "hanushek2003":         "hanushek2003",   # MISSING — need separate file
    "morgan2016":           "morgan2016_no_effect_resources.pdf",
    "hyman2017":            "hyman_2017_does_money_matter_long_run.pdf",
    "neilson2014":          "neilson2014.pdf",
    # Cluster 5: Charter/Vouchers
    "hoxby2009":            "hoxby2009_Hoxby_Murarka_2009_charter_nyc.pdf",
    "angrist2013":          "angrist2013.pdf",
    "abdulkadirolu2018":    "abdulkadirolu2018",  # MISSING — need separate file
    "abdulkadiroglu2011":   "abdulkadiroglu_etal_2011_w17332.pdf",
    "dobbie2011":           "dobbie2011.pdf",
    "rouse1998":            "rouse1998_private_school_vouchers.pdf",
    "howell2002":           "howell2002",     # MISSING
    "walters2018":          "walters2018.pdf",
    "cohodes2021":          "cohodes_setren_walters_2021_can_successful_schools.pdf",
    "credostanford2015":    "credostanford2015_CREDO_2015_urban_charter.pdf",
    "fryer2014":            "fryer2014_Fryer_2014_charter_best_practices.pdf",
    # Cluster 6: Reading
    "ehri2001":             "ehri2001.pdf",
    "castles2018":          "castles2018",    # MISSING
    "shanahan2010":         "shanahan2010.pdf",
    "kjeldsen2014":         "kjeldsen2014",   # MISSING
    "kim2006":              "kim2006_summer_reading_intervention.pdf",
    "hanford2018":          "hanford2018",    # MISSING
    "may2016":              "may2016",        # MISSING
    "may2023":              "may_etal_2023_reading_recovery_rct.pdf",
    # Cluster 7: Tutoring
    "nickow2020":           "nickow2020_Nickow_Oreopoulos_Quan_2020.pdf",
    "nickow2024":           "nickow_oreopoulos_quan_2023_w27476.pdf",
    "cohen1982":            "cohen_kulik_kulik_1982_educational_outcomes_tutoring.pdf",
    "kraft2021":            "kraft_falken_2021_blueprint_tutoring.pdf",
    "kraft2025":            "kraft_lovison_2025_tutoring_group_size.pdf",
    "bhatt2024":            "bhatt2024.pdf",
    # Cluster 8: SEL/Noncognitive
    "durlak2011":           "durlak2011",     # MISSING
    "duckworth2007":        "duckworth_peterson_matthews_kelly_2007_grit.pdf",
    "duckworth2009":        "duckworth2009",  # MISSING — need separate file from 2007
    "sisk2018":             "sisk2018_growth_mindsets.pdf",
    "cred2017":             "crede_tynan_harms_2017_much_ado_about_grit.pdf",
    "yeager2016":           "yeager2016_growth_mindset_rct.pdf",
    "yeager2020":           "yeager2020_growth_mindset_controversies.pdf",
    "yeager2021":           "yeager2021_teacher_mindsets.pdf",
    "wang2020":             "wang2020_classroom_climate_wellbeing.pdf",
    "darlinghammondcook2018": "darlinghammond2018.pdf",
    "jones2019":            "jones2019_Jones_2019_SEL_evidence.pdf",
    "osher2020":            "osher2020_drivers_human_development.pdf",
    # Cluster 9: Out-of-School
    "coleman1966":          "coleman_1966_equality_of_educational_opportunity_coleman.pdf",
    "reardon2011":          "reardon2011_schools_inequality.pdf",
    "alexander2007":        "alexander_entwisle_olson_2007_lasting_consequences_summer.pdf",
    "morrissey2017":        "morrissey_vinopal_2018_neighborhood_poverty_academic_skills.pdf",
    "borman2010":           "borman_dowling_2010_schools_inequality_coleman.pdf",
    "wolf2017":             "wolf_magnuson_kimbro_2017_family_neighborhood_poverty.pdf",
    "benner2016":           "benner_boyle_sadler_2016_parental_involvement_adolescents.pdf",
    "goldhaber2022":        "goldhaber2022_Goldhaber_etal_2022_remote_hybrid_pandemic.pdf",
    "bacherhicks2019":      "bacherhicks2019.pdf",
    "clark2020":            "clark2020_covid_online_learning.pdf",
    "scherer2019":          "scherer2019_ses_ict_literacy.pdf",
    "tan2020":              "tan2020_intensive_parenting.pdf",
    "rodriguez2018":        "rodriguez2018",  # MISSING
    "guryan2023":           "guryan2023_Guryan_etal_2023_not_too_late.pdf",
    # Cluster 10: International
    "mourshed2010":         "mourshed2010",   # MISSING
    "sahlberg2020":         "sahlberg2020_distributed_leadership.pdf",
    "harris2017":           "harris2017_learning_organizations.pdf",
    "wilson2001":           "wilson2001_connecticut_teaching_policy.pdf",
    "hanushek2015":         "hanushek2015",   # MISSING — need separate file
    # Cross-cutting / Methodology
    "greenberg2009":        "greenberg2009",  # MISSING
    "sims2023":             "sims2023",       # MISSING
    "porter2022":           "porter2022",     # MISSING
    "levin1997":            "levin_1997_raising_school_productivity_x_efficiency.pdf",
    "wei2012":              "wei2012_professional_learning.pdf",
    "campbell2021":         "campbell2021_professional_learning.pdf",
    "koedel2009":           "koedel2009_value_added_ceiling.pdf",
    "wodtke2026":           "wodtke_white_zhou_2026_school_factors.pdf",
    "darlinghammond2010":   "darlinghammond2010",  # MISSING — need separate file
    "cook2015":             "cook2015_Cook_etal_2015_not_too_late.pdf",
    "jackson2018b":         "jackson2018b_test_scores_miss.pdf",
    "rothstein2009":        "rothstein_2009_efp.pdf",
    "rothstein2010":        "rothstein_2010_qje.pdf",
    "rothstein2016":        "rothstein_2016_revisiting_impacts_teachers.pdf",
    "chetty2011":           "chetty_etal_2011_star_peers_w16485.pdf",
    "heckman2006":          "heckman_2006_the_effects_of_cognitive_and.pdf",
}

# ============================================================
# STEP 1: Delete all previously created bad canonical files
# (files named exactly {key}.pdf that were created by the previous script)
# ============================================================
deleted = []
for key in EXPLICIT_MAP.keys():
    canonical = CONSOLIDATED / f"{key}.pdf"
    if canonical.exists():
        canonical.unlink()
        deleted.append(f"{key}.pdf")

print(f"Deleted {len(deleted)} previously created canonical files (cleaning up bad copies)")

# ============================================================
# STEP 2: Create correct canonical files from verified sources
# ============================================================
found = {}
missing = []

for key, source_name in EXPLICIT_MAP.items():
    canonical = CONSOLIDATED / f"{key}.pdf"
    
    # Skip if marked as MISSING
    if not source_name.endswith(".pdf"):
        missing.append(key)
        continue
    
    source = CONSOLIDATED / source_name
    if source.exists():
        shutil.copy2(source, canonical)
        found[key] = source_name
    else:
        # Try to find it elsewhere in the repo
        matches = list(REPO.rglob(source_name))
        if matches:
            shutil.copy2(matches[0], canonical)
            found[key] = str(matches[0])
        else:
            missing.append(key)

print(f"\nCreated {len(found)} canonical files")
print(f"Still missing: {len(missing)}")
print("\nMissing keys:")
for k in sorted(missing):
    print(f"  {k}")

# ============================================================
# STEP 3: Verify canonical files exist and have reasonable sizes
# ============================================================
print("\n=== CANONICAL FILE VERIFICATION ===")
bad_files = []
for key in EXPLICIT_MAP.keys():
    canonical = CONSOLIDATED / f"{key}.pdf"
    if canonical.exists():
        size = canonical.stat().st_size
        if size < 50000:  # Less than 50KB is suspicious
            bad_files.append(f"  WARNING: {key}.pdf is only {size//1024}KB — may be corrupt/wrong")
    else:
        if key not in missing:
            bad_files.append(f"  ERROR: {key}.pdf should exist but doesn't")

if bad_files:
    print("Potential issues:")
    for b in bad_files:
        print(b)
else:
    print("All canonical files look OK (size > 50KB)")

# ============================================================
# STEP 4: Write still_missing.md with Google Scholar search terms
# ============================================================
SEARCH_TERMS = {
    "castles2018":      '"Ending the Reading Wars" Castles Rastle Nation 2018 Psychological Science in the Public Interest',
    "durlak2011":       '"The Impact of Enhancing Students Social and Emotional Learning" Durlak Weissberg 2011 Child Development',
    "greenberg2009":    '"How Citation Distortions Create Unfounded Authority" Greenberg BMJ 2009',
    "hanford2018":      '"Hard Words Why Arent Kids Being Taught to Read" Hanford APM Reports 2018',
    "howell2002":       '"School Vouchers and Academic Performance" Howell Peterson Wolf Campbell 2002',
    "kjeldsen2014":     '"Gains from Training in Phonological Awareness in Kindergarten" Kjeldsen 2014',
    "lipsey2018":       '"Translating the Statistical Representation of the Effects of Education Interventions" Lipsey 2018',
    "may2016":          '"Reading Recovery Evaluation i3 Scale-Up" May Sirinides 2016 CPRE',
    "mourshed2010":     '"How the Worlds Most Improved School Systems Keep Getting Better" McKinsey Mourshed Chijioke Barber 2010',
    "porter2022":       '"Implementing the Every Student Succeeds Act" Porter Fusarelli 2022',
    "rodriguez2018":    '"Family Socioeconomic Status and Children Academic Achievement" Rodriguez 2018',
    "sims2023":         '"Quantifying Promising Trials Bias in Randomized Controlled Trials" Sims 2023',
    "hanushek2011":     '"The Economic Value of Higher Teacher Quality" Hanushek 2011 Economics of Education Review',
    "hanushek2003":     '"The Failure of Input-Based Schooling Policies" Hanushek 2003 Economic Journal',
    "abdulkadirolu2018": '"Research Design Meets Market Design" Abdulkadiroglu Angrist Hull Pathak 2016 American Economic Review',
    "darlinghammond2010": '"The Flat World and Education" Darling-Hammond 2010 Teachers College Press',
    "campbell2014":     '"The Abecedarian Project" Campbell Ramey Pungello Sparling 2014',
    "duckworth2009":    '"Development and Validation of the Short Grit Scale" Duckworth Quinn 2009 Journal of Personality Assessment',
    "hanushek2015":     '"The Knowledge Capital of Nations" Hanushek Woessmann 2015 MIT Press',
}

missing_path = REPO / "literature" / "still_missing.md"
with open(missing_path, "w") as f:
    f.write("# Papers Still Missing — Canonical Audit v2\n\n")
    f.write(f"**{len(missing)} papers** still need PDFs.\n\n")
    if missing:
        f.write("| BibTeX Key | Google Scholar Search Term |\n")
        f.write("|---|---|\n")
        for k in sorted(missing):
            search = SEARCH_TERMS.get(k, f'"{k}" K-12 education research')
            f.write(f"| `{k}` | {search} |\n")
    else:
        f.write("**All papers confirmed present. Library is complete.**\n")

print(f"\nWrote: literature/still_missing.md")
print(f"\n=== SUMMARY ===")
print(f"Total BibTeX keys:        {len(EXPLICIT_MAP)}")
print(f"Canonical PDFs created:   {len(found)}")
print(f"Still missing:            {len(missing)}")
