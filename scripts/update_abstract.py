import re

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'r') as f:
    content = f.read()

old_text = r"This document synthesizes the causal evidence across ten core domains of K-12 education research, drawing on a verified registry of 99 high-impact papers."
new_text = r"This document synthesizes the causal evidence across ten core domains of K-12 education research. The synthesis directly cites 61 high-impact papers, drawn from a systematically reviewed registry of 124 empirical studies, meta-analyses, and critical re-evaluations (all of which are included in the bibliography for further reading)."

if old_text in content:
    content = content.replace(old_text, new_text)
    print("Abstract updated successfully.")
else:
    print("Could not find the exact abstract text to replace.")

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'w') as f:
    f.write(content)
