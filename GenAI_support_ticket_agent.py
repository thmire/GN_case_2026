import os, json, requests
from dotenv import load_dotenv
from openai import OpenAI

# Get the API_KEY
load_dotenv()  # reads .env into os.environ if the file exists
API_KEY = os.environ.get("GN_API_KEY")

if not API_KEY:
    raise SystemExit("Error: GN_API_KEY environment variable is not set. See README.md.")

# from the Case brief
client = OpenAI(
        api_key=API_KEY,
        base_url="https://models.genie.gn.group/openai/v1",
        default_headers={"api-key": API_KEY},
    )
MODEL = "gpt-6-luna"

# Here provide the python functions that query the API:
API_BASE = "http://127.0.0.1:8000"

# Create a ticket
def create_ticket(title: str, description: str):
    r = requests.post(f"{API_BASE}/tickets",
                      json={"title": title, "description": description})
    if r.status_code >= 400:
        return {"error": r.json().get("detail", "Unknown error")}
    return r.json()

# Delete a ticket
def delete_ticket(ticket_id: int):
    r = requests.delete(f"{API_BASE}/tickets/{ticket_id}")
    if r.status_code >= 400:
        return {"error": r.json().get("detail", "Unknown error")}
    return {"message": f"Ticket {ticket_id} deleted"}

# Update a ticket
def update_ticket(ticket_id: int, status: str = None, resolution: str = None):
    update_requests = {}
    if status:
        update_requests["status"] = status
    if resolution:
        update_requests["resolution"] = resolution
        
    r = requests.patch(f"{API_BASE}/tickets/{ticket_id}",
                       json=update_requests)
    
    if r.status_code >= 400:
        return {"error": r.json().get("detail", "Unknown error")}    
    return r.json()

# Get a specific ticket
def get_ticket_by_id(ticket_id: int):
    r = requests.get(f"{API_BASE}/tickets/{ticket_id}")    
    if r.status_code >= 400:
        return {"error": r.json().get("detail", "Unknown error")}
    return r.json()

# Search tickets by title or status
def get_tickets_by_parameters(status: str = None,
                              title: str = None):
    params = {}
    if status:
        params["status"] = status
    if title:
        params["title"] = title
        
    r = requests.get(f"{API_BASE}/tickets/search", params=params)
    
    if r.status_code >= 400:
        return {"error": r.json().get("detail", "Unknown error")}
    return r.json()

# Now the tool schema

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_ticket",
            "description": "Create a new support ticket",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                },
                "required": ["title", "description"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_ticket",
            "description": "Delete a ticket using its ID",
            "parameters": {
                "type": "object",
                "properties": {"ticket_id": {"type": "integer"}},
                "required": ["ticket_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_ticket_by_id",
            "description": "Get a single ticket by its ID",
            "parameters": {
                "type": "object",
                "properties": {"ticket_id": {"type": "integer"}},
                "required": ["ticket_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_tickets_by_parameters",
            "description": "List tickets, optionally filtered by status or title",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {"type": "string",
                               "enum": ["OPEN", "RESOLVED", "CLOSED"]},
                    "title": {"type": "string"}
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_ticket",
            "description": "Update a ticket's status and/or resolution",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {"type": "integer"},
                    "status": {"type": "string",
                               "enum": ["OPEN", "RESOLVED", "CLOSED"]},
                    "resolution": {"type": "string"},
                },
                "required": ["ticket_id"],
            },
        },
    },
]

FUNCTIONS = {
    "create_ticket": create_ticket,
    "delete_ticket": delete_ticket,
    "get_tickets_by_parameters": get_tickets_by_parameters,
    "get_ticket_by_id": get_ticket_by_id,
    "update_ticket": update_ticket,
}

# The loop that runs the agent

def run_agent(user_input: str):

    SYSTEM_PROMPT = (
        "You are a helpful support ticket assistant. "
        "Use the tools to perform ticket operations. "
        "If a tool returns an error, explain it clearly to the user."
        )

    messages = [
        {"role": "system",
         "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]

    for _ in range(5):  # max rounds to avoid infinite loop
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            max_completion_tokens=100,
        )
        msg = response.choices[0].message
        if not msg.tool_calls:
            return msg.content or "(no response)"
    
        messages.append(msg)
        for call in msg.tool_calls:
            fn_name = call.function.name
            args = json.loads(call.function.arguments)
            result = FUNCTIONS[fn_name](**args)
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result),
            })
    
    return "Agent stopped after maximum tool rounds."


# ---------
if __name__ == "__main__":
    print("Ticket Agent ready. Type 'exit' to quit.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ("exit", "quit"):
            break
        print(f"Agent: {run_agent(user_input)}")
