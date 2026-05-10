import re

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'r') as f:
    content = f.read()

# Fix mourshed2010
old_text = r"Similarly, \citet{mourshed2010} found that the most improved school systems globally share common features: strong teacher recruitment and training, data-driven instruction, and sustained political commitment."
new_text = r"Similarly, \citet{mourshed2010} found that improving school systems adopt interventions appropriate to their specific performance stage (e.g., basic literacy and numeracy for poor-to-fair systems, versus professionalizing teaching for good-to-great systems), while sharing a common reliance on the continuity of new leadership to sustain reform."

if old_text in content:
    content = content.replace(old_text, new_text)
    print("Found and replaced mourshed2010 text exactly.")
else:
    print("Could not find exact mourshed2010 text. Using regex.")
    content = re.sub(
        r"Similarly, \\citet\{mourshed2010\} found that the most improved school systems globally share common features: strong teacher recruitment and training, data-driven instruction, and sustained political commitment\.",
        new_text,
        content
    )

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'w') as f:
    f.write(content)
