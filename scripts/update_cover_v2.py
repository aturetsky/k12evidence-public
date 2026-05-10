import re

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'r') as f:
    content = f.read()

# Replace the author block with the new human-AI collaborative format
old_author = r'\\author\{Avi Turetsky\}'
new_author = r"""\\author{
  Avi Turetsky \\and Manus AI \\\\
  \\vspace{0.5em}
  \\small\\textit{(human-AI collaborative working paper)} \\\\
  \\vspace{1em}
  \\small\\textit{Additional AI tools: Perplexity, Claude (Anthropic), Gemini (Google), ResearchRabbit, Elicit}
}"""
content = re.sub(old_author, new_author, content)

with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'w') as f:
    f.write(content)

print("Cover page updated.")
