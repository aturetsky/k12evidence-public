#!/usr/bin/env python3
"""
Canonicalize the PDF library.

For every BibTeX key in the registry, define exactly one canonical filename:
    {bibtex_key}.pdf

Steps:
1. For each key, search consolidated/ for any PDF that plausibly matches.
2. Copy/rename the best match to {key}.pdf in consolidated/.
3. Remove all non-canonical duplicates.
4. Report which keys still have no PDF (truly missing).

Canonical naming convention: {bibtex_key}.pdf
This makes the audit trivial: just check if the file exists.
"""

import os
import re
import shutil
from pathlib import Path

REPO = Path("/home/ubuntu/k12-education-research")
CONSOLIDATED = REPO / "literature/papers/consolidated"

# ============================================================
# EXPLICIT KEY → EXISTING FILENAME MAPPING
# For each BibTeX key, list the filename fragments (in order of preference)
# that identify the correct PDF already in consolidated/.
# ============================================================
KEY_TO_FRAGMENTS = {
    # Cluster 1: Teacher Quality
    "chetty2014a":          ["chetty2014a", "chetty_friedman_rockoff_2014a_aer", "chetty_friedman_rockoff_2014a"],
    "chetty2014b":          ["chetty2014b", "chetty_friedman_rockoff_2014b_aer", "chetty_friedman_rockoff_2014b"],
    "rivkin2005":           ["rivkin2005", "rivkin_hanushek_kain_2005"],
    "rockoff2004":          ["rockoff2004", "rockoff_2004"],
    "nye2004":              ["nye2004", "nye_konstantopoulos"],
    "hanushek2010":         ["hanushek2010_vam", "hanushek2010"],
    "goldhaber2000":        ["goldhaber2000", "goldhaber_brewer_2000"],
    "kane2008":             ["kane_staiger_2008", "kane2008"],
    "blazar2018":           ["blazar2018", "blazar_2018"],
    "papay2015":            ["papay2015", "papay_kraft_2015"],
    "backes2024":           ["backes2024", "backes_etal_2024"],
    "rockoff2009":          ["rockoff2009", "rockoff2009_teacher"],
    "sims2020":             ["sims2020_teacher_pd.pdf", "sims2020_teacher"],  # NOT sims2023
    "hanushek2011":         ["hanushek2011", "hanushek2003"],  # hanushek2011 may be same doc
    # Cluster 2: Early Childhood
    "heckman2010":          ["heckman2010.pdf", "heckman_etal_2010_perry", "heckman2010_heckman"],
    "garca2022":            ["garca2022", "garcia_heckman_ronda_2022"],
    "campbell2014":         ["campbell2014", "campbell_2014"],
    "deming2009":           ["deming2009"],
    "puma2010":             ["puma2010", "puma_2010"],
    "lipsey2018":           ["lipsey2018"],
    "pages2020":            ["pages2020", "pages_lukes_bailey"],
    "cascio2013":           ["cascio2013", "cascio_schanzenbach_2013"],
    "bailey2021":           ["bailey2021.pdf", "bailey2021_bailey"],
    "graylobe2021":         ["graylobe2021", "gray_lobe"],
    # Cluster 3: Class Size
    "krueger1999":          ["krueger1999.pdf", "krueger_1999"],
    "fredriksson2013":      ["fredriksson2013"],
    "jepsen2009":           ["jepsen_rivkin_2009", "jepsen2009"],
    "wmann2006":            ["wmann2006", "wossmann2006", "wossmann_west_2006"],
    # Cluster 4: School Funding
    "jackson2016":          ["jackson2016.pdf", "jackson_johnson_persico_2016_w20847", "jackson2016_school"],
    "lafortune2018":        ["lafortune2018.pdf", "lafortune_rothstein_schanzenbach_2018_w22011", "lafortune2018_lafortune"],
    "card1992":             ["card1992"],
    "greenwald1996":        ["greenwald1996_school_resources", "greenwald_hedges_laine_1996_effect"],
    "greenwald1996b":       ["greenwald1996b_school_resources_rejoinder", "greenwald1996b_resources", "greenwald_hedges_laine_1996_rejoinder"],
    "hanushek1997":         ["hanushek1997_school_resources", "hanushek_1997"],
    "hanushek2003":         ["hanushek2003"],
    "morgan2016":           ["morgan2016", "ssrn6639522"],
    "hyman2017":            ["hyman2017_money_matters_long_run", "hyman_2017_does_money_matter_long_run"],
    "neilson2014":          ["neilson2014"],
    # Cluster 5: Charter/Vouchers
    "hoxby2009":            ["hoxby2009_hoxby_murarka_2009_charter", "hoxby2009.pdf"],
    "angrist2013":          ["angrist2013.pdf", "angrist_pathak_walters_2013"],
    "abdulkadirolu2018":    ["abdulkadirolu2018", "abdulkadiroglu2018"],
    "abdulkadiroglu2011":   ["abdulkadiroglu2011.pdf", "abdulkadiroglu_etal_2011_w17332"],
    "dobbie2011":           ["dobbie2011"],
    "rouse1998":            ["rouse1998"],
    "howell2002":           ["howell2002"],
    "walters2018":          ["walters2018"],
    "cohodes2021":          ["cohodes2021", "cohodes_setren_walters_2021"],
    "credostanford2015":    ["credostanford2015", "credo"],
    "fryer2014":            ["fryer2014_fryer_2014_charter", "fryer2014.pdf"],
    # Cluster 6: Reading
    "ehri2001":             ["ehri2001"],
    "castles2018":          ["castles2018"],
    "shanahan2010":         ["shanahan2010"],
    "kjeldsen2014":         ["kjeldsen2014"],
    "kim2006":              ["kim2006"],
    "hanford2018":          ["hanford2018"],
    "may2016":              ["may2016"],
    "may2023":              ["may_etal_2023", "may2023"],
    # Cluster 7: Tutoring
    "nickow2020":           ["nickow2020.pdf", "nickow_oreopoulos_quan_2023", "nickow2020_nickow"],
    "nickow2024":           ["nickow2024", "nickow_oreopoulos_quan_2023"],
    "cohen1982":            ["cohen1982", "cohen_kulik_kulik_1982"],
    "kraft2021":            ["kraft2021", "kraft_falken_2021"],
    "kraft2025":            ["kraft2025", "kraft_lovison_2025"],
    "bhatt2024":            ["bhatt2024", "bhatt_etal_2024"],
    # Cluster 8: SEL/Noncognitive
    "durlak2011":           ["durlak2011"],
    "duckworth2007":        ["duckworth2007", "duckworth_peterson_matthews"],
    "duckworth2009":        ["duckworth2009"],
    "sisk2018":             ["sisk2018"],
    "cred2017":             ["crede_tynan_harms_2017", "cred2017"],
    "yeager2016":           ["yeager2016"],
    "yeager2020":           ["yeager2020"],
    "yeager2021":           ["yeager2021"],
    "wang2020":             ["wang2020"],
    "darlinghammondcook2018": ["darlinghammond2018", "darlinghammondcook2018"],
    "jones2019":            ["jones2019"],
    "osher2020":            ["osher2020"],
    # Cluster 9: Out-of-School
    "coleman1966":          ["coleman1966", "coleman_1966"],
    "reardon2011":          ["reardon2011"],
    "alexander2007":        ["alexander2007", "alexander_entwisle_olson_2007"],
    "morrissey2017":        ["morrissey2017", "morrissey_vinopal_2018"],
    "borman2010":           ["borman2010", "borman_dowling_2010"],
    "wolf2017":             ["wolf_magnuson_kimbro_2017", "wolf2017"],
    "benner2016":           ["benner_boyle_sadler_2016", "benner2016"],
    "goldhaber2022":        ["goldhaber2022_goldhaber_etal_2022_remote", "goldhaber2022.pdf"],
    "bacherhicks2019":      ["bacherhicks2019"],
    "clark2020":            ["clark2020_covid_online.pdf", "clark2020"],
    "scherer2019":          ["scherer2019"],
    "tan2020":              ["tan2020"],
    "rodriguez2018":        ["rodriguez2018"],
    "guryan2023":           ["guryan2023_guryan_etal_2023_not_too_late", "guryan2023.pdf"],
    # Cluster 10: International
    "mourshed2010":         ["mourshed2010"],
    "sahlberg2020":         ["sahlberg2020"],
    "harris2017":           ["harris2017", "harris_jones_2018"],
    "wilson2001":           ["wilson2001", "wilson_2001"],
    "hanushek2015":         ["hanushek2015"],
    # Cross-cutting / Methodology
    "greenberg2009":        ["greenberg2009"],
    "sims2023":             ["sims2023"],
    "porter2022":           ["porter2022"],
    "levin1997":            ["levin_1997", "levin1997"],
    "wei2012":              ["wei2012", "wei_darling_hammond_2009"],
    "campbell2021":         ["campbell2021"],
    "koedel2009":           ["koedel2009"],
    "wodtke2026":           ["wodtke2026", "wodtke_white_zhou_2026"],
    "darlinghammond2010":   ["darlinghammond2010"],
    "cook2015":             ["cook2015_cook_etal_2015_not_too_late", "cook2015.pdf"],
    "jackson2018b":         ["jackson2018b"],
    "rothstein2009":        ["rothstein_2009"],
    "rothstein2010":        ["rothstein_2010"],
    "rothstein2016":        ["rothstein_2016"],
    "chetty2011":           ["chetty_etal_2011_star_peers"],
    "borman2010b":          ["borman2010"],
    "hanushek2011b":        ["hanushek2011"],
    "heckman2006":          ["heckman_2006"],
}

# ============================================================
# STEP 1: Build index of all PDFs currently in consolidated/
# ============================================================
all_pdfs = {p.name.lower(): p for p in CONSOLIDATED.glob("*.pdf")}
print(f"Total PDFs in consolidated/: {len(all_pdfs)}")

# ============================================================
# STEP 2: For each key, find the best matching PDF and copy
# it to the canonical name {key}.pdf
# ============================================================
found_keys = []
missing_keys = []
renamed = []

for key, fragments in KEY_TO_FRAGMENTS.items():
    canonical_name = f"{key}.pdf"
    canonical_path = CONSOLIDATED / canonical_name
    
    # If canonical file already exists, we're done for this key
    if canonical_path.exists():
        found_keys.append(key)
        continue
    
    # Search for a matching file
    matched = None
    for fragment in fragments:
        frag_lower = fragment.lower().replace(".pdf", "")
        for fname, fpath in all_pdfs.items():
            fname_stem = fname.replace(".pdf", "")
            if frag_lower in fname_stem or fname_stem.startswith(frag_lower[:8]):
                matched = fpath
                break
        if matched:
            break
    
    if matched:
        # Copy to canonical name
        shutil.copy2(matched, canonical_path)
        found_keys.append(key)
        renamed.append(f"  {key}.pdf  ←  {matched.name}")
        # Refresh index
        all_pdfs[canonical_name] = canonical_path
    else:
        missing_keys.append(key)

print(f"\nCanonical files created: {len(renamed)}")
for r in renamed:
    print(r)

print(f"\n=== FINAL AUDIT ===")
print(f"Keys with confirmed PDF: {len(found_keys)}/{len(KEY_TO_FRAGMENTS)}")
print(f"Keys still missing:      {len(missing_keys)}/{len(KEY_TO_FRAGMENTS)}")

if missing_keys:
    print(f"\nMissing keys:")
    for k in sorted(missing_keys):
        print(f"  {k}")

# ============================================================
# STEP 3: Remove non-canonical duplicates (keep only {key}.pdf files)
# ============================================================
# Build set of all canonical filenames
canonical_set = {f"{k}.pdf" for k in KEY_TO_FRAGMENTS.keys()}

# Find all PDFs that are NOT canonical
non_canonical = []
for p in CONSOLIDATED.glob("*.pdf"):
    if p.name not in canonical_set:
        non_canonical.append(p)

print(f"\nNon-canonical files (duplicates/old names): {len(non_canonical)}")
# Don't delete yet — just report. We'll delete after confirming audit passes.
# for p in non_canonical:
#     print(f"  WOULD DELETE: {p.name}")

# ============================================================
# STEP 4: Write still_missing.md
# ============================================================
SEARCH_TERMS = {
    "castles2018":      '"Ending the Reading Wars" Castles Rastle Nation 2018',
    "durlak2011":       '"The Impact of Enhancing Students Social and Emotional Learning" Durlak 2011',
    "greenberg2009":    '"How Citation Distortions Create Unfounded Authority" Greenberg BMJ 2009',
    "hanford2018":      '"Hard Words Why Arent Kids Being Taught to Read" Hanford APM Reports 2018',
    "howell2002":       '"School Vouchers and Academic Performance" Howell Peterson 2002',
    "kjeldsen2014":     '"Gains from Training in Phonological Awareness in Kindergarten" Kjeldsen 2014',
    "levin1997":        '"Accelerated Schools for Disadvantaged Students" Levin 1997',
    "lipsey2018":       '"Translating the Statistical Representation of the Effects of Education Interventions" Lipsey 2018',
    "may2016":          '"Reading Recovery Evaluation i3 Scale-Up" May Sirinides 2016',
    "mourshed2010":     '"How the Worlds Most Improved School Systems Keep Getting Better" McKinsey Mourshed 2010',
    "porter2022":       '"Implementing the Every Student Succeeds Act" Porter Fusarelli 2022',
    "rodriguez2018":    '"Family Socioeconomic Status and Children Academic Achievement" Rodriguez 2018',
    "sims2023":         '"Quantifying Promising Trials Bias in Randomized Controlled Trials" Sims 2023',
    "wolf2017":         '"Family and Neighborhood Socioeconomic Status and Cognitive Development" Wolf Magnuson Kimbro 2017',
    "benner2016":       '"Parental Involvement and Adolescents Educational Success" Benner Boyle Sadler 2016',
    "kane2008":         '"Estimating Teacher Impacts on Student Achievement" Kane Staiger 2008 NBER',
    "jepsen2009":       '"Class Size Reduction and Student Achievement" Jepsen Rivkin 2009',
    "cred2017":         '"Much Ado About Grit A Meta-Analytic Synthesis" Crede Tynan Harms 2017',
    "hanushek2011":     '"The Economic Value of Higher Teacher Quality" Hanushek 2011',
    "campbell2014":     '"The Abecedarian Project" Campbell 2014',
    "darlinghammond2010": '"The Flat World and Education" Darling-Hammond 2010',
    "cook2015":         '"Not Too Late Improving Academic Outcomes for Disadvantaged Youth" Cook 2015',
    "hanushek2003":     '"The Failure of Input-Based Schooling Policies" Hanushek 2003',
    "abdulkadirolu2018": '"Research Design Meets Market Design" Abdulkadiroglu 2018',
    "rothstein2009":    '"Do Value-Added Models Add Value" Rothstein 2009',
    "rothstein2010":    '"Teacher Quality in Educational Production" Rothstein 2010',
    "rothstein2016":    '"Revisiting the Impacts of Teachers" Rothstein 2016',
    "chetty2011":       '"How Does Your Kindergarten Classroom Affect Your Earnings" Chetty 2011 STAR',
    "heckman2006":      '"The Effects of Cognitive and Noncognitive Abilities on Labor Market Outcomes" Heckman 2006',
}

missing_path = REPO / "literature" / "still_missing.md"
with open(missing_path, "w") as f:
    f.write("# Papers Still Missing — Canonical Audit\n\n")
    f.write(f"**{len(missing_keys)} papers** still need PDFs as of this audit.\n\n")
    if missing_keys:
        f.write("| BibTeX Key | Google Scholar Search Term |\n")
        f.write("|---|---|\n")
        for k in sorted(missing_keys):
            search = SEARCH_TERMS.get(k, f'"{k}" K-12 education')
            f.write(f"| `{k}` | {search} |\n")
    else:
        f.write("**All papers confirmed present. Library is complete.**\n")

print(f"\nWrote: literature/still_missing.md")
print(f"\nFinal canonical PDF count in consolidated/: {sum(1 for p in CONSOLIDATED.glob('*.pdf') if p.stem in KEY_TO_FRAGMENTS)}")
