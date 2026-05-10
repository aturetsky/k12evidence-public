import os

latex_content = r"""\documentclass[12pt,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath,amssymb}
\usepackage{geometry}
\geometry{margin=1in, headheight=15pt}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{tabularx}
\usepackage{hyperref}
\hypersetup{colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=blue}
\usepackage{natbib}
\usepackage{setspace}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage{parskip}

\setlength{\parskip}{6pt}
\setlength{\parindent}{0pt}
\doublespacing

\pagestyle{fancy}
\fancyhf{}
\rhead{\thepage}
\lhead{\textit{K-12 Education Research: Evidence Synthesis}}

\title{\textbf{Drivers of Student Success in K-12 Education}\\[0.5em]
\Large A Systematic Synthesis of Causal Evidence}
\author{Avi Turetsky \and Manus AI}
\date{May 2026 --- Working Draft}

\begin{document}

\maketitle
\thispagestyle{empty}

\begin{abstract}
\noindent This document synthesizes the causal evidence across ten core domains of K-12 education research, drawing on a verified registry of 99 high-impact papers. We assess the magnitude and reliability of interventions including teacher quality, early childhood education, class size reduction, school funding, charter schools, reading instruction, high-dosage tutoring, social-emotional learning, out-of-school factors, and international system design. The synthesis highlights areas of strong consensus, areas of intense methodological debate, and domains where observational findings are often confounded by selection bias. We conclude by identifying high-priority replication candidates with publicly available data, proposing four cross-cutting themes that unify the evidence base, and cataloging instances where policy claims have exceeded empirical findings.

\vspace{1em}
\noindent \textbf{Methodological Note:} The citation registry underlying this synthesis was rigorously verified using AI-assisted workflows. Perplexity Computer was employed to fact-check effect sizes and verify paper existence across 10 verification batches, while Claude 3 Opus was utilized for editorial review and internal consistency checks. Elicit was considered for automated literature retrieval but ultimately not employed in favor of direct institutional access and manual verification.
\end{abstract}

\tableofcontents
\newpage

%% ============================================================
\section{Introduction}
%% ============================================================

The empirical literature on K-12 education policy is vast, politically salient, and methodologically heterogeneous. Over the past three decades, the field has undergone a ``credibility revolution,'' moving away from simple observational correlations toward rigorous causal identification strategies. However, despite this methodological progress, significant debates remain regarding the magnitude, persistence, and scalability of key interventions.

This document provides a structured synthesis of the causal evidence across ten core research clusters. It is built upon a systematically verified registry of 99 seminal papers, meta-analyses, and critical re-evaluations. For each cluster, we review the foundational findings, examine the prevailing methodological disputes, and synthesize the current state of the evidence, with explicit attention to effect sizes and their policy implications. Effect sizes throughout this document are reported as Cohen's $d$ (standard deviation units) unless otherwise noted.

%% ============================================================
\section{Methodological Framework}
%% ============================================================

Before examining specific substantive clusters, it is necessary to establish the methodological hierarchy used to evaluate evidence in this review. Education research is particularly susceptible to selection bias: students are not randomly assigned to schools, teachers, or neighborhoods, meaning that observational correlations rarely represent true causal effects.

\subsection{The Hierarchy of Causal Evidence}
This synthesis prioritizes research designs capable of isolating causal mechanisms, ranked roughly as follows:
\begin{enumerate}
    \item \textbf{Randomized Controlled Trials (RCTs):} The gold standard (e.g., Project STAR for class size), though often limited in scale or duration.
    \item \textbf{Natural Experiments and Lotteries:} Over-subscribed charter school lotteries \citep{abdulkadiroglu2011} provide RCT-equivalent evidence within specific sub-populations.
    \item \textbf{Regression Discontinuity (RD):} Exploiting arbitrary cutoffs (e.g., Maimonides' Rule for class size, \citealt{angrist1999}) to compare near-identical students on either side of a threshold.
    \item \textbf{Difference-in-Differences (DiD):} Analyzing the differential impact of policy rollouts across states or districts over time (e.g., school finance reforms, \citealt{jackson2016}).
    \item \textbf{Instrumental Variables (IV) and Value-Added Models (VAMs):} Using exogenous shocks or controlling for prior test scores to isolate teacher or school effects \citep{chetty2014a}.
\end{enumerate}

\subsection{Common Threats to Validity}
Even rigorous designs face significant threats to validity when translated to policy. \textbf{Scale-up effects} (general equilibrium effects) occur when an intervention works in a small trial but fails when implemented broadly due to supply constraints (e.g., the dilution of teacher quality in California's class size reduction, \citealt{jepsen2009}). \textbf{Fadeout} is another pervasive issue, particularly in early childhood interventions \citep{puma2012}, where initial cognitive gains dissipate within a few years, complicating cost-benefit analyses.

%% ============================================================
\section{Cluster 1: Teacher Quality and Value-Added Models}
%% ============================================================

The consensus in education economics is that teacher quality is the most important school-based determinant of student achievement. Foundational work by \citet{rivkin2005} and \citet{rockoff2004} demonstrated that a one standard deviation increase in teacher quality raises student test scores by approximately $d = 0.10$--$0.15$. Subsequent research using Project STAR data suggested even larger effects, with the gap between a 75th and 25th percentile teacher estimated at $d = 0.34$--$0.48$ \citep{nye2004}.

\subsection{The Value-Added Debate}
The central methodological debate in this cluster concerns the validity of Value-Added Models (VAMs) used to estimate teacher effectiveness. \citet{chetty2014a, chetty2014b} provided the most influential defense of VAMs, using data from 2.5 million students to argue that VAM estimates are unbiased predictors of teacher causal effects. They found that replacing a bottom-5\% teacher with an average teacher raises the lifetime earnings of a single classroom by approximately \$250,000.

However, this conclusion has been rigorously contested. \citet{rothstein2010} demonstrated that standard VAMs fail falsification tests---teachers appear to affect students' \textit{prior} test scores, indicating significant non-random sorting of students to teachers based on unobservable characteristics. While complex, multi-year models can reduce this bias \citep{koedel2010}, the instability of teacher rankings across different model specifications remains a major concern for high-stakes policy use.

\subsection{Non-Cognitive Teacher Effects}
Recent research has expanded the definition of teacher quality beyond test scores. \citet{jackson2018a} found that teachers have substantial effects on non-cognitive outcomes---such as attendance, behavior, and course grades---and that these non-test-score effects predict high school graduation and earnings even when a teacher's test-score value-added is low. \citet{blazar2018} confirmed through random assignment that teachers have causal impacts on student self-efficacy and behavior, though he cautioned against using these measures for formal evaluation.

\subsection{Policy Implications and Exceeded Claims}
The policy translation of VAM research frequently exceeds the empirical findings. The \citet{chetty2014b} \$250,000 lifetime earnings figure is routinely cited by policymakers to justify aggressive termination of low-performing teachers. However, the authors themselves explicitly cautioned against this interpretation, noting that high-stakes use of VAMs would likely induce teaching-to-the-test and alter the reliability of the metric (Goodhart's Law). The empirical reality is that while teacher quality matters immensely, our ability to measure it precisely enough for high-stakes personnel decisions remains highly contested.

%% ============================================================
\section{Cluster 2: Early Childhood Education}
%% ============================================================

Early childhood education (ECE) interventions are widely cited as having the highest return on investment in the education sector, though the evidence base reveals complex dynamics regarding the persistence of these effects.

\subsection{Long-Run Returns and the Fadeout Problem}
The foundational evidence for ECE relies heavily on small-scale, intensive interventions from the 1960s and 1970s. \citet{heckman2010a} demonstrated that the HighScope Perry Preschool Program produced a 7--12\% annual return on investment, with significant effects on crime reduction and earnings persisting to age 40. Similarly, the Abecedarian Project showed large improvements in adult health and metabolic outcomes \citep{campbell2014}.

However, modern, scaled-up public pre-K programs show a different pattern. The Head Start Impact Study \citep{puma2012} found that initial cognitive gains largely faded by 3rd grade. More concerningly, the Tennessee Voluntary Prekindergarten RCT \citep{lipsey2018} found that by 3rd grade, pre-K participants actually scored \textit{lower} than the control group on academic measures.

Despite short-term test score fadeout, quasi-experimental evaluations of historical Head Start rollouts \citep{bailey2021} and universal pre-K programs \citep{cascio2013} suggest significant long-term benefits for educational attainment and earnings, particularly for disadvantaged students. The reconciliation of short-term test score fadeout with long-term life outcome improvements remains a central theoretical challenge, likely mediated by non-cognitive skill development.

\subsection{Policy Implications and Exceeded Claims}
The rhetoric surrounding universal pre-K frequently conflates distinct programmatic models. Policymakers routinely cite the massive ROI of the Perry Preschool project to justify modern universal pre-K expansions. This is a severe extrapolation: Perry was a highly intensive, multi-year intervention targeting 58 deeply disadvantaged children, featuring weekly home visits and highly trained staff. Assuming that a modern, scaled-up state pre-K program (which often struggles with staff retention and quality control) will yield Perry-like returns is an analytical error. The Tennessee Pre-K findings \citep{lipsey2018} serve as a stark reminder that poor-quality ECE can be worse than no ECE at all.

%% ============================================================
\section{Cluster 3: Class Size Reduction}
%% ============================================================

The effect of class size on student achievement is one of the most heavily studied, yet persistently debated, topics in education policy.

\subsection{Experimental and Quasi-Experimental Evidence}
The strongest causal evidence comes from the Tennessee STAR experiment. \citet{krueger1999} reanalysis found that students randomly assigned to small classes (13--17 students) outperformed those in regular classes (22--25 students) by approximately $d = 0.20$ in early grades, with larger effects for minority students. Long-term follow-ups \citep{chetty2011} showed that small class assignment in kindergarten translated to roughly \$1,000 higher annual earnings at age 27.

Outside of experimental settings, \citet{angrist1999} used Maimonides' Rule in Israel as a natural experiment, finding that class size reductions significantly improved reading and math scores. Similarly, \citet{fredriksson2013} used a regression discontinuity design in Sweden to show that one fewer student per class raised adult earnings by approximately 3\%.

\subsection{Cost-Effectiveness and General Equilibrium Effects}
Despite these positive findings, widespread implementation of class size reduction has proven problematic. \citet{jepsen2009} showed that California's massive class size reduction initiative yielded near-zero net benefits for disadvantaged students. The sudden demand for new teachers led wealthy districts to poach experienced teachers from poorer districts, forcing the latter to hire uncertified instructors. This general equilibrium effect entirely negated the structural benefit of smaller classes. Furthermore, cross-national analyses \citep{wossmann2006} find inconsistent and generally small effects of class size across different education systems.

\subsection{Policy Implications}
Class size reduction is popular with parents and teachers but ranks poorly on cost-effectiveness metrics. Given the massive expense of hiring additional teachers and building new classrooms, interventions like high-dosage tutoring (discussed in Cluster 7) are increasingly viewed as more efficient mechanisms for delivering individualized attention.

%% ============================================================
\section{Cluster 4: School Funding and Resources}
%% ============================================================

The question of whether ``money matters'' in education has been central to education economics since the Coleman Report (1966), which famously concluded that school resources had little independent effect on student achievement compared to family background.

\subsection{The ``Does Money Matter?'' Debate}
For decades, the consensus was shaped by Hanushek's meta-analyses \citep{hanushek1997, hanushek2003}, which argued there was no consistent, statistically significant relationship between per-pupil expenditure and student achievement. However, this view was challenged by \citet{greenwald1996}, whose meta-analysis found significant positive effects.

The debate shifted decisively with the advent of quasi-experimental designs evaluating court-ordered school finance reforms. \citet{jackson2016} provided the most compelling evidence, demonstrating that a 10\% increase in per-pupil spending across all 12 school years led to 7\% higher adult wages and a 3.7 percentage point reduction in adult poverty. Crucially, these effects were two to three times larger for low-income students.

\subsection{Mechanisms and Distributional Impacts}
Recent studies consistently confirm that targeted funding increases improve outcomes. \citet{lafortune2018} showed that post-1990 finance reforms significantly increased achievement in low-income districts relative to high-income districts, effectively closing a portion of the achievement gap. \citet{hyman2017} found that Michigan's finance reform raised college enrollment and graduation rates. The mechanisms driving these improvements typically include reductions in class size, increases in teacher salaries (which attract better candidates), and capital improvements \citep{neilson2014}.

\subsection{Policy Implications}
The debate is no longer \textit{whether} money matters, but \textit{how} it is spent. Unrestricted block grants often yield lower returns than funds explicitly targeted toward instructional quality or high-need populations.

%% ============================================================
\section{Cluster 5: Charter Schools and Vouchers}
%% ============================================================

Research on school choice---encompassing charter schools and voucher programs---reveals highly heterogeneous effects that depend heavily on the specific model and regulatory environment.

\subsection{The ``No Excuses'' Charter Model}
The most robust positive findings in the charter literature come from urban ``No Excuses'' charter schools. Using lottery-based designs, \citet{angrist2010, angrist2012} found that Boston charter schools generated substantial test score gains, on the order of $d = 0.40$ in math per year. \citet{abdulkadiroglu2011} confirmed similar effects. Importantly, \citet{cohodes2021} demonstrated that these Boston charters maintained their large positive effects even as the sector scaled up, suggesting the model is replicable.

Conversely, non-urban charters and virtual charter schools generally show null or negative effects on student achievement. The \citet{credo2015} national report highlighted this variance, showing that while urban charters often outperform traditional public schools, the average national effect is near zero due to severe underperformance in the virtual and suburban sectors.

\subsection{Voucher Programs and the Supply-Side Mechanism}
Evidence on private school vouchers is mixed and increasingly negative in recent large-scale programs. While early evaluations of the Milwaukee voucher program \citep{rouse1998} and the New York scholarship program \citep{howell2002} showed modest positive effects, recent statewide programs have yielded concerning results.

The stark divergence between early positive findings and recent negative ones points to a critical supply-side dynamic. In mature, highly regulated sectors (like Boston charters), students transfer to demonstrably higher-quality schools. In rapidly expanding, lightly regulated voucher programs, the participating private schools often experienced declining enrollment prior to the program and may offer lower instructional quality than the public schools students left behind. \citet{abdulkadiroglu2018} found that the Louisiana Scholarship Program caused severe test score declines---approaching $d = -0.40$ in math---for voucher recipients in the first year, a finding consistent with this supply-side interpretation.

"""

with open('/home/ubuntu/k12-education-research/drafts/latex_part1.tex', 'w') as f:
    f.write(latex_content)
