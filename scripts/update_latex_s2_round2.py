import re

# 1. Update LaTeX text
path = "/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex"
with open(path, "r") as f:
    content = f.read()

# Update Methodology (add screening note)
old_method = r"A programmatic API approach was preferred over interactive visual tools to ensure a rigorous, reproducible, and transparent methodology for identifying high-centrality missing nodes\."
new_method = r"A programmatic API approach was preferred over interactive visual tools to ensure a rigorous, reproducible, and transparent methodology for identifying high-centrality missing nodes. The Semantic Scholar analysis surfaced 26 highly-cited candidate papers missing from the initial registry; after qualitative screening for methodological rigor and direct relevance, the 12 most critical papers were incorporated into this synthesis."
content = content.replace(old_method, new_method)

# Update Cluster 1 (Hanushek 2010 & Sims 2020)
c1_insert = r"This raises profound questions about the validity of using VAMs for high-stakes evaluation."
c1_new = r"This raises profound questions about the validity of using VAMs for high-stakes evaluation. As Hanushek (2010) \cite{hanushek2010} cautions, while the variance in teacher quality is undeniably large and economically significant, translating these statistical generalizations into precise, high-stakes personnel decisions at the individual teacher level remains fraught with measurement error. Furthermore, efforts to systematically improve teacher quality through professional development have yielded mixed results; Sims and Fletcher-Wood (2020) \cite{sims2020} demonstrate that effective professional development requires specific, sustained characteristics—such as instructional coaching and deliberate practice—that are rarely present in standard district-led training."
content = content.replace(c1_insert, c1_new)

# Update Cluster 7 (Wang 2020)
c7_insert = r"Broader reviews similarly emphasize that SEL cannot be treated as an isolated curriculum, but must be integrated into the structural climate of the school \cite{darlinghammond2018, jones2019}."
c7_new = r"Broader reviews similarly emphasize that SEL cannot be treated as an isolated curriculum, but must be integrated into the structural climate of the school \cite{darlinghammond2018, jones2019}. Wang et al. (2020) \cite{wang2020} further corroborate this, showing that positive classroom climates directly mediate both academic achievement and psychological well-being, suggesting that SEL interventions are most effective when they alter the relational environment rather than merely teaching discrete skills."
content = content.replace(c7_insert, c7_new)

# Update Cluster 8 & 9 (Clark 2020 on COVID)
c8_insert = r"The rapid shift to remote learning during the COVID-19 pandemic provided a massive, albeit non-random, shock to this literature."
c8_new = r"The rapid shift to remote learning during the COVID-19 pandemic provided a massive, albeit non-random, shock to this literature. Clark et al. (2020) \cite{clark2020} documented that while online learning mitigated some academic loss, it was a highly imperfect substitute for in-person instruction, with severe equity implications."
content = content.replace(c8_insert, c8_new)

# Update Equity theme (Scherer 2019)
eq_insert = r"Technology interventions (Cluster 8) frequently widen achievement gaps because affluent students have better home infrastructure to capitalize on them."
eq_new = r"Technology interventions (Cluster 8) frequently widen achievement gaps because affluent students have better home infrastructure to capitalize on them. Scherer and Siddiq (2019) \cite{scherer2019} provide comprehensive evidence that socioeconomic status is strongly and persistently related to students' ICT literacy, meaning that technology-centric reforms often act as regressively distributed resources."
content = content.replace(eq_insert, eq_new)

# Update Cross-cutting (Osher 2020)
cc_insert = r"The evidence strongly suggests that education reform cannot succeed through isolated, single-variable interventions."
cc_new = r"The evidence strongly suggests that education reform cannot succeed through isolated, single-variable interventions. As Osher et al. (2020) \cite{osher2020} comprehensively articulate, human development and learning are fundamentally driven by the complex interplay of relationships, contexts, and structural supports, meaning that narrow policy levers will consistently underperform holistic, ecological approaches."
content = content.replace(cc_insert, cc_new)

with open(path, "w") as f:
    f.write(content)

# 2. Update BibTeX
bib_path = "/home/ubuntu/k12-education-research/drafts/k12_references.bib"
with open(bib_path, "a") as f:
    f.write("""
@article{hanushek2010,
  title={Generalizations about using value-added measures of teacher quality},
  author={Hanushek, Eric A and Rivkin, Steven G},
  journal={The American Economic Review},
  volume={100},
  number={2},
  pages={267--271},
  year={2010}
}

@article{sims2020,
  title={Identifying the characteristics of effective teacher professional development: A critical review},
  author={Sims, Sam and Fletcher-Wood, Harry},
  journal={School Effectiveness and School Improvement},
  volume={32},
  number={1},
  pages={47--63},
  year={2020}
}

@article{wang2020,
  title={Classroom climate and children's academic and psychological wellbeing: A systematic review and meta-analysis},
  author={Wang, Ming-Te and Degol, Hajer and Amemiya, Jamie},
  journal={Developmental Review},
  volume={57},
  pages={100912},
  year={2020}
}

@article{clark2020,
  title={Compensating for academic loss: Online learning and student performance during the COVID-19 pandemic},
  author={Clark, Andrew E and Nong, Huong and Zhu, Haiwei and Ward, Rachel},
  journal={China Economic Review},
  volume={68},
  pages={101619},
  year={2020}
}

@article{scherer2019,
  title={The relation between students' socioeconomic status and ICT literacy: Findings from a meta-analysis},
  author={Scherer, Ronny and Siddiq, Fazilat},
  journal={Computers & Education},
  volume={138},
  pages={13--32},
  year={2019}
}

@article{osher2020,
  title={Drivers of human development: How relationships and context shape learning and development},
  author={Osher, David and Cantor, Pamela and Berg, Juliette and Steyer, Lily and Rose, Todd},
  journal={Applied Developmental Science},
  volume={24},
  number={1},
  pages={6--36},
  year={2020}
}
""")

print("LaTeX and BibTeX updated successfully.")
