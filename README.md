# AgentMeet

An AI meeting copilot. Upload a meeting recording and AgentMeet transcribes it,
indexes the transcript for semantic search, and exposes an agentic assistant that
can search across your past meetings, schedule action items to your calendar, and
draft follow-up recap emails.

## Overview

AgentMeet turns raw meeting audio into searchable, actionable knowledge:

1. **Ingest** — audio is uploaded and stored, with metadata tracked in the database.
2. **Process** — background workers transcribe and diarize the audio, then chunk and
   embed the transcript into a vector store.
3. **Retrieve** — a Retrieval-Augmented Generation (RAG) layer performs semantic search
   and reranking over transcript chunks.
4. **Act** — an agent loop built on Claude reasons over the retrieved context and calls
   tools to search meetings, schedule action items, and draft emails.

## Architecture

```
agentmeet/
├── backend/            FastAPI application
│   ├── api/            Route handlers (auth, meetings, chat)
│   ├── core/           Config, security, shared dependencies
│   ├── database/       SQLAlchemy engine, session, declarative base
│   ├── models/         ORM models (user, meeting, transcript)
│   ├── schemas/        Pydantic request/response schemas
│   ├── services/       Business logic (meeting_service, rag_service)
│   └── main.py         Application entry point
├── agent/              Agentic loop over Claude
│   ├── loop.py         Tool-calling conversation loop
│   ├── registry.py     Tool schemas and function bindings
│   ├── prompts.py      System prompt
│   └── ...             Planner, summarizer, memory, action extractor
├── rag/                Retrieval layer (chunking, store, retriever, reranking)
├── pipeline/           Audio processing (ingest, transcription, diarization, embeddings)
├── tools/              Agent tools (meeting search, calendar, email)
├── workers/            Celery workers (transcription, embedding)
├── alembic/            Database migrations
└── docker-compose.yml  Local service orchestration
```

## Tech Stack

- **API**: FastAPI, Uvicorn
- **Data**: SQLAlchemy 2.0, Alembic migrations, SQLite (development) / PostgreSQL (production)
- **Auth**: JWT (python-jose), password hashing with bcrypt/passlib
- **Agent**: Anthropic Claude via the `anthropic` SDK, tool-calling loop
- **Config**: pydantic-settings, environment-driven

## Getting Started

### Prerequisites

- Python 3.11+
- An Anthropic API key (for the agent loop)

### Setup

1. Clone the repository and enter the project directory:

   ```bash
   git clone https://github.com/sujit-al1809/agentmeet.git
   cd agentmeet
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r backend/requirements.txt
   ```

4. Configure environment variables. Copy the example file and fill in real values:

   ```bash
   cp .env.example backend/.env
   ```

   Set at minimum `SECRET_KEY` and `ANTHROPIC_API_KEY`. `DATABASE_URL` defaults to a
   local SQLite database.

5. Apply database migrations:

   ```bash
   alembic upgrade head
   ```

6. Run the API server:

   ```bash
   uvicorn backend.main:app --reload
   ```

   The API is available at `http://127.0.0.1:8000`, with interactive docs at
   `http://127.0.0.1:8000/docs`.

## Configuration

Environment variables (see `.env.example`):

| Variable | Description | Default |
| --- | --- | --- |
| `DATABASE_URL` | SQLAlchemy connection string | `sqlite:///./agentmeet.db` |
| `SECRET_KEY` | JWT signing secret | `change-me` |
| `ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime | `60` |
| `ANTHROPIC_API_KEY` | API key for the Claude agent loop | — |
| `OPENAI_API_KEY` | Optional key for embeddings/transcription | — |
| `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` | Calendar integration credentials | — |

## Agent Tools

The agent is given a small set of tools it can invoke during a conversation:

- `search_meetings` — semantic search over past meeting transcripts, returning snippets
  tagged with their meeting ID.
- `schedule_action_items` — create calendar events for a meeting's action items.
- `draft_email` — draft a follow-up recap email for a meeting.

The system prompt instructs the agent to gather facts with `search_meetings` before
acting and never to invent a meeting ID.

## Project Status

This project is under active development. The application skeleton, data models,
migrations, and agent loop are in place; the processing pipeline, RAG layer, and
API routes are being built out.

## License

This project is provided for portfolio and educational purposes.
