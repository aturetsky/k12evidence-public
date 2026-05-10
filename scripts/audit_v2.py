"""
Improved audit: explicit mapping of every BibTeX key to expected PDF filename fragments.
Also consolidates all PDFs from upload dir and all repo subdirs into one clean directory.
"""

import re
import shutil
from pathlib import Path

REPO = Path("/home/ubuntu/k12-education-research")
UPLOAD_DIR = Path("/home/ubuntu/upload")
CONSOLIDATED = REPO / "literature" / "papers" / "consolidated"
CONSOLIDATED.mkdir(parents=True, exist_ok=True)

# Step 1: Copy ALL PDFs from upload dir into consolidated with clean names
# Explicit mapping: bib_key -> (search_fragment_in_upload, clean_filename)
UPLOAD_TO_KEY = {
    "Professional_Learning_in_the_Learning_Pr":     ("wei2012",          "wei2012_professional_learning"),
    "1-s2.0-S0272775796000696":                     ("rouse1998",         "rouse1998_private_school_vouchers"),
    "kim-2006":                                      ("kim2006",           "kim2006_summer_reading"),
    "1-s2.0-S0190740917301731":                     ("tan2020",           "tan2020_intensive_parenting"),
    "s10964-016-0431-4":                             ("sisk2018",          "sisk2018_growth_mindsets"),
    "2007-07951-009":                               ("duckworth2007",     "duckworth2007_grit"),
    "cohen-et-al-1982":                             ("cohen1982",         "cohen1982_tutoring_meta"),
    "greenwald-et-al-1996-interpreting":            ("greenwald1996b",    "greenwald1996b_resources_rejoinder"),
    "greenwald-et-al-1996-the-effect":              ("greenwald1996",     "greenwald1996_school_resources"),
    "Schools_and_Inequality":                       ("borman2010",        "borman2010_schools_inequality"),
    "Leadingschoolsaslearningorganizations":        ("harris2017",        "harris2017_learning_organizations"),
    "JofMarriageandFamily-2017-Morrissey":          ("morrissey2017",     "morrissey2017_neighborhood_poverty"),
    "alexander-et-al-2007":                         ("alexander2007",     "alexander2007_summer_learning_gap"),
    "FGIIW_20260430":                               ("wodtke2026",        "wodtke2026_how_much_schools_matter"),
    "2016-29674-001":                               ("yeager2016",        "yeager2016_growth_mindset_rct"),
    "cohodes-et-al-2021":                           ("cohodes2021",       "cohodes2021_charter_scaling"),
    "w25796":                                       ("kraft2021",         "kraft2021_tutoring_blueprint"),
    "Hyman-MoneyMatterLong-2017":                   ("hyman2017",         "hyman2017_money_matters_long_run"),
    "POL2015-0249_app":                             ("papay2015",         "papay2015_teacher_experience"),
    "hanushek-1997":                                ("hanushek1997",      "hanushek1997_school_resources"),
    "Wmann-InternationalEvidenceExpenditures-2006": ("wmann2006",         "wmann2006_class_size_international"),
    "project_muse_466693":                          ("wilson2001",        "wilson2001_connecticut_teaching_policy"),
    "goldhaber-brewer-2000":                        ("goldhaber2000",     "goldhaber2000_teacher_certification"),
    "ED443782":                                     ("puma2010",          "puma2010_head_start_impact"),
    "edfp_a_00251":                                 ("koedel2009",        "koedel2009_value_added_ceiling"),
    "DistributedleadershipinpracticeinFinnishschools": ("sahlberg2020",   "sahlberg2020_distributed_leadership"),
    "nye-et-al-2004":                               ("nye2004",           "nye2004_teacher_effects"),
    "edfp.2009.4.4.319(1)":                         ("rockoff2009",       "rockoff2009_teacher_effectiveness_dup"),
    "edfp.2009.4.4.319":                            ("rockoff2009",       "rockoff2009_teacher_effectiveness"),
    "1-s2.0-S0047272715001449":                     ("jackson2016",       "jackson2016_school_spending"),
    "2006-the-impact-of-individual-teachers":       ("rockoff2004",       "rockoff2004_individual_teachers"),
    "Econometrica-2005-Rivkin":                     ("rivkin2005",        "rivkin2005_teachers_schools"),
    "699018":                                       ("jackson2018b",      "jackson2018b_test_scores_miss"),
    "125-1-175":                                    ("krueger1999",       "krueger1999_star_experiment"),
    "chetty-et-al-2014-measuring-the-impacts-of-teachers-i": ("chetty2014a", "chetty2014a_teacher_vam_bias"),
    "chetty-et-al-2014-measuring-the-impacts-of-teachers-ii": ("chetty2014b", "chetty2014b_teacher_vam_outcomes"),
    "ssrn-6639522":                                 ("morgan2016",        "morgan2016_no_effect_resources"),
    # Previously uploaded (pasted_file prefix)
    "pasted_file_HOdNYE_2020-99903-019":            ("yeager2020",        "yeager2020_growth_mindset_controversies"),
    "pasted_file_QV97zq":                           ("scherer2019",       "scherer2019_ses_ict"),
    "pasted_file_W7qNaw":                           ("clark2020",         "clark2020_covid_online"),
    "pasted_file_efVviJ_Hanushek-Generalizations":  ("hanushek2010",      "hanushek2010_vam_generalizations"),
    "pasted_file_fdDGGo_yeager-et-al-2021":         ("yeager2021",        "yeager2021_teacher_mindsets"),
    "pasted_file_ifbBlS_Drivers":                   ("osher2020",         "osher2020_drivers_human_development"),
    "pasted_file_paMQX7":                           ("wang2020",          "wang2020_classroom_climate"),
    "pasted_file_wBvxvB_Identifying":               ("sims2020",          "sims2020_teacher_pd"),
}

# Copy all uploads to consolidated with clean names
copied_keys = set()
for fragment, (bib_key, clean_name) in UPLOAD_TO_KEY.items():
    for f in UPLOAD_DIR.glob("*.pdf"):
        if fragment.lower() in f.name.lower():
            dest = CONSOLIDATED / f"{clean_name}.pdf"
            shutil.copy2(f, dest)
            copied_keys.add(bib_key)
            break

print(f"Copied {len(copied_keys)} files from uploads to consolidated dir")

# Step 2: Also copy all existing repo PDFs to consolidated
existing_count = 0
for p in REPO.rglob("*.pdf"):
    if "/upload/" not in str(p) and "/consolidated/" not in str(p):
        dest = CONSOLIDATED / p.name
        if not dest.exists():
            shutil.copy2(p, dest)
            existing_count += 1

print(f"Copied {existing_count} existing repo PDFs to consolidated dir")
print(f"Total in consolidated: {len(list(CONSOLIDATED.glob('*.pdf')))}")

# Step 3: Build explicit key->filename map for ALL 119 BibTeX entries
# This is the ground truth — every key we expect to have
ALL_KEYS_EXPECTED = {
    # Cluster 1: Teacher Quality
    "chetty2014a":      "chetty2014a",
    "chetty2014b":      "chetty2014b",
    "rivkin2005":       "rivkin2005",
    "rockoff2004":      "rockoff2004",
    "nye2004":          "nye2004",
    "hanushek2010":     "hanushek2010",
    "goldhaber2000":    "goldhaber2000",
    "kane2008":         "kane2008",
    "blazar2018":       "blazar2018",
    "papay2015":        "papay2015",
    "backes2024":       "backes2024",
    "rockoff2009":      "rockoff2009",
    "sims2020":         "sims2020",
    "hanushek2011":     "hanushek2011",
    # Cluster 2: ECE
    "heckman2010":      "heckman2010",
    "garca2022":        "garca2022",
    "campbell2014":     "campbell2014",
    "deming2009":       "deming2009",
    "puma2010":         "puma2010",
    "lipsey2018":       "lipsey2018",
    "pages2020":        "pages2020",
    "cascio2013":       "cascio2013",
    "bailey2021":       "bailey2021",
    "graylobe2021":     "graylobe2021",
    # Cluster 3: Class Size
    "krueger1999":      "krueger1999",
    "fredriksson2013":  "fredriksson2013",
    "jepsen2009":       "jepsen2009",
    "wmann2006":        "wmann2006",
    # Cluster 4: School Funding
    "jackson2016":      "jackson2016",
    "lafortune2018":    "lafortune2018",
    "card1992":         "card1992",
    "greenwald1996":    "greenwald1996",
    "greenwald1996b":   "greenwald1996b",
    "hanushek1997":     "hanushek1997",
    "hanushek2003":     "hanushek2003",
    "morgan2016":       "morgan2016",
    "hyman2017":        "hyman2017",
    "neilson2014":      "neilson2014",
    # Cluster 5: Charter/Vouchers
    "hoxby2009":        "hoxby2009",
    "angrist2013":      "angrist2013",
    "abdulkadirolu2018": "abdulkadirolu2018",
    "abdulkadiroglu2011": "abdulkadiroglu2011",
    "dobbie2011":       "dobbie2011",
    "rouse1998":        "rouse1998",
    "howell2002":       "howell2002",
    "walters2018":      "walters2018",
    "cohodes2021":      "cohodes2021",
    "credostanford2015": "credostanford2015",
    "fryer2014":        "fryer2014",
    # Cluster 6: Reading
    "ehri2001":         "ehri2001",
    "castles2018":      "castles2018",
    "shanahan2010":     "shanahan2010",
    "kjeldsen2014":     "kjeldsen2014",
    "kim2006":          "kim2006",
    "hanford2018":      "hanford2018",
    "may2016":          "may2016",
    "may2023":          "may2023",
    # Cluster 7: Tutoring
    "nickow2020":       "nickow2020",
    "nickow2024":       "nickow2024",
    "cohen1982":        "cohen1982",
    "kraft2021":        "kraft2021",
    "kraft2025":        "kraft2025",
    "bhatt2024":        "bhatt2024",
    # Cluster 8: SEL/Noncognitive
    "durlak2011":       "durlak2011",
    "duckworth2007":    "duckworth2007",
    "duckworth2009":    "duckworth2009",
    "sisk2018":         "sisk2018",
    "cred2017":         "cred2017",
    "yeager2016":       "yeager2016",
    "yeager2020":       "yeager2020",
    "yeager2021":       "yeager2021",
    "wang2020":         "wang2020",
    "darlinghammondcook2018": "darlinghammondcook2018",
    "jones2019":        "jones2019",
    "osher2020":        "osher2020",
    # Cluster 9: Out-of-School
    "coleman1966":      "coleman1966",
    "reardon2011":      "reardon2011",
    "alexander2007":    "alexander2007",
    "morrissey2017":    "morrissey2017",
    "borman2010":       "borman2010",
    "wolf2017":         "wolf2017",
    "benner2016":       "benner2016",
    "goldhaber2022":    "goldhaber2022",
    "bacherhicks2019":  "bacherhicks2019",
    "clark2020":        "clark2020",
    "scherer2019":      "scherer2019",
    "tan2020":          "tan2020",
    "rodriguez2018":    "rodriguez2018",
    "guryan2023":       "guryan2023",
    # Cluster 10: International
    "mourshed2010":     "mourshed2010",
    "sahlberg2020":     "sahlberg2020",
    "harris2017":       "harris2017",
    "wilson2001":       "wilson2001",
    "hanushek2015":     "hanushek2015",
    # Cross-cutting / Methodology
    "greenberg2009":    "greenberg2009",
    "sims2023":         "sims2023",
    "porter2022":       "porter2022",
    "levin1997":        "levin1997",
    "wei2012":          "wei2012",
    "campbell2021":     "campbell2021",
    "koedel2009":       "koedel2009",
    "wodtke2026":       "wodtke2026",
    "hanushek2003":     "hanushek2003",
    "darlinghammond2010": "darlinghammond2010",
    "cook2015":         "cook2015",
    "jackson2018b":     "jackson2018b",
}

# Check each expected key against consolidated dir
all_pdfs_in_consolidated = {p.stem.lower(): p for p in CONSOLIDATED.glob("*.pdf")}

found = []
missing = []

for key, fragment in ALL_KEYS_EXPECTED.items():
    matched = False
    for stem, path in all_pdfs_in_consolidated.items():
        if fragment.lower()[:8] in stem or key.lower()[:8] in stem:
            found.append((key, stem))
            matched = True
            break
    if not matched:
        missing.append(key)

print(f"\n=== AUDIT RESULTS ===")
print(f"Expected: {len(ALL_KEYS_EXPECTED)}")
print(f"Found: {len(found)}")
print(f"Missing: {len(missing)}")
print(f"\nMissing keys:")
for k in sorted(missing):
    print(f"  {k}")

# Save clean missing list
with open(REPO / "literature" / "still_missing_v2.md", "w") as f:
    f.write("# Papers Still Missing — Final Audit\n\n")
    f.write(f"{len(missing)} papers still need PDFs.\n\n")
    f.write("| BibTeX Key | Google Scholar Search Term |\n")
    f.write("|---|---|\n")
    
    # Map keys to search terms
    SEARCH_TERMS = {
        "kane2008": '"Estimating Teacher Impacts on Student Achievement" Kane Staiger 2008',
        "blazar2018": '"Validating Teacher Effects on Students Attitudes and Behaviors" Blazar 2018',
        "backes2024": '"Heterogeneous Impacts of Teacher Value-Added on Postsecondary Outcomes" Backes Goldhaber 2024',
        "hanushek2011": '"The Economic Value of Higher Teacher Quality" Hanushek Rivkin 2011',
        "campbell2014": '"Early Childhood Investments Substantially Boost Adult Health" Campbell 2014 Science',
        "deming2009": '"Early Childhood Intervention and Life-Cycle Skill Development" Deming 2009',
        "lipsey2018": '"Effects of the Tennessee Voluntary Prekindergarten Program" Lipsey Farran 2018',
        "pages2020": '"Revised Estimates of the Impacts of Head Start" Pages Bailey Duncan 2020',
        "cascio2013": '"The Impacts of Expanding Access to High-Quality Preschool" Cascio Schanzenbach 2013',
        "graylobe2021": '"The Long-Term Effects of Universal Preschool in Boston" Gray-Lobe 2021',
        "fredriksson2013": '"Long-Term Effects of Class Size" Fredriksson Ockert Oosterbeek 2013',
        "jepsen2009": '"Class Size Reduction and Student Achievement" Jepsen Rivkin 2009',
        "card1992": '"Does School Quality Matter? Returns to Education" Card Krueger 1992',
        "hanushek2003": '"The Failure of Input-Based Schooling Policies" Hanushek 2003',
        "neilson2014": '"The Effect of School Construction on Test Scores" Neilson Zimmerman 2014',
        "abdulkadirolu2018": '"Accountability and Flexibility in Public Schools" Abdulkadiroglu 2018',
        "abdulkadiroglu2011": '"Accountability and Flexibility in Public Schools" Abdulkadiroglu 2011',
        "dobbie2011": '"Are High-Quality Schools Enough to Increase Achievement" Dobbie Fryer 2011',
        "howell2002": '"School Vouchers and Academic Performance" Howell Peterson 2002',
        "walters2018": '"The Demand for Effective Charter Schools" Walters 2018',
        "fryer2014": '"Injecting Charter School Best Practices into Traditional Public Schools" Fryer 2014',
        "credostanford2015": '"Urban Charter School Study" CREDO Stanford 2015',
        "ehri2001": '"Systematic Phonics Instruction Helps Students Learn to Read" Ehri 2001',
        "castles2018": '"Ending the Reading Wars" Castles Rastle Nation 2018',
        "shanahan2010": '"The National Early Literacy Panel" Shanahan Lonigan 2010',
        "kjeldsen2014": '"Gains from Training in Phonological Awareness in Kindergarten" Kjeldsen 2014',
        "hanford2018": '"Hard Words Why Aren\'t Kids Being Taught to Read" Hanford 2018',
        "may2016": '"Reading Recovery Evaluation i3 Scale-Up" May Sirinides 2016',
        "may2023": '"Reading Recovery Evaluation" May Sirinides 2023',
        "nickow2020": '"The Impressive Effects of Tutoring on PreK-12 Learning" Nickow Oreopoulos 2020',
        "nickow2024": '"The Promise of Tutoring for PreK-12 Learning" Nickow Oreopoulos 2024',
        "kraft2025": '"The Effects of Tutoring Group Size on Student Learning" Kraft Lovison 2025',
        "bhatt2024": '"Scaling High-Dosage Tutoring Evidence from a Hybrid Model" Bhatt Cook Guryan 2024',
        "durlak2011": '"The Impact of Enhancing Students Social and Emotional Learning" Durlak 2011',
        "duckworth2009": '"Development and Validation of the Short Grit Scale" Duckworth Quinn 2009',
        "cred2017": '"Much Ado About Grit A Meta-Analytic Synthesis" Crede Tynan Harms 2017',
        "darlinghammondcook2018": '"Educating the Whole Child" Darling-Hammond Cook-Harvey 2018',
        "jones2019": '"The Evidence Base for How We Learn SEL" Jones Kahn 2019',
        "coleman1966": '"Equality of Educational Opportunity" Coleman 1966',
        "reardon2011": '"The Widening Academic Achievement Gap Between the Rich and the Poor" Reardon 2011',
        "wolf2017": '"Family and Neighborhood Socioeconomic Status and Cognitive Development" Wolf 2017',
        "benner2016": '"Parental Involvement and Adolescents Educational Success" Benner Boyle 2016',
        "goldhaber2022": '"Consequences of Remote and Hybrid Instruction During the Pandemic" Goldhaber 2022',
        "bacherhicks2019": '"The School to Prison Pipeline Long-Run Impacts of School Suspensions" Bacher-Hicks 2019',
        "guryan2023": '"Not Too Late Improving Academic Outcomes Among Adolescents" Guryan 2023',
        "mourshed2010": '"How the Worlds Most Improved School Systems Keep Getting Better" McKinsey 2010',
        "hanushek2015": '"The Knowledge Capital of Nations" Hanushek Woessmann 2015',
        "greenberg2009": '"How Citation Distortions Create Unfounded Authority" Greenberg BMJ 2009',
        "sims2023": '"Quantifying Promising Trials Bias in Randomized Controlled Trials" Sims 2023',
        "porter2022": '"Implementing the Every Student Succeeds Act" Porter Fusarelli 2022',
        "levin1997": '"Accelerated Schools for Disadvantaged Students" Levin 1997',
        "campbell2021": '"Developing Teachers as Professionals" Campbell 2021',
        "cook2015": '"Not Too Late Improving Academic Outcomes for Disadvantaged Youth" Cook 2015',
        "jackson2018b": '"What Do Test Scores Miss" Jackson 2018',
        "darlinghammond2010": '"The Flat World and Education" Darling-Hammond 2010',
        "hoxby2009": '"Charter Schools in New York City" Hoxby Murarka 2009',
        "lafortune2018": '"School Finance Reform and Distribution of Student Achievement" Lafortune 2018',
        "nickow2020": '"The Impressive Effects of Tutoring" Nickow Oreopoulos Quan NBER 2020',
        "garca2022": '"The Lasting Effects of Early Childhood Education" Garcia Heckman 2022',
        "heckman2010": '"The Rate of Return to the HighScope Perry Preschool Program" Heckman 2010',
        "jackson2016": '"The Effects of School Spending on Educational and Economic Outcomes" Jackson Johnson Persico 2016',
        "angrist2013": '"Stand and Deliver Effects of Boston Charter Schools" Angrist Pathak Walters 2013',
        "abdulkadiroglu2011": '"Accountability and Flexibility in Public Schools Evidence from Boston" Abdulkadiroglu 2011',
    }
    
    for k in sorted(missing):
        search = SEARCH_TERMS.get(k, f'"{k}" education research')
        f.write(f"| `{k}` | {search} |\n")

print(f"\nSaved to literature/still_missing_v2.md")
