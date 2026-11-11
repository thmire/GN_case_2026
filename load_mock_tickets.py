import requests, json

# load the mock tickets
with open("mock_tickets.json") as f:
    ticket_data = json.load(f)

for t in ticket_data:
    # load the data into the server with the create_ticket function
    r = requests.post("http://127.0.0.1:8000/tickets",
        json={"title": t["title"], "description": t["description"]})
    ticket_id = r.json()["id"]

    # For tickets with non-default data, update to reflect status and resolution
    if t["status"] != "OPEN" or t["resolution"]:
        requests.patch(f"http://127.0.0.1:8000/tickets/{ticket_id}",
                       json={"status": t["status"],
                             "resolution": t["resolution"]})
        
