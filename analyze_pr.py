import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv


# Github Configuration (set by the workflow)
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]  # this combines the user and repo names
PR_NUMBER = os.environ["PR_NUMBER"]

# LLM configuration
load_dotenv()  # reads .env into os.environ if the file exists
API_KEY = os.environ.get("GN_API_KEY")
if not API_KEY:
    raise SystemExit("GN_API_KEY not set")
client = OpenAI(
        api_key=API_KEY,
        base_url="https://models.genie.gn.group/openai/v1",
        default_headers={"api-key": API_KEY},
    )

# Get the PR diff

diff_url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}"
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}",
           "Accept": "application/vnd.github.v3.diff" # get the diff
           }
response = requests.get(diff_url,
                        headers=headers)
response.raise_for_status() # Check that we got something.
diff = response.text

# Check that there is something in the PR
if not diff.strip():
    print("Empty diff, nothing to review.")
    raise SystemExit(0)

# Truncate to keep cost/time reasonable for this exercise
max_chars = 20000
if len(diff) > max_chars:
    diff = diff[:max_chars] + "\n... (truncated)"

# Send it to a LLM for analysis
# Should be a simple summary and any suggestions for improvements.

SYSTEM_PROMPT = (
    "You are a code reviewer."
    "Provide a simple summary of the pull request."
    "Make suggestions for improvements if it is appropriate."
    "Be concise."
    )

messages = [
        {"role": "system",
         "content": SYSTEM_PROMPT},
        {"role": "user",
         "content": f"Review this diff:\n\n{diff}"},
    ]

response = client.chat.completions.create(
    model="gpt-6-luna",
    messages=messages,
    max_completion_tokens=300,
    reasoning_effort="none",
)



