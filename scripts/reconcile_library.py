"""
Reconcile the uploaded PDFs against what's already in the repo.
1. List all PDFs currently in the repo
2. Compare against uploaded files by filename similarity and size
3. Copy any genuinely new files into the consolidated library
4. Report what was already there, what's new, and what's still missing
"""

import os
import re
import shutil
from pathlib import Path

REPO = Path("/home/ubuntu/k12-education-research")
UPLOAD_DIR = Path("/home/ubuntu/upload")
LIBRARY_DIR = REPO / "literature" / "papers" / "consolidated"
LIBRARY_DIR.mkdir(parents=True, exist_ok=True)

# Map uploaded files to canonical BibTeX keys and clean names
# Format: (upload_filename_pattern, bib_key, clean_name)
UPLOAD_MAP = [
    ("Professional_Learning_in_the_Learning_Pr", "campbell2021", "campbell2021_professional_learning"),
    ("1-s2.0-S0272775796000696", "rouse1998", "rouse1998_private_school_vouchers"),
    ("kim-2006", "kim2006", "kim2006_summer_reading_intervention"),
    ("1-s2.0-S0190740917301731", "tan2020", "tan2020_intensive_parenting"),  # check year
    ("s10964-016-0431-4", "sisk2018", "sisk2018_growth_mindsets"),  # check year
    ("2007-07951-009", "duckworth2007", "duckworth2007_grit"),
    ("cohen-et-al-1982", "cohen1982", "cohen1982_tutoring_meta_analysis"),
    ("greenwald-et-al-1996-interpreting", "greenwald1996b", "greenwald1996b_school_resources_rejoinder"),
    ("greenwald-et-al-1996-the-effect", "greenwald1996", "greenwald1996_school_resources"),
    ("Schools_and_Inequality", "reardon2011", "reardon2011_schools_inequality"),
    ("Leadingschoolsaslearningorganizations", "leithwood2004", "leithwood2004_learning_organizations"),
    ("JofMarriageandFamily-2017-Morrissey", "morrissey2017", "morrissey2017_neighborhood_poverty"),
    ("alexander-et-al-2007", "alexander2007", "alexander2007_summer_learning_gap"),
    ("FGIIW_20260430", "ssrn2026", "ssrn2026_unknown"),  # need to identify
    ("2016-29674-001", "yeager2016", "yeager2016_growth_mindset"),
    ("cohodes-et-al-2021", "cohodes2021", "cohodes2021_charter_scaling"),
    ("w25796", "nber_w25796", "nber_w25796_unknown"),  # need to identify
    ("Hyman-MoneyMatterLong-2017", "hyman2017", "hyman2017_money_matters"),
    ("POL2015-0249_app", "pol2015", "pol2015_unknown"),  # need to identify
    ("hanushek-1997", "hanushek1997", "hanushek1997_school_resources"),
    ("Wmann-InternationalEvidenceExpenditures-2006", "wossmann2006", "wossmann2006_international_expenditures"),
    ("project_muse_466693", "projectmuse", "projectmuse_unknown"),  # need to identify
    ("goldhaber-brewer-2000", "goldhaber2000", "goldhaber2000_teacher_certification"),
    ("ED443782", "ed443782", "ed443782_unknown"),  # need to identify
    ("edfp_a_00251", "edfp2016", "edfp2016_unknown"),  # need to identify
    ("DistributedleadershipinpracticeinFinnishschools", "sahlberg_dist", "sahlberg_distributed_leadership"),
    ("nye-et-al-2004", "nye2004", "nye2004_teacher_effects"),
    ("edfp.2009.4.4.319", "rockoff2009", "rockoff2009_teacher_effectiveness"),
    ("1-s2.0-S0047272715001449", "jackson2016", "jackson2016_school_spending"),
    ("2006-the-impact-of-individual-teachers", "rockoff2004", "rockoff2004_individual_teachers"),
    ("Econometrica-2005-Rivkin", "rivkin2005", "rivkin2005_teachers_schools_achievement"),
    ("699018", "jackson2018b", "jackson2018b_test_scores_miss"),
    ("125-1-175", "krueger1999", "krueger1999_star_experiment"),
    ("chetty-et-al-2014-measuring-the-impacts-of-teachers-i", "chetty2014a", "chetty2014a_teacher_vam_bias"),
    ("chetty-et-al-2014-measuring-the-impacts-of-teachers-ii", "chetty2014b", "chetty2014b_teacher_vam_outcomes"),
    ("ssrn-6639522", "ssrn6639522", "ssrn6639522_unknown"),  # need to identify
    # Previously uploaded (pasted_file prefix)
    ("pasted_file_HOdNYE_2020-99903-019", "yeager2020", "yeager2020_growth_mindset_controversies"),
    ("pasted_file_QV97zq", "scherer2019", "scherer2019_ses_ict_literacy"),
    ("pasted_file_W7qNaw", "clark2020", "clark2020_covid_online_learning"),
    ("pasted_file_efVviJ_Hanushek-Generalizations", "hanushek2010", "hanushek2010_vam_generalizations"),
    ("pasted_file_fdDGGo_yeager-et-al-2021", "yeager2021", "yeager2021_teacher_mindsets"),
    ("pasted_file_ifbBlS_Drivers", "osher2020", "osher2020_drivers_human_development"),
    ("pasted_file_paMQX7", "wang2020", "wang2020_classroom_climate"),
    ("pasted_file_wBvxvB_Identifying", "sims2020", "sims2020_teacher_pd_characteristics"),
]

# Get all existing PDFs in repo (excluding upload dir)
existing_pdfs = {}
for p in REPO.rglob("*.pdf"):
    if "/upload/" not in str(p):
        existing_pdfs[p.name.lower()] = p
        existing_pdfs[p.stem.lower()] = p

print(f"Existing PDFs in repo: {len(set(existing_pdfs.values()))}")
print(f"Uploaded files: {len(list(UPLOAD_DIR.glob('*.pdf')))}")
print()

already_in_repo = []
newly_copied = []
unidentified = []

for pattern, bib_key, clean_name in UPLOAD_MAP:
    # Find the matching uploaded file
    upload_file = None
    for f in UPLOAD_DIR.glob("*.pdf"):
        if pattern.lower() in f.name.lower():
            upload_file = f
            break
    
    if not upload_file:
        continue
    
    dest = LIBRARY_DIR / f"{clean_name}.pdf"
    
    # Check if already in repo under any name
    in_repo = False
    for existing_stem, existing_path in existing_pdfs.items():
        if (bib_key.lower() in existing_stem or 
            clean_name.split("_")[0].lower() in existing_stem):
            in_repo = True
            already_in_repo.append((bib_key, clean_name, str(existing_path).replace(str(REPO)+"/", "")))
            break
    
    # Always copy to consolidated dir with clean name
    shutil.copy2(upload_file, dest)
    
    if not in_repo:
        newly_copied.append((bib_key, clean_name))
        print(f"  NEW: {bib_key} -> {clean_name}.pdf")
    else:
        print(f"  EXISTS: {bib_key} (also at {already_in_repo[-1][2]})")

print(f"\n=== SUMMARY ===")
print(f"Already in repo: {len(already_in_repo)}")
print(f"Newly added: {len(newly_copied)}")

# Now run full BibTeX audit against consolidated library
print("\n=== FULL BIB AUDIT ===")
bib_file = REPO / "drafts" / "k12_references.bib"
with open(bib_file) as f:
    bib = f.read()

all_keys = re.findall(r'@\w+\{(\w+),', bib)
print(f"Total BibTeX keys: {len(all_keys)}")

# All PDFs now in consolidated dir + rest of repo
all_repo_pdfs = set()
for p in REPO.rglob("*.pdf"):
    if "/upload/" not in str(p):
        all_repo_pdfs.add(p)

print(f"Total PDFs in repo (incl. consolidated): {len(all_repo_pdfs)}")

# Check each key
missing_keys = []
found_keys = []
for key in sorted(all_keys):
    key_lower = key.lower()
    found = False
    for p in all_repo_pdfs:
        stem = p.stem.lower()
        if key_lower[:8] in stem or stem[:8] in key_lower:
            found = True
            found_keys.append((key, str(p).replace(str(REPO)+"/", "")))
            break
    if not found:
        missing_keys.append(key)

print(f"\nFound: {len(found_keys)}")
print(f"Still missing: {len(missing_keys)}")
print("\nStill missing PDFs:")
for key in missing_keys:
    # Get title and author from bib
    match = re.search(rf'@\w+\{{{key},[^@]+?title\s*=\s*\{{([^}}]+)\}}[^@]+?author\s*=\s*\{{([^}}]+)\}}', bib, re.DOTALL)
    if not match:
        match = re.search(rf'@\w+\{{{key},[^@]+?author\s*=\s*\{{([^}}]+)\}}[^@]+?title\s*=\s*\{{([^}}]+)\}}', bib, re.DOTALL)
        if match:
            author, title = match.group(1), match.group(2)
        else:
            author, title = "unknown", "unknown"
    else:
        title, author = match.group(1), match.group(2)
    first_author = author.split(",")[0].strip()
    year_m = re.search(r'(\d{4})', key)
    year = year_m.group(1) if year_m else "????"
    print(f"  [{key}] {first_author} ({year}) — {title[:60]}")

# Save missing list
with open(REPO / "literature" / "still_missing.md", "w") as f:
    f.write("# Papers Still Missing from Library\n\n")
    f.write(f"As of audit run. {len(missing_keys)} papers need PDFs.\n\n")
    f.write("| # | BibTeX Key | First Author | Year | Title |\n")
    f.write("|---|---|---|---|---|\n")
    for i, key in enumerate(missing_keys, 1):
        match = re.search(rf'@\w+\{{{key},[^@]+?title\s*=\s*\{{([^}}]+)\}}[^@]+?author\s*=\s*\{{([^}}]+)\}}', bib, re.DOTALL)
        if not match:
            match = re.search(rf'@\w+\{{{key},[^@]+?author\s*=\s*\{{([^}}]+)\}}[^@]+?title\s*=\s*\{{([^}}]+)\}}', bib, re.DOTALL)
            if match:
                author, title = match.group(1), match.group(2)
            else:
                author, title = "unknown", "unknown"
        else:
            title, author = match.group(1), match.group(2)
        first_author = author.split(",")[0].strip()
        year_m = re.search(r'(\d{4})', key)
        year = year_m.group(1) if year_m else "????"
        f.write(f"| {i} | `{key}` | {first_author} | {year} | {title[:60]} |\n")

print(f"\nMissing list saved to literature/still_missing.md")
