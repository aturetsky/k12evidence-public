"""
sort_downloaded_papers.py
-------------------------
After Avi moves downloaded PDFs into the staging folder
(literature/papers/_staging/), this script:
  1. Matches each PDF by filename keyword to the correct cluster directory
  2. Renames it to the canonical filename used in the registry
  3. Moves it into the correct cluster_XX folder
  4. Reports any unmatched files for manual review

Usage:
    python3 scripts/sort_downloaded_papers.py

Place downloaded PDFs in:
    /home/ubuntu/k12-education-research/literature/papers/_staging/
"""

import os, shutil
from pathlib import Path

BASE = Path("/home/ubuntu/k12-education-research/literature/papers")
STAGING = BASE / "_staging"
STAGING.mkdir(exist_ok=True)

# Mapping: (keyword_fragments_in_filename, cluster_dir, canonical_name)
# keyword_fragments: ALL must appear (case-insensitive) in the source filename
PAPER_MAP = [
    # ── Cluster 1: Teacher Quality / VAMs ────────────────────────────────────
    (["chetty", "2014", "2593"],      "cluster_01_teacher_quality", "chetty_friedman_rockoff_2014a_aer.pdf"),
    (["chetty", "2014", "2633"],      "cluster_01_teacher_quality", "chetty_friedman_rockoff_2014b_aer.pdf"),
    (["rothstein", "2010"],           "cluster_01_teacher_quality", "rothstein_2010_qje.pdf"),
    (["jackson", "test score", "miss"], "cluster_01_teacher_quality", "jackson_2018_jpe.pdf"),
    (["rivkin"],                      "cluster_01_teacher_quality", "rivkin_hanushek_kain_2005_econometrica.pdf"),
    (["rockoff", "2004"],             "cluster_01_teacher_quality", "rockoff_2004_aer.pdf"),
    (["goldhaber", "brewer"],         "cluster_01_teacher_quality", "goldhaber_brewer_2000_eepa.pdf"),
    (["papay", "kraft"],              "cluster_01_teacher_quality", "papay_kraft_2015_jpube.pdf"),
    (["rothstein", "2009"],           "cluster_01_teacher_quality", "rothstein_2009_efp.pdf"),
    (["koedel", "betts"],             "cluster_01_teacher_quality", "koedel_betts_2009_efp.pdf"),
    (["blazar", "2018"],              "cluster_01_teacher_quality", "blazar_2018_eepa.pdf"),
    (["nye", "konstantopoulos"],      "cluster_01_teacher_quality", "nye_konstantopoulos_hedges_2004_eepa.pdf"),

    # ── Cluster 3: Class Size ─────────────────────────────────────────────────
    (["angrist", "lavy", "1999"],     "cluster_03_class_size", "angrist_lavy_1999_qje.pdf"),
    (["angrist", "lavy", "2019"],     "cluster_03_class_size", "angrist_lavy_2019_aer.pdf"),
    (["fredriksson"],                 "cluster_03_class_size", "fredriksson_ockert_oosterbeek_2013_qje.pdf"),
    (["hoxby", "2000"],               "cluster_03_class_size", "hoxby_2000_qje.pdf"),
    (["jepsen", "rivkin"],            "cluster_03_class_size", "jepsen_rivkin_2009_jhr.pdf"),
    (["wossmann", "west"],            "cluster_03_class_size", "wossmann_west_2006_eer.pdf"),
    (["wößmann"],                     "cluster_03_class_size", "wossmann_west_2006_eer.pdf"),

    # ── Cluster 4: School Funding ─────────────────────────────────────────────
    (["hanushek", "1997"],            "cluster_04_school_funding", "hanushek_1997_eepa.pdf"),
    (["card", "krueger", "1992"],     "cluster_04_school_funding", "card_krueger_1992_jpe.pdf"),
    (["neilson", "zimmerman"],        "cluster_04_school_funding", "neilson_zimmerman_2014_jpube.pdf"),
    (["hyman", "2017"],               "cluster_04_school_funding", "hyman_2017_aej_policy.pdf"),
    (["hanushek", "2003"],            "cluster_04_school_funding", "hanushek_2003_ej.pdf"),
    (["greenwald", "hedges", "laine"],"cluster_04_school_funding", "greenwald_hedges_laine_1996_rer.pdf"),

    # ── Cluster 5: Charter Schools / Vouchers ────────────────────────────────
    (["abdulkadiroglu", "2016"],      "cluster_05_charter_schools", "abdulkadiroglu_2016_aer.pdf"),
    (["abdulkadiroğlu", "2016"],      "cluster_05_charter_schools", "abdulkadiroglu_2016_aer.pdf"),
    (["cohodes", "setren"],           "cluster_05_charter_schools", "cohodes_setren_walters_2021_aej_policy.pdf"),
    (["abdulkadiroglu", "pathak", "walters"], "cluster_05_charter_schools", "abdulkadiroglu_pathak_walters_2018_aej_applied.pdf"),
    (["rouse", "1998"],               "cluster_05_charter_schools", "rouse_1998_qje.pdf"),
    (["fryer", "2014"],               "cluster_05_charter_schools", "fryer_2014_qje.pdf"),
    (["walters", "2018"],             "cluster_05_charter_schools", "walters_2018_jpe.pdf"),

    # ── Cluster 6: Reading Instruction ───────────────────────────────────────
    (["castles", "rastle"],           "cluster_06_reading_instruction", "castles_rastle_nation_2018_pspi.pdf"),
    (["kjeldsen"],                    "cluster_06_reading_instruction", "kjeldsen_etal_2014_rw.pdf"),

    # ── Cluster 7: High-Dosage Tutoring ──────────────────────────────────────
    (["guryan", "ludwig"],            "cluster_07_tutoring", "guryan_etal_2023_aer.pdf"),
    (["cohen", "kulik", "1982"],      "cluster_07_tutoring", "cohen_kulik_kulik_1982_aerj.pdf"),
    (["nickow", "2024"],              "cluster_07_tutoring", "nickow_oreopoulos_quan_2024_aerj.pdf"),
    (["nickow", "promise"],           "cluster_07_tutoring", "nickow_oreopoulos_quan_2024_aerj.pdf"),

    # ── Cluster 8: SEL / Non-Cognitive Skills ────────────────────────────────
    (["durlak"],                      "cluster_08_sel_noncognitive", "durlak_etal_2011_cd.pdf"),
    (["sisk"],                        "cluster_08_sel_noncognitive", "sisk_etal_2018_ps.pdf"),
    (["credé"],                       "cluster_08_sel_noncognitive", "crede_tynan_harms_2017_jpsp.pdf"),
    (["crede", "tynan"],              "cluster_08_sel_noncognitive", "crede_tynan_harms_2017_jpsp.pdf"),
    (["heckman", "stixrud"],          "cluster_08_sel_noncognitive", "heckman_stixrud_urzua_2006_jle.pdf"),
    (["porter", "fusarelli"],         "cluster_08_sel_noncognitive", "porter_fusarelli_2022_ep.pdf"),
    (["duckworth", "2007"],           "cluster_08_sel_noncognitive", "duckworth_etal_2007_jpsp.pdf"),
    (["duckworth", "peterson"],       "cluster_08_sel_noncognitive", "duckworth_etal_2007_jpsp.pdf"),

    # ── Cluster 9: Out-of-School Factors ─────────────────────────────────────
    (["borman", "dowling"],           "cluster_09_out_of_school", "borman_dowling_2010_tcr.pdf"),
    (["alexander", "entwisle"],       "cluster_09_out_of_school", "alexander_entwisle_olson_2007_asr.pdf"),
    (["morrissey", "vinopal"],        "cluster_09_out_of_school", "morrissey_vinopal_2018_jmf.pdf"),
    (["tan", "lyu", "peng"],          "cluster_09_out_of_school", "tan_lyu_peng_2020_psp.pdf"),
    (["benner", "boyle"],             "cluster_09_out_of_school", "benner_boyle_sadler_2016_jra.pdf"),
    (["wolf", "magnuson"],            "cluster_09_out_of_school", "wolf_magnuson_kimbro_2017_dp.pdf"),
    (["kim", "2006"],                 "cluster_09_out_of_school", "kim_2006_eepa.pdf"),

    # ── Cluster 10: International Systems ────────────────────────────────────
    (["harris", "jones", "2017"],     "cluster_10_international", "harris_jones_2017_slm.pdf"),
]

def match_file(filename: str):
    """Return (cluster_dir, canonical_name) for a filename, or None if no match."""
    fn_lower = filename.lower()
    for keywords, cluster, canonical in PAPER_MAP:
        if all(kw.lower() in fn_lower for kw in keywords):
            return cluster, canonical
    return None

def sort_papers():
    staged = list(STAGING.glob("*.pdf"))
    if not staged:
        print(f"No PDFs found in {STAGING}")
        print("Place downloaded PDFs there and re-run this script.")
        return

    moved = []
    unmatched = []

    for pdf in staged:
        result = match_file(pdf.name)
        if result:
            cluster_dir, canonical = result
            dest_dir = BASE / cluster_dir
            dest_dir.mkdir(exist_ok=True)
            dest = dest_dir / canonical
            if dest.exists():
                print(f"  [SKIP] Already exists: {canonical}")
            else:
                shutil.move(str(pdf), str(dest))
                moved.append((cluster_dir, canonical))
                print(f"  [MOVED] {pdf.name} → {cluster_dir}/{canonical}")
        else:
            unmatched.append(pdf.name)
            print(f"  [UNMATCHED] {pdf.name} — needs manual placement")

    print(f"\n── Summary ──────────────────────────────────────────")
    print(f"  Moved:     {len(moved)}")
    print(f"  Unmatched: {len(unmatched)}")
    if unmatched:
        print(f"\nUnmatched files (place manually):")
        for fn in unmatched:
            print(f"  {STAGING / fn}")

if __name__ == "__main__":
    sort_papers()
