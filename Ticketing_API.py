# Script for running a local HTTP server containing mock support tickets.
# Server has an API that will interface with an Agent.

from fastapi import FastAPI, HTTPException # API, error handling
import uvicorn # Running local server.
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()
tickets = {} # Store the tickets.
next_id = 1

class TicketCreate(BaseModel):
    "User interface for creating tickets"
    title: str
    description: str
    #created: # PResumably a date and time, use Datetime
    #status: 

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Create tickets
@app.post("/tickets")
def create_ticket(body: TicketCreate):
    global next_id
    ticket = {"id": next_id,
              "title": body.title,
              "description": body.description,
              "created": datetime.now(),
              "status": "OPEN",
              "resolution": None}
    tickets[next_id] = ticket
    next_id += 1
    return ticket

# Read all tickets
@app.get("/tickets")
def list_tickets():
    return list(tickets.values())

    
##
##@app.get("/")
##def read_root():
##    return {"Hello": "World"}
##
##
##@app.get("/items/{item_id}")
##def read_item(item_id: int, q: str | None = None):
##    return {"item_id": item_id, "q": q}
