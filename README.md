# GN_case_2026
End-to-End Fault-Tolerant GenAI Agent System

## Contents
- [Part 1: Mock Ticketing API](#part-1-mock-ticketing-api)
- [Part 2: GenAI Agent](#part-2-genai-agent)
- [Part 3: PR Review Bot](#part-3-pr-review-bot)
- [Part 4: Terraform](#part-4-terraform)
- [Part 5: Design Decisions](#part-5-design-decisions)

## Prerequisites

## Part 1: Mock Ticketing API

```bash
uvicorn api:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive docs at `http://127.0.0.1:8000/docs`.

On startup it loads 20 mock tickets from `mock_tickets.json`. Tickets created, updated, or deleted during a session are lost when the server restarts.
