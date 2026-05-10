import re

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'r') as f:
    content = f.read()

# Add mourshed2010 to the International Systems section
old_text = r"High-performing systems often share common characteristics: highly selective teacher recruitment (Finland recruits teachers from the top third of university graduates; South Korea from the top 5\%), rigorous national curricula that emphasize deep conceptual understanding over procedural fluency, significant autonomy for teachers and schools coupled with strong accountability mechanisms, and high social status for the teaching profession."

new_text = r"High-performing systems often share common characteristics: highly selective teacher recruitment (Finland recruits teachers from the top third of university graduates; South Korea from the top 5\%), rigorous national curricula that emphasize deep conceptual understanding over procedural fluency, significant autonomy for teachers and schools coupled with strong accountability mechanisms, and high social status for the teaching profession. \citet{mourshed2010} found that improving school systems adopt interventions appropriate to their specific performance stage (e.g., basic literacy and numeracy for poor-to-fair systems, versus professionalizing teaching for good-to-great systems), while sharing a common reliance on the continuity of new leadership to sustain reform."

if old_text in content:
    content = content.replace(old_text, new_text)
    print("Added mourshed2010 to manuscript.")
else:
    print("Could not find the insertion point.")

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'w') as f:
    f.write(content)
