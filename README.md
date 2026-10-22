# FastAPI + PostgreSQL starter

A small FastAPI app on PostgreSQL, ready to deploy: a notes API with create,
list and delete, and its table created on startup. The database comes from one
environment variable, `DATABASE_URL`, so no password sits in the code.

| Endpoint | What it does |
|---|---|
| `GET /` | Says whether the database is connected |
| `GET /health` | Runs a query and returns the PostgreSQL version |
| `GET /notes` | Lists the notes |
| `POST /notes` | Adds one: `{"text": "..."}` |
| `DELETE /notes/{id}` | Deletes one |
| `GET /docs` | FastAPI's interactive docs |

## Deploy it on Uppcoder (free plan)

[Uppcoder](https://portal.uppcoder.com/developers?utm_source=github&utm_medium=repo&utm_campaign=fastapi-starter)
runs it on its own HTTPS address with a real PostgreSQL database and VS Code in
the browser beside it.

1. Sign up at portal.uppcoder.com, confirm your email, then Billing, Spark, Start free.
2. Stacks, Create, Blank stack. Pick **FastAPI**, then add **PostgreSQL**: it is
   connected to the app automatically.
3. On the FastAPI card, under Git repository, paste
   `https://github.com/websson/fastapi-postgresql-starter` (branch `main`).
4. Deploy. Uppcoder clones the repository, sets `DATABASE_URL` and installs the
   PostgreSQL driver. Open the app's address and `/health` shows the database.

The full walk-through, with pictures:
[Deploy a FastAPI app with PostgreSQL, free](https://portal.uppcoder.com/guides/deploy-fastapi-postgresql?utm_source=github&utm_medium=repo&utm_campaign=fastapi-starter).

To start from your own copy, fork this repository first and paste your fork's
address instead.

## Run it on your own machine

With Docker:

```bash
docker compose up
```

Then open http://localhost:8000/docs. Compose starts PostgreSQL 16 beside the
app and sets `DATABASE_URL` for it.

Without Docker, point `DATABASE_URL` at any PostgreSQL database:

```bash
pip install -r requirements.txt
export DATABASE_URL=postgresql://user:password@localhost:5432/mydb
uvicorn main:app --reload
```

## Using SQLAlchemy instead

`DATABASE_URL` starts with `postgresql://`, which SQLAlchemy reads as psycopg2.
With psycopg 3 (installed here), give SQLAlchemy
`DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)`.

MIT licensed. Made by [WEBSSON](https://github.com/websson).
