with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'r') as f:
    content = f.read()

old_text = r"""The question of whether ``money matters'' in education has been central to education economics since the Coleman Report (1966), which famously concluded that school resources had little independent effect on student achievement compared to family background. This conclusion was enormously influential, shaping decades of education policy and providing intellectual cover for persistent funding inequities between wealthy and poor districts.

\subsection{Historical Context and the Funding Equity Problem}
The historical context is critical: prior to the 1990s, school funding in the US was overwhelmingly tied to local property taxes, resulting in massive disparities between wealthy and poor districts. In many states, per-pupil spending in the wealthiest districts was two to three times higher than in the poorest districts. Early attempts to measure the impact of these disparities using cross-sectional data often yielded null results, largely because wealthy districts face different educational challenges than poor districts, confounding simple observational correlations. A wealthy suburban district with high spending and high test scores is not a valid counterfactual for a poor urban district with low spending and low test scores.

\subsection{The ``Does Money Matter?'' Debate}
For decades, the consensus was shaped by Hanushek's meta-analyses \citep{hanushek1997, hanushek2003}, which argued there was no consistent, statistically significant relationship between per-pupil expenditure and student achievement. However, this view was challenged by \citet{greenwald1996}, whose meta-analysis found significant positive effects, and the debate shifted decisively with the advent of quasi-experimental designs evaluating court-ordered school finance reforms."""

new_text = r"""The question of whether ``money matters'' in education has been central to education economics for over half a century. For decades, the prevailing consensus was that it did not---a view built on two distinct pillars of research separated by thirty years: the Coleman Report in the 1960s and Hanushek's meta-analyses in the 1990s.

\subsection{The Origins of the Null-Effects Consensus}
The original skepticism regarding school funding stems from the Coleman Report (1966), a massive federally mandated study which famously concluded that measurable school resources had little independent effect on student achievement compared to a student's family background. This conclusion was enormously influential, providing intellectual cover for persistent funding inequities between wealthy and poor districts. 

This skepticism was later reinforced and formalized in the economics literature by Hanushek's influential meta-analyses \citep{hanushek1997, hanushek2003}. Reviewing decades of production-function studies, Hanushek argued there was no consistent, statistically significant relationship between per-pupil expenditure and student achievement. Together, Coleman and Hanushek cemented a powerful narrative: throwing money at schools is an inefficient way to improve outcomes.

\subsection{The Methodological Flaw in Early Research}
The historical context of school finance explains why these early studies failed to find an effect. Prior to the 1990s, US school funding was overwhelmingly tied to local property taxes, resulting in massive disparities. However, early attempts to measure the impact of these disparities relied on cross-sectional observational data, which is heavily confounded by selection bias. A wealthy suburban district with high spending and high test scores is not a valid counterfactual for a poor urban district with low spending and low test scores, because the student populations differ fundamentally. Similarly, state compensatory funding often directs \textit{more} money to districts with the \textit{lowest} achievement, creating a negative correlation between spending and test scores that masks any positive causal effect of the money itself.

\subsection{The Quasi-Experimental Revolution}
This null-effects consensus was initially challenged by \citet{greenwald1996}, whose competing meta-analysis found significant positive effects, but the debate only shifted decisively with the advent of modern quasi-experimental designs evaluating court-ordered school finance reforms."""

if old_text in content:
    content = content.replace(old_text, new_text)
    print("Cluster 4 opening rewritten successfully.")
else:
    print("Could not find the exact text to replace.")

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'w') as f:
    f.write(content)
