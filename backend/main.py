"""PEOPLE backend entrypoint.

This repository is currently a minimal backend-only scaffold.
It provides a small HTTP API to support:
- 10-digit personal IDs
- a keypad-like digit echo endpoint
- text-only messaging between IDs
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


APP_NAME = "PEOPLE"
APP_VERSION = "0.1.0"


def utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def validate_person_id(person_id: str) -> str:
    if len(person_id) != 10 or not person_id.isdigit():
        raise HTTPException(status_code=422, detail="person_id must be exactly 10 digits")
    return person_id


class RegisterRequest(BaseModel):
    person_id: str = Field(..., description="Exactly 10 digits")


class MessageRequest(BaseModel):
    from_id: str = Field(..., description="Exactly 10 digits")
    to_id: str = Field(..., description="Exactly 10 digits")
    text: str = Field(..., min_length=1, max_length=2000)
    kind: Literal["text"] = "text"


class KeypadPressRequest(BaseModel):
    digit: str = Field(..., description="Single digit 0-9")


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Personal Digital Identity Platform (backend scaffold)",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# In-memory storage (for scaffold/demo purposes only)
registered_people: set[str] = set()
messages: list[dict] = []


@app.get("/")
async def root():
    return {
        "app_name": APP_NAME,
        "version": APP_VERSION,
        "timestamp": utc_now().isoformat(),
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


@app.post("/api/v1/people/register")
async def register_person(body: RegisterRequest):
    person_id = validate_person_id(body.person_id)
    registered_people.add(person_id)
    return {"person_id": person_id, "registered": True, "timestamp": utc_now().isoformat()}


@app.post("/api/v1/keypad/press")
async def keypad_press(body: KeypadPressRequest):
    if len(body.digit) != 1 or not body.digit.isdigit():
        raise HTTPException(status_code=422, detail="digit must be a single character 0-9")
    return {"digit": body.digit}


@app.post("/api/v1/messages/send")
async def send_message(body: MessageRequest):
    from_id = validate_person_id(body.from_id)
    to_id = validate_person_id(body.to_id)

    if from_id not in registered_people:
        raise HTTPException(status_code=404, detail="from_id is not registered")
    if to_id not in registered_people:
        raise HTTPException(status_code=404, detail="to_id is not registered")

    record = {
        "id": len(messages) + 1,
        "from_id": from_id,
        "to_id": to_id,
        "kind": "text",
        "text": body.text,
        "timestamp": utc_now().isoformat(),
    }
    messages.append(record)
    return record


@app.get("/api/v1/messages/inbox/{person_id}")
async def inbox(person_id: str):
    person_id = validate_person_id(person_id)
    if person_id not in registered_people:
        raise HTTPException(status_code=404, detail="person_id is not registered")
    return [m for m in messages if m["to_id"] == person_id]


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
