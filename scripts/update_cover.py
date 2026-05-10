import re

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'r') as f:
    content = f.read()

# Replace the author block
old_author = r'\\author\{Avi Turetsky \\and Manus AI\}'
new_author = r"""\\author{
  Avi Turetsky \\
  \\small\\textit{Financial Markets Researcher} \\\\
  \\vspace{0.5em}
  \\small\\textit{with computational and drafting assistance from} \\\\
  Manus AI
}"""
content = re.sub(old_author, new_author, content)

# Replace the abstract methodology note to be a formal "Declaration of AI Assistance"
old_note = r'\\noindent \\textbf\{AI Methodology Note:\}.*?Case Western Reserve University libraries\.'
new_note = r"""\\noindent \\textbf{Declaration of AI Assistance:} In accordance with emerging transparency guidelines for academic publishing (e.g., ICMJE, WAME), we disclose the following use of artificial intelligence in the preparation of this manuscript: \textbf{Manus AI} acted as the primary computational research assistant, executing literature retrieval, fact-checking, and drafting under human direction. \textbf{Perplexity} was employed for iterative fact-checking of effect sizes and verification of paper existence. \textbf{Claude} (Anthropic) and \textbf{Gemini} (Google) were used for independent editorial review, structural critique, and internal consistency checks. \textbf{ResearchRabbit} and \textbf{Elicit} were integrated for citation network analysis and automated literature screening. The human author (Turetsky) designed the research agenda, directed all AI operations, reviewed the primary literature, and takes full responsibility for the final content and conclusions."""
content = re.sub(old_note, new_note, content, flags=re.DOTALL)

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'w') as f:
    f.write(content)

print("Cover page updated.")
