import re

path = "/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex"
with open(path, "r") as f:
    content = f.read()

# 1. Update Methodology
old_method = r"\\textbf\{ResearchRabbit\} and \\textbf\{Elicit\} were integrated for citation network analysis and automated literature screening\."
new_method = r"\\textbf{Semantic Scholar} (via programmatic API) and \\textbf{Elicit} were integrated for citation network analysis and automated literature screening. A programmatic API approach was preferred over visual UI tools (like ResearchRabbit) to ensure a rigorous, reproducible, and transparent methodology for identifying high-centrality missing nodes."
content = re.sub(old_method, new_method, content)

# 2. Update Cluster 2 (Early Childhood Ed)
c2_insert = r"This long-term fadeout puzzle has motivated the replication agenda in this domain."
c2_new = r"This long-term fadeout puzzle has motivated the replication agenda in this domain. Recent evidence from universal pre-K scale-ups provides crucial context: Gray-Lobe et al. (2021) \cite{graylobe2021} found that while Boston's universal preschool program did not raise state test scores, it significantly increased high school graduation and college enrollment, suggesting that early childhood interventions may operate primarily through non-cognitive channels rather than sustained cognitive gains."
content = content.replace(c2_insert, c2_new)

# 3. Update Cluster 7 (SEL & Non-cognitive)
c7_insert = r"Subsequent meta-analyses have largely confirmed these effects, though with significant heterogeneity depending on implementation fidelity \cite{taylor2017}."
c7_new = r"Subsequent meta-analyses have largely confirmed these effects, though with significant heterogeneity depending on implementation fidelity \cite{taylor2017}. The role of school climate and teacher mindsets in mediating these interventions has also emerged as critical; as Yeager et al. (2021) \cite{yeager2020} and Yeager and Dweck (2020) \cite{yeager2020controversies} demonstrate, growth-mindset interventions often fail to replicate when delivered in unsupportive classroom environments or by teachers with fixed mindsets. Broader reviews similarly emphasize that SEL cannot be treated as an isolated curriculum, but must be integrated into the structural climate of the school \cite{darlinghammond2018, jones2019}."
content = content.replace(c7_insert, c7_new)

# 4. Update Cluster 9 (Out-of-School)
c9_insert = r"Suspensions, in particular, show strong negative correlations with long-term attainment \cite{skiba2014}."
c9_new = r"Suspensions, in particular, show strong negative correlations with long-term attainment \cite{skiba2014}. The causal impact of these disciplinary policies has been further clarified by Bacher-Hicks et al. (2019) \cite{bacherhicks2019}, who demonstrated that strict-discipline schools directly increase the likelihood of later adult arrests and incarceration—the so-called 'school-to-prison pipeline'—independent of student baseline characteristics."
content = content.replace(c9_insert, c9_new)

with open(path, "w") as f:
    f.write(content)
print("LaTeX updated successfully.")
