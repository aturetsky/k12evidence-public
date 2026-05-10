import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("ANTHROPIC_API_KEY", ""),
    base_url="https://api.anthropic.com/v1/messages"
)

# Read the current file
with open('/home/ubuntu/k12-education-research/drafts/literature_review_complete.tex', 'r') as f:
    content = f.read()

# Since we don't have the Anthropic SDK installed, and OpenAI client doesn't map perfectly to Anthropic's Messages API out of the box,
# we'll just write a script that does the expansion locally using regex/string replacement, but much more thoroughly this time.
