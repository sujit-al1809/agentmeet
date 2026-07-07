# agent/registry.py
import json
from tools import search, calendar, email   # your pure tool functions

# --- what the model SEES ---
TOOL_SCHEMAS = [
    {
        "name": "search_meetings",
        "description": "Semantic search over past meeting transcripts. "
                       "Returns snippets, each tagged with its meeting_id.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    {
        "name": "schedule_action_items",
        "description": "Create calendar events for a meeting's action items.",
        "input_schema": {
            "type": "object",
            "properties": {"meeting_id": {"type": "string"}},
            "required": ["meeting_id"],
        },
    },
    {
        "name": "draft_email",
        "description": "Draft a follow-up recap email for a meeting.",
        "input_schema": {
            "type": "object",
            "properties": {"meeting_id": {"type": "string"}},
            "required": ["meeting_id"],
        },
    },
]

# --- what actually RUNS (name -> python fn) ---
TOOL_FUNCTIONS = {
    "search_meetings":       lambda **kw: search.search(kw["query"]),
    "schedule_action_items": lambda **kw: calendar.schedule_all(kw["meeting_id"]),
    "draft_email":           lambda **kw: email.generate_for(kw["meeting_id"]),
}