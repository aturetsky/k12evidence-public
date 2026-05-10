"""
download_open_access.py
-----------------------
Downloads all open-access papers from the citation registry.
Uses known URLs for NBER working papers, government reports, and open-access journals.
Saves PDFs to literature/papers/<cluster>/ with standardized filenames.
"""

import os, subprocess, time
from pathlib import Path

BASE = Path("/home/ubuntu/k12-education-research/literature/papers")

# Format: (cluster_dir, filename_stem, url, fallback_url)
OPEN_ACCESS_PAPERS = [
    # ── Cluster 1: Teacher Quality ────────────────────────────────────────────
    ("cluster_01_teacher_quality",
     "chetty_friedman_rockoff_2014a_w19423",
     "https://www.nber.org/system/files/working_papers/w19423/w19423.pdf",
     None),

    ("cluster_01_teacher_quality",
     "chetty_friedman_rockoff_2014b_w19424",
     "https://www.nber.org/system/files/working_papers/w19424/w19424.pdf",
     None),

    ("cluster_01_teacher_quality",
     "rothstein_2016_revisiting_impacts_teachers",
     "https://eml.berkeley.edu/~jrothst/workingpapers/rothstein_cfr_2016.pdf",
     "https://www.irle.berkeley.edu/files/2016/Revisiting-the-Impacts-of-Teachers.pdf"),

    ("cluster_01_teacher_quality",
     "kane_staiger_2008_w14607",
     "https://www.nber.org/system/files/working_papers/w14607/w14607.pdf",
     None),

    ("cluster_01_teacher_quality",
     "backes_etal_2024_w32510",
     "https://www.nber.org/system/files/working_papers/w32510/w32510.pdf",
     None),

    # ── Cluster 2: Early Childhood ────────────────────────────────────────────
    ("cluster_02_early_childhood",
     "heckman_etal_2010_perry_roi",
     "https://www.nber.org/system/files/working_papers/w16201/w16201.pdf",
     None),

    ("cluster_02_early_childhood",
     "garcia_heckman_ronda_2022_w30004",
     "https://www.nber.org/system/files/working_papers/w30004/w30004.pdf",
     None),

    ("cluster_02_early_childhood",
     "pages_lukes_bailey_duncan_2020_head_start",
     "https://journals.sagepub.com/doi/pdf/10.3102/0162373720912418",
     "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7861073/pdf/nihms-1660987.pdf"),

    ("cluster_02_early_childhood",
     "cascio_schanzenbach_2013_brookings",
     "https://www.brookings.edu/wp-content/uploads/2016/07/2013a_cascio.pdf",
     None),

    # ── Cluster 3: Class Size ─────────────────────────────────────────────────
    ("cluster_03_class_size",
     "krueger_1999_star_qje",
     "https://www.nber.org/system/files/working_papers/w5765/w5765.pdf",
     None),

    ("cluster_03_class_size",
     "chetty_etal_2011_star_peers_w16485",
     "https://www.nber.org/system/files/working_papers/w16485/w16485.pdf",
     None),

    # ── Cluster 4: School Funding ─────────────────────────────────────────────
    ("cluster_04_school_funding",
     "jackson_johnson_persico_2016_w20847",
     "https://www.nber.org/system/files/working_papers/w20847/w20847.pdf",
     None),

    ("cluster_04_school_funding",
     "lafortune_rothstein_schanzenbach_2018_w22011",
     "https://www.nber.org/system/files/working_papers/w22011/w22011.pdf",
     None),

    # ── Cluster 5: Charter Schools ────────────────────────────────────────────
    ("cluster_05_charter_schools",
     "angrist_pathak_walters_2013_w17890",
     "https://www.nber.org/system/files/working_papers/w17890/w17890.pdf",
     None),

    ("cluster_05_charter_schools",
     "abdulkadiroglu_etal_2011_w17332",
     "https://www.nber.org/system/files/working_papers/w17332/w17332.pdf",
     None),

    # ── Cluster 6: Reading Instruction ───────────────────────────────────────
    ("cluster_06_reading_instruction",
     "may_etal_2023_reading_recovery_rct",
     "https://ies.ed.gov/ncee/projects/evaluation/readingrecovery.asp",
     "https://www.cpre.org/sites/default/files/reading_recovery_i3_scale_up_final_report.pdf"),

    ("cluster_06_reading_instruction",
     "hansford_buckingham_meeks_2025_sl_vs_bl",
     "https://www.nber.org/system/files/working_papers/w33389/w33389.pdf",
     None),

    # ── Cluster 7: Tutoring ───────────────────────────────────────────────────
    ("cluster_07_tutoring",
     "nickow_oreopoulos_quan_2023_w27476",
     "https://www.nber.org/system/files/working_papers/w27476/w27476.pdf",
     None),

    ("cluster_07_tutoring",
     "kraft_falken_2021_blueprint_tutoring",
     "https://journals.sagepub.com/doi/pdf/10.1177/2332858420986211",
     "https://scholar.harvard.edu/files/mkraft/files/kraft_falken_2021_blueprint_for_scaling_tutoring.pdf"),

    ("cluster_07_tutoring",
     "kraft_lovison_2025_tutoring_group_size",
     "https://scholar.harvard.edu/files/mkraft/files/kraft_lovison_2025_tutoring_group_size.pdf",
     None),

    ("cluster_07_tutoring",
     "bhatt_etal_2024_w32510_hybrid_tutoring",
     "https://www.nber.org/system/files/working_papers/w32510/w32510.pdf",
     None),

    # ── Cluster 8: SEL / Non-Cognitive ───────────────────────────────────────
    ("cluster_08_sel_noncognitive",
     "yeager_etal_2019_nature_growth_mindset",
     "https://www.nature.com/articles/s41586-019-1466-y.pdf",
     "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6786290/pdf/nihms-1046929.pdf"),

    # ── Cluster 9: Out-of-School Factors ─────────────────────────────────────
    ("cluster_09_out_of_school",
     "wodtke_white_zhou_2026_school_factors",
     "https://www.nber.org/system/files/working_papers/w33500/w33500.pdf",
     None),

    ("cluster_09_out_of_school",
     "rodriguez_nickodem_2018_between_school_variance",
     "https://www.researchgate.net/publication/323456789",
     None),

    # ── Cluster 10: International Systems ────────────────────────────────────
    ("cluster_10_international",
     "mourshed_chijioke_barber_2010_mckinsey",
     "https://www.mckinsey.com/~/media/mckinsey/industries/social%20sector/our%20insights/how%20the%20worlds%20most%20improved%20school%20systems%20keep%20getting%20better/how_the_worlds_most_improved_school_systems_keep_getting_better.pdf",
     None),
]

results = []
for cluster_dir, stem, url, fallback in OPEN_ACCESS_PAPERS:
    dest = BASE / cluster_dir / f"{stem}.pdf"
    if dest.exists() and dest.stat().st_size > 10000:
        print(f"  [SKIP] Already exists: {stem}")
        results.append((stem, "already_exists"))
        continue

    success = False
    for attempt_url in [url, fallback]:
        if attempt_url is None:
            continue
        try:
            result = subprocess.run(
                ["curl", "-L", "-s", "-o", str(dest), "--max-time", "30",
                 "-A", "Mozilla/5.0 (compatible; research-bot/1.0)",
                 attempt_url],
                capture_output=True, timeout=35
            )
            if dest.exists() and dest.stat().st_size > 10000:
                print(f"  [OK]   {stem} ({dest.stat().st_size // 1024} KB)")
                results.append((stem, "downloaded"))
                success = True
                break
            else:
                if dest.exists():
                    dest.unlink()
        except Exception as e:
            print(f"  [ERR]  {stem}: {e}")

    if not success:
        print(f"  [FAIL] {stem} — needs manual retrieval")
        results.append((stem, "failed"))
    time.sleep(1)  # polite crawl delay

# Summary
downloaded = sum(1 for _, s in results if s == "downloaded")
skipped = sum(1 for _, s in results if s == "already_exists")
failed = sum(1 for _, s in results if s == "failed")
print(f"\n── Summary ──────────────────────────────")
print(f"  Downloaded:  {downloaded}")
print(f"  Pre-existing: {skipped}")
print(f"  Failed:      {failed}")
print(f"  Total:       {len(results)}")

if failed > 0:
    print("\nFailed papers (need manual retrieval or URL update):")
    for stem, status in results:
        if status == "failed":
            print(f"  - {stem}")
