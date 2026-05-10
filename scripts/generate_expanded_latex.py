import re

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'r') as f:
    content = f.read()

# 1. Update the AI acknowledgment in the abstract to include ResearchRabbit, OpenAI, and Elicit.
content = content.replace(
    r"Perplexity Computer was employed to fact-check effect sizes and verify paper existence across 10 verification batches, while Claude 3 Opus was utilized for editorial review and internal consistency checks. Elicit was considered for automated literature retrieval but ultimately not employed in favor of direct institutional access and manual verification.",
    r"Perplexity Computer was employed to fact-check effect sizes and verify paper existence across 10 verification batches. Claude 3 Opus and OpenAI models were utilized for editorial review, structural expansion, and internal consistency checks. ResearchRabbit and the Elicit API are integrated into the broader project workflow for citation network analysis and automated literature retrieval, though primary PDF acquisition relied on direct institutional access."
)

# We will just write the updated content back for now, and then use python to do the major expansions
with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'w') as f:
    f.write(content)

