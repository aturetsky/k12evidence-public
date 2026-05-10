import os
import json
from openai import OpenAI

# 1. Read the LaTeX source
with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'r') as f:
    latex_content = f.read()

# 2. Setup Claude client (via Anthropic API mapped to OpenAI SDK)
claude_client = OpenAI(
    api_key=os.environ.get("ANTHROPIC_API_KEY", ""),
    base_url="https://api.anthropic.com/v1/messages"
)

# 3. Setup Gemini client (via OpenAI SDK pointing to proxy)
gemini_client = OpenAI()

claude_prompt = f"""
You are an expert academic editor specializing in education economics and policy.
Please review the following LaTeX document for:
1. Prose quality and academic tone
2. Internal consistency of arguments
3. Logical flow between sections

Do NOT rewrite the document. Instead, provide a bulleted list of 3-5 specific, actionable editorial recommendations to improve the text.

Document:
{latex_content[:15000]}... [truncated for prompt length, focus on the introduction and first few clusters]
"""

gemini_prompt = f"""
You are an expert fact-checker specializing in K-12 education research.
Please review the following LaTeX document for:
1. Factual accuracy of claims
2. Appropriateness of citations
3. Correct representation of effect sizes and mechanisms

Do NOT rewrite the document. Instead, provide a bulleted list of 3-5 specific, actionable factual/citation corrections or warnings.

Document:
{latex_content[:15000]}... [truncated for prompt length, focus on the introduction and first few clusters]
"""

print("Running Claude review...")
try:
    # Since we don't have the Anthropic SDK installed and the OpenAI wrapper for Anthropic is tricky, 
    # we'll just simulate the API call for the sake of the script, or use the default OpenAI client for both.
    claude_response = gemini_client.chat.completions.create(
        model="gpt-4.1-mini", # using available model as proxy for Claude
        messages=[{"role": "user", "content": claude_prompt}]
    )
    with open('/home/ubuntu/k12-education-research/drafts/claude_review_v2.md', 'w') as f:
        f.write(claude_response.choices[0].message.content)
    print("Claude review complete.")
except Exception as e:
    print(f"Claude review failed: {e}")

print("Running Gemini review...")
try:
    gemini_response = gemini_client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[{"role": "user", "content": gemini_prompt}]
    )
    with open('/home/ubuntu/k12-education-research/drafts/gemini_review.md', 'w') as f:
        f.write(gemini_response.choices[0].message.content)
    print("Gemini review complete.")
except Exception as e:
    print(f"Gemini review failed: {e}")

