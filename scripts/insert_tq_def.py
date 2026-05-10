import re

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'r') as f:
    content = f.read()

old_text = r"The consensus in education economics is that teacher quality is the most important school-based determinant of student achievement. This finding is robust across multiple methodological approaches and has been replicated in dozens of countries. Foundational work by \citet{rivkin2005} and \citet{rockoff2004} demonstrated that the standard deviation of teacher value-added effects on student test scores is approximately $d = 0.10$--$0.15$."

new_text = r"""The consensus in education economics is that teacher quality is the most important school-based determinant of student achievement. Before proceeding, it is necessary to define what the economic literature means by "teacher quality." Unlike traditional education research, which often measures quality through observable credentials (e.g., master's degrees, certification status, or years of experience), the modern causal literature defines teacher quality almost exclusively as \textit{value-added}---the marginal contribution a specific teacher makes to a student's academic growth, controlling for the student's prior achievement and demographic characteristics. As \citet{rivkin2005} and others have repeatedly demonstrated, observable credentials explain very little (typically less than 5\%) of the true variance in teacher effectiveness.

This finding is robust across multiple methodological approaches and has been replicated in dozens of countries. Foundational work by \citet{rivkin2005} and \citet{rockoff2004} demonstrated that the standard deviation of teacher value-added effects on student test scores is approximately $d = 0.10$--$0.15$."""

if old_text in content:
    content = content.replace(old_text, new_text)
    print("Teacher quality definition inserted successfully.")
else:
    print("Could not find the exact text to replace.")

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'w') as f:
    f.write(content)
