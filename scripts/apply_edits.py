import re

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'r') as f:
    content = f.read()

# 1. Claude: Add transition between Methodological Framework and Clusters
transition_text = r"""\subsection{Threats to Validity in Education Research}
...
Heterogeneous effects across student subgroups often mask important distributional consequences of universal policies.

\vspace{1em}
\noindent \textit{Transitioning to the Substantive Clusters:} The following ten sections apply this methodological lens to specific domains of K-12 education policy. In each cluster, we observe how the application of increasingly rigorous research designs---from early observational studies to recent randomized lotteries and regression discontinuities---has frequently challenged or overturned established policy consensus.
"""
# Since exact replacement might fail if we don't match perfectly, we'll use a targeted substitution
content = re.sub(
    r'(Heterogeneous effects across student subgroups often mask important distributional consequences of universal policies\.)',
    r'\1\n\n\\vspace{1em}\n\\noindent \\textit{Transitioning to the Substantive Clusters:} The following ten sections apply this methodological lens to specific domains of K-12 education policy. In each cluster, we observe how the application of increasingly rigorous research designs---from early observational studies to recent randomized lotteries and regression discontinuities---has frequently challenged or overturned established policy consensus.',
    content
)

# 2. Gemini: Fix "one standard deviation increase in teacher quality" phrasing
content = re.sub(
    r'a one standard deviation increase in teacher quality raises student test scores by approximately \$d = 0\.10\$--\$0\.15\$',
    r'the standard deviation of teacher value-added effects on student test scores is approximately $d = 0.10$--$0.15$',
    content
)

# 3. Gemini: Fix ASA quote (make it a paraphrase rather than a direct quote if it wasn't exact)
content = re.sub(
    r'noting that VAMs are ``not sufficiently reliable or valid to be used in high-stakes personnel decisions\.\'\'',
    r'expressing significant concerns about the reliability and validity of VAMs, and advising against their sole or primary use for such decisions.',
    content
)

# 4. Gemini: Add "present discounted value" to the Chetty $250k claim
content = re.sub(
    r'raises the lifetime earnings of a single classroom by approximately \\\$250,000',
    r'raises the lifetime earnings (in present discounted value) of a single classroom by approximately \\$250,000',
    content
)

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'w') as f:
    f.write(content)

print("Edits applied successfully.")
