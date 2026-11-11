# Script for running a local HTTP server containing mock support tickets.
# Server has an API that will interface with an Agent.

from fastapi import FastAPI, HTTPException, Response # API, error handling
import uvicorn # Running local server.
from pydantic import BaseModel
from typing import Optional # want to have optional attributes in pydantic
from datetime import datetime
import os, json

app = FastAPI()
tickets = {} # Store the tickets.
next_id = 1

# Load in some mock data when the app starts up.
@app.on_event("startup")
def load_tickets():
    global next_id
    path = "./mock_tickets.json"
    if not os.path.exists(path):
        return
    with open(path) as f:
        data = json.load(f)
    for t in data:
        tickets[next_id] = {
            "id": next_id,
            "title": t["title"],
            "description": t["description"],
            "created": datetime.fromisoformat(t["created"]),
            "status": t["status"],
            "resolution": t.get("resolution"),
        }
        next_id += 1

class TicketCreate(BaseModel):
    title: str
    description: str
    #created: # PResumably a date and time, use Datetime
    #status: 

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    resolution: Optional[str] = None
    

# Create tickets
@app.post("/tickets")
def create_ticket(body: TicketCreate):
    global next_id
    ticket = {"id": next_id,
              "title": body.title,
              "description": body.description,
              "created": datetime.now(),
              "status": "OPEN",
              "resolution": None,
              "comments": None,
              }
    tickets[next_id] = ticket
    next_id += 1
    return ticket

# Delete tickets
@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int):
    # Check if ticket exists
    if ticket_id not in tickets:
        raise HTTPException(status_code=404,
                            detail=f"Ticket {ticket_id} not found")
    del tickets[ticket_id]
    return Response(status_code=204)
        
# Update a ticket
@app.patch("/tickets/{ticket_id}")
def update_ticket(ticket_id: int, update: TicketUpdate):
    # Check if ticket exists
    if ticket_id not in tickets:
        raise HTTPException(status_code=404,
                            detail=f"Ticket {ticket_id} not found")
    
    # Check if the status update is acceptable
    if update.status not in ["OPEN","RESOLVED","CLOSED"]:
        raise HTTPException(status_code=422,
                        detail="ticket status must be OPEN, RESOLVED or CLOSED")
    
    # If both pass, get the update
    update_data = update.model_dump(exclude_unset=True) 
    tickets[ticket_id].update(update_data)
    
    return tickets[ticket_id]
    
# Read all tickets
@app.get("/tickets")
def list_all_tickets():
    return list(tickets.values())

@app.get("/tickets/search")
def get_specific_tickets(status: Optional[str] = None,
                         title: Optional[str] = None):
    results = list(tickets.values())
    if status is not None:
        results = [t for t in results if t["status"] == status]
    if title is not None:
        results = [t for t in results if title.lower() in t["title"].lower()]
    return results

# Get a specific ticket
@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    # Check if ticket exists
    if ticket_id not in tickets:
        raise HTTPException(status_code=404,
                            detail=f"Ticket {ticket_id} not found")
    return tickets[ticket_id]







