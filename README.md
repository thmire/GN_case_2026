# GN_case_2026
End-to-End Fault-Tolerant GenAI Agent System

A mock ticketing API, an LLM-powered agent that operates it, a GitHub Actions PR review bot, and Terraform infrastructure for Azure.

## Contents
- [Part 1: Mock Ticketing API](#part-1-mock-ticketing-api)
- [Part 2: GenAI Agent](#part-2-genai-agent)
- [Part 3: PR Review Bot](#part-3-pr-review-bot)
- [Part 4: Terraform](#part-4-terraform)
- [Part 5: Design Decisions](#part-5-design-decisions)

## Prerequisites

- Python 3.10+
- Terraform 1.0+
- The API key provided in the brief
- Python modules: fastapi, uvicorn, pydantic, typing, datetime, os, json 

## Setup (do this once)

```bash
# 1. Clone the repo
git clone <repo-url>
cd <repo-name>

# 2. Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure the API key
cp .env.example .env
# Open .env and replace "your-api-key-here" with the key from the brief
```
The `.env` file is gitignored.

---

## Part 1: Mock Ticketing API

```bash
uvicorn Ticketing_API:app --reload
```

The API is available at `http://127.0.0.1:8000`. Docs at `http://127.0.0.1:8000/docs`.

On startup it loads 20 mock tickets from `mock_tickets.json`. Tickets created, updated, or deleted during a session are lost when the server restarts.

### Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/tickets` | List all tickets |
| GET | `/tickets/search?status=OPEN&title=keyboard` | Filter by status and/or title |
| GET | `/tickets/{id}` | Get one ticket (404 if missing) |
| POST | `/tickets` | Create a ticket |
| PATCH | `/tickets/{id}` | Update status/resolution,  **404** if not found, **422** if status is invalid |
| DELETE | `/tickets/{id}` | Delete a ticket **404** if not found |

### Business logic errors (required by the brief)

```bash
# 404
curl -i http://127.0.0.1:8000/tickets/999
```

```bash
# 422
curl -i -X PATCH http://127.0.0.1:8000/tickets/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "PROGRESS"}'
```

If you prefer, the interactive docs page can be used to check responses:
1) Open http://127.0.0.1:8000/docs
2) Browse to GET /tickets/{ticket_ID} and select "Try it out"
3) Enter ticket ID = 99, and execute - returns 404
5) Browse to PATCH /tickets/{ticket_ID} and select "Try it out"
6) Enter "PROGRESS" as the value of status in the Edit Value Schema - returns 422 with a helpful error message.


## Part 2: GenAI Agent

A CLI agent that operates the ticketing API.

### Run

With the API running, in a seperate terminal:

```bash
python3 GenAI_support_ticket_agent.py
```

### Example session

---

### Part 3: PR Review Bot

When a PR is opened or updated on this repo, a Github Actions workflow runs "analyze_pr.py". This fetchs the PR diff, sends it to the LLM for a summary and improvement suggestions, and posts a comment on the PR.

### Example

I made a branch, made a test commit, and continued to commit on that branch while completing Task 4 and working on the README.
The bot made multiple comments in the PR at the URL below, before I merged the PR.

https://github.com/thmire/GN_case_2026/pull/1

## Part 4: Terraform (Azure)

A minimal skeleton that describes how the API would run on Azure.

### Files

- `infra/main.tf` — resource group, App Service plan, Linux Web App
- `infra/variables.tf` — three input variables
- `infra/outputs.tf` — the app's default hostname

## Part 5: Design decision I would change in production

