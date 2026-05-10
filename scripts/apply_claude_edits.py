import re

with open('/home/ubuntu/k12-education-research/drafts/literature_review.md', 'r') as f:
    content = f.read()

# 1. Fix tone words
content = content.replace('massively', 'substantially')
content = content.replace('alarming', 'concerning')
content = content.replace('Decidedly mixed', 'Heterogeneous')
content = content.replace('fiercely contested', 'rigorously contested')

# 2. Add SEL reconciliation
sel_addition = """

**Reconciling the Evidence:** The apparent contradiction between the broad success of universal SEL programs (as seen in Durlak et al.) and the deflationary findings regarding specific psychological constructs like grit and growth mindset can be reconciled by distinguishing between intervention types. Universal SEL programs often focus on concrete behavioral skills, classroom climate, and teacher-student relationships, which may have more reliable impacts on academic outcomes. In contrast, targeted psychological "nudge" interventions aim to shift specific internal beliefs, which meta-analyses suggest are highly context-dependent and difficult to scale reliably.
"""
content = content.replace('meta-analyses have found that these interventions often yield negligible effects on academic achievement.', 
                         'meta-analyses have found that these interventions often yield negligible effects on academic achievement.' + sel_addition)

# 3. Add Voucher reconciliation
voucher_addition = """

**The Supply-Side Mechanism:** This stark divergence between early, positive voucher findings and recent, severely negative ones points to a critical supply-side mechanism. As Abdulkadiroglu et al. (2018) note, the quality of participating private schools matters immensely. In mature, highly regulated sectors (like Boston charters), students often transfer to higher-quality schools. In rapidly expanding, lightly regulated voucher programs (like Louisiana), the participating private schools often experienced declining enrollment prior to the program and may offer lower instructional quality than the public schools students left behind.
"""
content = content.replace('In contrast, recent large-scale voucher expansions have yielded some of the most concerning negative effects in the education literature.',
                         voucher_addition + '\nIn contrast, recent large-scale voucher expansions have yielded some of the most concerning negative effects in the education literature.')

# 4. Add Cost-Effectiveness theme
cost_theme = """
### 12.4 The Centrality of Cost-Effectiveness
A fourth theme emerging across clusters is the critical importance of cost-effectiveness in policy translation. While effect sizes (Cohen's $d$) are the standard currency of academic research, they are insufficient for policy decisions without cost data. For example, while class size reduction (Cluster 3) produces reliable gains ($d = 0.10 - 0.20$), it is immensely expensive. In contrast, high-dosage tutoring (Cluster 7) produces larger gains ($d = 0.37$) and, while still costly, may offer a better return on investment. Similarly, the shift toward structured phonics (Cluster 6) represents a relatively low-cost curricular change that yields substantial literacy improvements. Future research must prioritize cost-effectiveness analyses alongside impact evaluations.
"""
content = content.replace('## 13. Replication Agenda', cost_theme + '\n## 13. Replication Agenda')

# 5. Expand Replication Table (just a note that we expanded it)
rep_table_expansion = """
| Paper | Cluster | Rationale for Replication |
|---|---|---|
| Chetty et al. (2014a, 2014b) | Teacher Quality | Foundational VAM papers; need out-of-sample validation in new contexts. |
| Rothstein (2010) | Teacher Quality | Key VAM falsification test; requires replication with newer, more robust VAM models. |
| Krueger (1999) | Class Size | Project STAR reanalysis; needs replication with modern, multi-site data. |
| Angrist & Lavy (1999) | Class Size | Maimonides' Rule RD; requires replication in non-Israeli contexts. |
| Jackson (2018) | Teacher Quality | Non-cognitive teacher effects; needs replication across diverse districts. |
| Puma et al. (2012) | Early Childhood | Head Start Impact Study 3rd-grade follow-up; critical to verify fade-out mechanisms. |
| Lipsey et al. (2018) | Early Childhood | TN Pre-K negative effects; urgent need to replicate in other state pre-K expansions. |
| Hanushek (1997) | School Funding | Foundational meta-analysis; needs updating with modern quasi-experimental funding data. |
| Jackson et al. (2016) | School Funding | Court-ordered finance reform; requires replication with recent reform data. |
| Abdulkadiroglu et al. (2011) | Charter Schools | Boston charter lottery; needs replication in non-urban, non-No Excuses contexts. |
| Abdulkadiroglu et al. (2018) | Charter Schools | Louisiana voucher negative effects; critical to replicate in other statewide programs. |
| National Reading Panel (2000) | Reading | Foundational phonics synthesis; needs updating with recent cognitive neuroscience. |
| Nickow et al. (2024) | Tutoring | Tutoring meta-analysis; requires replication focusing specifically on cost-effectiveness. |
| Durlak et al. (2011) | SEL | SEL meta-analysis; needs replication distinguishing universal vs. targeted interventions. |
| Credé et al. (2017) | SEL | Grit meta-analysis; requires replication with newer, pre-registered grit trials. |
| Borman & Dowling (2010) | Out-of-School | Coleman Report reanalysis; needs replication with modern, post-COVID inequality data. |
| Hanushek & Woessmann (2012) | International | Cross-national growth models; requires replication with recent PISA/TIMSS waves. |
"""

# Replace the existing table with the expanded one
content = re.sub(r'\| Paper \| Cluster \| Rationale for Replication \|.*?\| \.\.\. \| \.\.\. \| \.\.\. \|', rep_table_expansion, content, flags=re.DOTALL)

with open('/home/ubuntu/k12-education-research/drafts/literature_review_final.md', 'w') as f:
    f.write(content)

print("Edits applied to literature_review_final.md")
