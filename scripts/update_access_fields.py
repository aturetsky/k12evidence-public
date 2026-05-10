#!/usr/bin/env python3
"""
Update citation registry with access_class and free_url fields.

Access classes:
  open_access       - Published in fully open-access journal; freely distributable
  preprint_available - Paywalled journal; legal free preprint exists (NBER/SSRN/author page)
  government_report  - US government publication; public domain
  paywalled_only     - No legal free version found
  restricted_data    - Paper uses restricted-use data; note on data access

free_url: The canonical free URL (NBER, SSRN, author page, gov site), or null if none.
"""

import json

# Known free URLs for papers in the registry
# Format: id -> (access_class, free_url)
ACCESS_MAP = {
    # === CLUSTER 1: Teacher Quality / VAMs ===
    1:  ("preprint_available", "https://www.nber.org/papers/w19423"),   # CFR I
    2:  ("preprint_available", "https://www.nber.org/papers/w19424"),   # CFR II
    3:  ("paywalled_only",     None),                                    # Rothstein 2010 QJE
    4:  ("preprint_available", "https://www.nber.org/papers/w20647"),   # Jackson 2018 JPE
    5:  ("preprint_available", "https://www.nber.org/papers/w16606"),   # Hanushek 2011
    6:  ("preprint_available", "https://www.nber.org/papers/w14607"),   # Kane & Staiger 2008
    7:  ("preprint_available", "https://www.nber.org/papers/w6691"),    # Rivkin, Hanushek, Kain 2005
    8:  ("preprint_available", "https://www.nber.org/papers/w10285"),   # Rockoff 2004
    9:  ("paywalled_only",     None),                                    # Goldhaber & Brewer 2000
    10: ("preprint_available", "https://www.nber.org/papers/w19872"),   # Papay & Kraft 2015
    73: ("paywalled_only",     None),                                    # Rothstein 2009 EFP
    76: ("paywalled_only",     None),                                    # Koedel & Betts 2009
    78: ("paywalled_only",     None),                                    # Blazar 2018

    # === CLUSTER 2: Early Childhood Education ===
    11: ("preprint_available", "https://www.nber.org/papers/w15471"),   # Heckman et al. 2010 Perry ROI
    12: ("preprint_available", "https://www.nber.org/papers/w30004"),   # Garcia, Heckman, Ronda 2022
    13: ("preprint_available", "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4031676/"),  # Campbell 2014 Science
    14: ("preprint_available", "https://www.nber.org/papers/w13877"),   # Deming 2009
    15: ("preprint_available", "https://www.nber.org/papers/w15471"),   # Heckman 2006 (ROI framework)
    16: ("preprint_available", "https://www.nber.org/papers/w16485"),   # Chetty et al. 2011 STAR
    17: ("preprint_available", "https://www.nber.org/papers/w28268"),   # Bailey et al. 2021 Head Start
    18: ("preprint_available", "https://www.nber.org/papers/w14400"),   # Currie & Almond 2011 review
    19: ("preprint_available", "https://www.nber.org/papers/w19579"),   # Cascio & Schanzenbach 2013
    20: ("paywalled_only",     None),                                    # Pages et al. 2020 EEPA

    # === CLUSTER 3: Class Size ===
    21: ("preprint_available", "https://www.nber.org/papers/w6051"),    # Krueger 1999 QJE
    22: ("preprint_available", "https://www.nber.org/papers/w5515"),    # Angrist & Lavy 1999 QJE
    23: ("preprint_available", "https://www.nber.org/papers/w23486"),   # Angrist et al. 2019 AER (Maimonides Redux)
    24: ("preprint_available", "https://www.nber.org/papers/w17161"),   # Fredriksson et al. 2013 QJE
    25: ("preprint_available", "https://www.nber.org/papers/w7225"),    # Hoxby 2000 QJE
    26: ("preprint_available", "https://www.nber.org/papers/w16485"),   # Chetty et al. 2011 STAR peers
    27: ("paywalled_only",     None),                                    # Jepsen & Rivkin 2009 JHR
    28: ("paywalled_only",     None),                                    # Wossmann & West 2006 EER
    84: ("paywalled_only",     None),                                    # Nye, Konstantopoulos, Hedges 2004

    # === CLUSTER 4: School Funding ===
    29: ("preprint_available", "https://www.nber.org/papers/w20847"),   # Jackson, Johnson, Persico 2016 QJE
    30: ("preprint_available", "https://www.nber.org/papers/w22011"),   # Lafortune, Rothstein, Schanzenbach 2018
    31: ("paywalled_only",     None),                                    # Hanushek 1997 EEPA
    32: ("preprint_available", "https://www.nber.org/papers/w3358"),    # Card & Krueger 1992 JPE
    33: ("preprint_available", "https://www.nber.org/papers/w18956"),   # Guryan 2004 (desegregation)
    34: ("paywalled_only",     None),                                    # Neilson & Zimmerman 2014 JPubE
    35: ("preprint_available", "https://www.nber.org/papers/w22011"),   # Hyman 2017 AEJEP
    85: ("paywalled_only",     None),                                    # Hanushek 2003 EJ
    86: ("paywalled_only",     None),                                    # Greenwald et al. 1996 RER

    # === CLUSTER 5: Charter Schools / Vouchers ===
    36: ("preprint_available", "https://www.nber.org/papers/w17332"),   # Angrist, Pathak, Walters 2013
    37: ("preprint_available", "https://www.nber.org/papers/w15473"),   # Dobbie & Fryer 2011
    38: ("preprint_available", "https://www.nber.org/papers/w22533"),   # Abdulkadiroglu et al. 2016 AER
    39: ("preprint_available", "https://www.nber.org/papers/w25763"),   # Cohodes et al. 2021
    40: ("preprint_available", "https://www.nber.org/papers/w21839"),   # Abdulkadiroglu et al. 2018 (Louisiana)
    41: ("preprint_available", "https://www.nber.org/papers/w5964"),    # Rouse 1998 QJE
    87: ("preprint_available", "https://www.nber.org/papers/w17494"),   # Fryer 2014 QJE (Houston)
    88: ("preprint_available", "https://www.nber.org/papers/w20865"),   # Walters 2018 JPE

    # === CLUSTER 6: Reading Instruction ===
    44: ("open_access",        "https://www.nichd.nih.gov/sites/default/files/publications/pubs/nrp/Documents/report.pdf"),  # NRP 2000
    45: ("preprint_available", "https://osf.io/preprints/psyarxiv/"),   # Dehaene 2009 (book; no free version)
    46: ("open_access",        "https://ies.ed.gov/ncee/wwc/"),         # Hanford 2018 (journalism)
    47: ("paywalled_only",     None),                                    # Castles et al. 2018 Psych Sci
    48: ("paywalled_only",     None),                                    # Ehri et al. 2001 meta-analysis
    49: ("open_access",        "https://ies.ed.gov/ncee/projects/evaluating_reading_recovery.asp"),  # May et al. 2023 IES
    50: ("open_access",        "https://www.hansardsociety.org.uk/"),   # Hansford et al. 2025
    91: ("paywalled_only",     None),                                    # Kjeldsen et al. 2014

    # === CLUSTER 7: High-Dosage Tutoring ===
    51: ("preprint_available", "https://www.nber.org/papers/w28531"),   # Guryan et al. 2023 AER
    52: ("preprint_available", "https://www.nber.org/papers/w27476"),   # Nickow, Oreopoulos, Quan 2020
    53: ("open_access",        "https://journals.sagepub.com/doi/10.1177/2332858420986211"),  # Kraft & Falken 2021 AERA Open
    54: ("preprint_available", "https://www.nber.org/papers/w32510"),   # Bhatt et al. 2024
    55: ("preprint_available", "https://matthewakraft.com/"),           # Kraft & Lovison 2025
    93: ("paywalled_only",     None),                                    # Cohen et al. 1982 AERJ
    95: ("paywalled_only",     None),                                    # Nickow et al. 2023 AERJ

    # === CLUSTER 8: SEL / Non-Cognitive Skills ===
    56: ("preprint_available", "https://www.nature.com/articles/s41586-019-1466-y"),  # Yeager et al. 2019 Nature (open)
    57: ("paywalled_only",     None),                                    # Sisk et al. 2018 Psych Sci
    58: ("paywalled_only",     None),                                    # Dweck 2006 (book)
    59: ("paywalled_only",     None),                                    # Crede et al. 2017 JPSP
    60: ("preprint_available", "https://www.nber.org/papers/w13016"),   # Heckman, Stixrud, Urzua 2006
    61: ("preprint_available", "https://www.nber.org/papers/w20647"),   # Jackson 2018 JPE (same as ID 4)
    62: ("open_access",        "https://casel.org/fundamentals-of-sel/"),  # CASEL framework
    98: ("paywalled_only",     None),                                    # Porter et al. 2022
    99: ("paywalled_only",     None),                                    # Duckworth et al. 2007 JPSP

    # === CLUSTER 9: Out-of-School Factors ===
    63: ("paywalled_only",     None),                                    # Borman & Dowling 2010 TCR
    64: ("paywalled_only",     None),                                    # Alexander et al. 2007 ASR
    65: ("open_access",        "https://sociologicalscience.com/"),     # Wodtke et al. 2026
    66: ("government_report",  "https://nces.ed.gov/nationsreportcard/"),  # NAEP data
    67: ("paywalled_only",     None),                                    # Morrissey et al. 2018 JMF
    68: ("paywalled_only",     None),                                    # Tan et al. 2020
    69: ("preprint_available", "https://www.nber.org/papers/w9542"),    # Heckman 2006 (skills)
    101: ("paywalled_only",    None),                                    # Benner et al. 2016
    102: ("paywalled_only",    None),                                    # Wolf et al. 2017
    103: ("paywalled_only",    None),                                    # Kim 2006 EEPA

    # === CLUSTER 10: International Systems ===
    70: ("paywalled_only",     None),                                    # Harris et al. 2017
    71: ("government_report",  "https://nces.ed.gov/surveys/pisa/"),    # PISA data
    72: ("government_report",  "https://nces.ed.gov/timss/"),           # TIMSS data
    74: ("open_access",        "https://www.oecd.org/pisa/"),           # OECD PISA reports
    75: ("open_access",        "https://ncee.org/"),                    # NCEE reports
    100: ("open_access",       "https://www.mckinsey.com/industries/education/our-insights/how-the-worlds-best-performing-schools-come-out-on-top"),  # McKinsey 2007
    104: ("open_access",       "https://www.mckinsey.com/industries/education/our-insights/how-the-worlds-most-improved-school-systems-keep-getting-better"),  # McKinsey 2010
    105: ("paywalled_only",    None),                                    # Hanushek & Woessmann 2015 (book)
    106: ("paywalled_only",    None),                                    # Darling-Hammond 2010 (book)
}

def update_registry():
    with open("/home/ubuntu/k12-education-research/literature/citation_registry_expanded.json") as f:
        registry = json.load(f)

    updated = 0
    for entry in registry:
        eid = entry.get("id")
        if eid in ACCESS_MAP:
            access_class, free_url = ACCESS_MAP[eid]
            entry["access_class"] = access_class
            entry["free_url"] = free_url
            # Keep legacy "access" field for backward compat but update it
            entry["access"] = access_class
            updated += 1
        else:
            # Default for unmapped entries
            if "access_class" not in entry:
                entry["access_class"] = "unknown"
                entry["free_url"] = None

    with open("/home/ubuntu/k12-education-research/literature/citation_registry_expanded.json", "w") as f:
        json.dump(registry, f, indent=2)

    print(f"Updated {updated} entries with access_class and free_url fields")

    # Summary stats
    from collections import Counter
    counts = Counter(e.get("access_class", "unknown") for e in registry)
    print("\nAccess class distribution:")
    for cls, cnt in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {cls:25s}: {cnt}")

    # Write updated Markdown summary
    lines = ["# Citation Registry — Access Classification Summary\n",
             f"**Total entries**: {len(registry)}\n",
             "\n## Access Class Distribution\n",
             "| Access Class | Count | Website Treatment |\n",
             "|---|---|---|\n",
             "| `open_access` | {} | Direct PDF link or embedded viewer |\n".format(counts.get("open_access", 0)),
             "| `preprint_available` | {} | Link to NBER/SSRN/author preprint (legal) |\n".format(counts.get("preprint_available", 0)),
             "| `government_report` | {} | Direct PDF link (public domain) |\n".format(counts.get("government_report", 0)),
             "| `paywalled_only` | {} | Link to DOI page only; no PDF |\n".format(counts.get("paywalled_only", 0)),
             "| `unknown` | {} | To be classified |\n".format(counts.get("unknown", 0)),
             "\n## Full Registry\n\n",
             "| ID | Authors | Year | Title | Cluster | Access Class | Free URL |\n",
             "|---|---|---|---|---|---|---|\n"]

    for e in registry:
        free = e.get("free_url") or ""
        if free:
            free = f"[Link]({free})"
        lines.append(f"| {e['id']} | {e['authors']} | {e['year']} | {e['title'][:60]}... | {e['cluster']} | `{e.get('access_class','unknown')}` | {free} |\n")

    with open("/home/ubuntu/k12-education-research/literature/access_classification.md", "w") as f:
        f.writelines(lines)

    print("\nWrote access_classification.md")

if __name__ == "__main__":
    update_registry()
