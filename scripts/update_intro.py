import re

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'r') as f:
    content = f.read()

old_text = r"This document provides a structured synthesis of the causal evidence across ten core research clusters. It is built upon a systematically verified registry of 99 seminal papers, meta-analyses, and critical re-evaluations."
new_text = r"This document provides a structured synthesis of the causal evidence across ten core research clusters. It directly cites 61 seminal papers, meta-analyses, and critical re-evaluations, drawn from a broader verified registry of 124 studies that inform the analysis."

if old_text in content:
    content = content.replace(old_text, new_text)
    print("Intro updated successfully.")
else:
    print("Could not find the exact intro text to replace.")

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'w') as f:
    f.write(content)
