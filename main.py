"""A small FastAPI app on PostgreSQL: a notes API.

The database comes from DATABASE_URL (postgresql://user:password@host:5432/db),
which Uppcoder sets when the app is connected to PostgreSQL and docker compose
sets locally. The table is created on startup, so a fresh database just works.
"""
import os
from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DATABASE_URL = os.environ.get("DATABASE_URL", "")


def connect():
    if not DATABASE_URL:
        raise HTTPException(503, "DATABASE_URL is not set: connect the app to PostgreSQL")
    return psycopg.connect(DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if DATABASE_URL:
        with psycopg.connect(DATABASE_URL) as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS notes ("
                " id SERIAL PRIMARY KEY,"
                " text TEXT NOT NULL,"
                " created_at TIMESTAMPTZ NOT NULL DEFAULT now())"
            )
    yield


app = FastAPI(title="FastAPI + PostgreSQL starter", lifespan=lifespan)


class NoteIn(BaseModel):
    text: str


@app.get("/")
def index():
    return {
        "app": "FastAPI + PostgreSQL starter",
        "database": "connected" if DATABASE_URL else "not connected (DATABASE_URL is not set)",
        "try": ["GET /notes", "POST /notes {\"text\": \"...\"}", "GET /docs"],
    }


@app.get("/health")
def health():
    with connect() as conn:
        version = conn.execute("SELECT version()").fetchone()[0]
    return {"ok": True, "postgres": version.split(",")[0]}


@app.get("/notes")
def list_notes():
    with connect() as conn:
        rows = conn.execute("SELECT id, text, created_at FROM notes ORDER BY id").fetchall()
    return [{"id": r[0], "text": r[1], "created_at": r[2].isoformat()} for r in rows]


@app.post("/notes", status_code=201)
def add_note(note: NoteIn):
    if not note.text.strip():
        raise HTTPException(422, "text must not be empty")
    with connect() as conn:
        row = conn.execute(
            "INSERT INTO notes (text) VALUES (%s) RETURNING id, created_at", (note.text.strip(),)
        ).fetchone()
    return {"id": row[0], "text": note.text.strip(), "created_at": row[1].isoformat()}


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    with connect() as conn:
        if conn.execute("DELETE FROM notes WHERE id = %s", (note_id,)).rowcount == 0:
            raise HTTPException(404, "no such note")
