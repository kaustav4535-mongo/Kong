
# PEOPLE

Minimal backend scaffold for the **PEOPLE** app.

## What it supports

- Each person has a **10-digit** `person_id`
- A simple **digital keypad** endpoint (echoes pressed digit)
- **Text-only** messages between registered IDs

## Run

This backend is implemented with FastAPI.

1. Install dependencies (example):
   - `pip install fastapi uvicorn pydantic`
2. Start the server:
   - `cd backend`
   - `python main.py`

Then open `http://localhost:8000/docs`.

## API

- `POST /api/v1/people/register` `{ "person_id": "0123456789" }`
- `POST /api/v1/keypad/press` `{ "digit": "7" }`
- `POST /api/v1/messages/send` `{ "from_id": "0123456789", "to_id": "1111111111", "text": "hello", "kind": "text" }`
- `GET /api/v1/messages/inbox/{person_id}`
