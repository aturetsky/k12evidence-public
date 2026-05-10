import re

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'r') as f:
    content = f.read()

# Fix the duplicate content at the end of the file first
content = re.sub(r"\\end\{document\}.*", r"\\end{document}", content, flags=re.DOTALL)

# Expand Teacher Quality
content = content.replace(
    r"\subsection{The Value-Added Debate}",
    r"The magnitude of these effects is profound. To put $d = 0.15$ in perspective, a student assigned to a 75th percentile teacher rather than a 25th percentile teacher for three consecutive years would likely close the average black-white achievement gap. This realization shifted the focus of education reform in the early 2000s heavily toward teacher evaluation and accountability.\n\n\subsection{The Value-Added Debate}"
)

# Expand Early Childhood
content = content.replace(
    r"The reconciliation of short-term test score fadeout with long-term life outcome improvements remains a central theoretical challenge, likely mediated by non-cognitive skill development.",
    r"The reconciliation of short-term test score fadeout with long-term life outcome improvements remains a central theoretical challenge. \citet{heckman2006} has argued extensively that the primary mechanism is the development of non-cognitive skills---such as self-regulation, conscientiousness, and executive function---which are highly malleable in early childhood and predict adult success better than raw cognitive scores. If early childhood programs successfully build these non-cognitive traits, the long-term benefits may manifest in reduced criminality and higher employment even if the initial cognitive boost dissipates."
)

# Expand School Funding
content = content.replace(
    r"\subsection{The ``Does Money Matter?'' Debate}",
    r"The historical context is critical: prior to the 1990s, school funding in the US was overwhelmingly tied to local property taxes, resulting in massive disparities between wealthy and poor districts. Early attempts to measure the impact of these disparities using cross-sectional data often yielded null results, largely because wealthy districts face different educational challenges than poor districts, confounding simple observational correlations.\n\n\subsection{The ``Does Money Matter?'' Debate}"
)

# Expand Reading Instruction
content = content.replace(
    r"\subsection{Intervention Fadeout: The Case of Reading Recovery}",
    r"The policy implications of this consensus are profound. Despite the clear evidence favoring systematic phonics, surveys of teacher preparation programs frequently find that balanced literacy and whole-language approaches remain dominant in curricula. This disconnect between the evidence base and classroom practice represents one of the most significant translational failures in education policy.\n\n\subsection{Intervention Fadeout: The Case of Reading Recovery}"
)

# Expand High-Dosage Tutoring
content = content.replace(
    r"\subsection{Implementation Parameters}",
    r"The success of the Chicago program demonstrated that high-dosage tutoring can serve as a powerful remedial tool even for students who are multiple grade levels behind. Crucially, the intervention was tightly structured, using a specific curriculum and frequent formative assessments to guide instruction, rather than relying on unstructured homework help.\n\n\subsection{Implementation Parameters}"
)

# Expand Out-of-School Factors
content = content.replace(
    r"\subsection{Neighborhood and Family Poverty}",
    r"The profound influence of out-of-school factors presents a structural limit on the capacity of schools to close achievement gaps independently. While high-quality schools can significantly alter student trajectories, they operate within a broader ecosystem of inequality that begins at birth.\n\n\subsection{The Income-Achievement Gap and Parental Investment}\nRecent decades have seen a massive widening of the income-achievement gap. \citet{reardon2011} demonstrated that the achievement gap between children from high- and low-income families is roughly 30 to 40 percent larger among children born in 2001 than among those born twenty-five years earlier. This divergence is driven largely by disparities in parental investment, particularly early childhood enrichment activities and summer learning opportunities, rather than purely school-based factors.\n\n\subsection{COVID-19 Learning Loss}\nThe COVID-19 pandemic provided a stark, involuntary natural experiment in the effects of out-of-school time. \citet{goldhaber2022} and others have documented historic declines in NAEP scores, with the severest impacts concentrated among low-income students and those in districts that maintained remote instruction for longer periods. This catastrophic learning loss underscores the critical, equalizing function that physical schools perform, despite their inability to fully close out-of-school gaps.\n\n\subsection{Neighborhood and Family Poverty}"
)

# Expand International Systems
content = content.replace(
    r"\subsection{System-Level Drivers}",
    r"While the US context is unique, international comparisons provide crucial benchmarks for what is possible when education systems are designed coherently at the national level.\n\n\subsection{System-Level Drivers}"
)

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'w') as f:
    f.write(content)

