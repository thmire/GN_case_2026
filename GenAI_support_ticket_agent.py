import os
from dotenv import load_dotenv

from openai import OpenAI

# Get the API_KEY
load_dotenv()  # reads .env into os.environ if the file exists
API_KEY = os.environ.get("GN_API_KEY")

if not API_KEY:
    raise SystemExit("Error: GN_API_KEY environment variable is not set. See README.md.")

# from the Case brief
##client = OpenAI(
##        api_key=API_KEY,
##        base_url="https://models.genie.gn.group/openai/v1",
##        default_headers={"api-key": API_KEY},
##    )
##
##
##response = client.chat.completions.create(
##    model="gpt-6-luna",
##    messages=[{"role": "user", "content": "Hello!"}],
##    max_completion_tokens=100,
##)
