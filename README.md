# GN_case_2026
End-to-End Fault-Tolerant GenAI Agent System

## Contents
- [Part 1: Mock Ticketing API](#part-1-mock-ticketing-api)
- [Part 2: GenAI Agent](#part-2-genai-agent)
- [Part 3: PR Review Bot](#part-3-pr-review-bot)
- [Part 4: Terraform](#part-4-terraform)
- [Part 5: Design Decisions](#part-5-design-decisions)

## Prerequisites

- Python 3.10+
- Python modules: fastapi, uvicorn, pydantic, typing, datetime, os, json 

## Part 1: Mock Ticketing API

```bash
uvicorn api:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive docs at `http://127.0.0.1:8000/docs`.

On startup it loads 20 mock tickets from `mock_tickets.json`. Tickets created, updated, or deleted during a session are lost when the server restarts.

### Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/tickets` | List all tickets |
| GET | `/tickets/search` | Filter by `status` and/or `title` |
| GET | `/tickets/{id}` | Get one ticket (404 if missing) |
| POST | `/tickets` | Create a ticket |
| PATCH | `/tickets/{id}` | Update status/resolution |
| DELETE | `/tickets/{id}` | Delete a ticket |

### Example

```bash
curl -X POST http://127.0.0.1:8000/tickets \
  -H "Content-Type: application/json" \
  -d '{"title": "Keyboard not working", "description": "Stopped responding"}'
```
