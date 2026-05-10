import re

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'r') as f:
    content = f.read()

# 1. Fix jackson2016
content = content.replace(
    r"They found that a 10\% increase in per-pupil spending across all 12 school years led to approximately 7\% higher adult wages and a 3.2 percentage point reduction in adult poverty (published \textit{QJE} estimates). Crucially, effects for children from low-income families were substantially larger---approximately 9.6\% wage gains and a 6.1 percentage point poverty reduction",
    r"They found that a 10\% increase in per-pupil spending across all 12 school years led to approximately 7.25\% higher adult wages, a 9.5 percentage point higher probability of graduating high school, and a 3.67 percentage point reduction in adult poverty (published \textit{QJE} estimates). Crucially, effects for children from low-income families were substantially larger---approximately 9.5\% wage gains, an 11.6 percentage point increase in high school graduation, and a 6.8 percentage point poverty reduction"
)

# 2. Fix lafortune2018
content = content.replace(
    r"\citet{lafortune2018} showed that post-1990 finance reforms significantly increased achievement in low-income districts relative to high-income districts, effectively closing a portion of the achievement gap.",
    r"\citet{lafortune2018} showed that post-1990 finance reforms significantly increased per-pupil spending in low-income districts by approximately \$1,200 per year and raised test scores in those districts by approximately 0.10 standard deviations over ten years, effectively closing a portion of the achievement gap."
)

# 3. Fix nickow2020
content = content.replace(
    r"\citet{nickow2020} synthesized recent experimental evidence, finding that high-dosage tutoring (defined as three or more sessions per week) produces average effect sizes of $d = 0.37$ in math and $d = 0.26$ in reading.",
    r"\citet{nickow2020} synthesized recent experimental evidence across 96 tutoring studies, finding that tutoring programs produce a pooled average effect size of $d = 0.37$ on learning outcomes."
)

# 4. Fix sisk2018
content = content.replace(
    r"Similarly, \citet{sisk2018} found that growth mindset interventions produce very small overall effects ($d = 0.08$ for intervention studies), with the largest effects concentrated in low-income and high-risk student populations.",
    r"Similarly, \citet{sisk2018} found that growth mindset interventions produce very small overall effects ($d = 0.08$ for intervention studies). While effects were larger for high-risk student populations, the authors noted these results should be interpreted with caution due to the small number of effect sizes and non-significant moderator comparisons."
)

# 5. Fix alexander2007
content = content.replace(
    r"\citet{alexander2007} demonstrated that the ``summer slide'' accounts for a substantial share of the reading achievement gap by the end of elementary school, with low-income students losing ground during the summer while higher-income students maintain or improve their skills.",
    r"\citet{alexander2007} demonstrated that the ``summer slide'' accounts for approximately two-thirds of the 9th-grade reading achievement gap between high- and low-income students, with low-income students losing ground during the summer while higher-income students maintain or improve their skills."
)

# 6. Fix mourshed2010
content = content.replace(
    r"Similarly, \citet{mourshed2010} found that the most improved school systems globally share common features: strong teacher recruitment and training, data-driven instruction, and sustained political commitment.",
    r"Similarly, \citet{mourshed2010} found that improving school systems adopt interventions appropriate to their specific performance stage (e.g., basic literacy and numeracy for poor-to-fair systems, versus professionalizing teaching for good-to-great systems), while sharing a common reliance on the continuity of new leadership to sustain reform."
)

# 7. Update AI Declaration
content = content.replace(
    r"\textbf{Claude} (Anthropic) and \textbf{Gemini} (Google) were used for independent editorial review, structural critique, and internal consistency checks.",
    r"\textbf{Claude} (Anthropic) and \textbf{Gemini} (Google) were used for independent editorial review, structural critique, and internal consistency checks. Specifically, Claude was provided with direct API access to the full text of source PDFs to conduct grounded verification of quantitative claims against the original papers."
)

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'w') as f:
    f.write(content)
print("Corrections applied.")
