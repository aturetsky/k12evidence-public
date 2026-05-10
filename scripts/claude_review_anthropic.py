import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

draft_content = open('/home/ubuntu/k12-education-research/drafts/literature_review.md', 'r').read()

prompt = f"""
You are an expert academic editor and education policy researcher. 
Please perform a rigorous editorial and structural review of the following literature review draft on K-12 education research.

Specifically, evaluate:
1. INTERNAL CONSISTENCY: Check whether the cross-cutting synthesis and replication agenda logically follow from the cluster-level findings.
2. EDITORIAL QUALITY: Note any sections that are unclear, poorly structured, or where the argument could be strengthened.
3. GAPS IN SYNTHESIS: Identify any clusters where the synthesis feels thin or where the transition between competing findings is abrupt.
4. TONE AND AUDIENCE: Ensure the tone is rigorously academic yet accessible for a working paper.

Please provide specific, actionable feedback organized by section.

DRAFT DOCUMENT:
{draft_content}
"""

print("Submitting draft to Claude for review...")
message = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4000,
    system="You are a rigorous academic editor.",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

with open('/home/ubuntu/k12-education-research/drafts/claude_review_feedback.md', 'w') as f:
    f.write(message.content[0].text)

print("Review complete. Feedback saved to drafts/claude_review_feedback.md")
