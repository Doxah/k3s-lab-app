import os
import psycopg
from flask import Flask, jsonify, request

app = Flask(__name__)
DSN = (f"host={os.environ['DB_HOST']} dbname={os.environ['DB_NAME']} "
       f"user={os.environ['DB_USER']} password={os.environ['DB_PASSWORD']}")

def db():
    return psycopg.connect(DSN, connect_timeout=3)

@app.get("/api/healthz")          # liveness : le process répond
def healthz():
    return {"status": "ok"}

@app.get("/api/readyz")           # readiness : la base est joignable
def readyz():
    try:
        with db() as conn:
            conn.execute("SELECT 1")
        return {"status": "ready"}
    except psycopg.Error as exc:     # erreurs de base uniquement, pas les bugs du code
        return {"status": "db unreachable", "error": str(exc)}, 503

@app.get("/api/version")
def version():
    return {"version": os.environ.get("APP_VERSION", "dev"), "pod": os.environ.get("HOSTNAME")}

@app.get("/api/messages")
def list_messages():
    with db() as conn:
        rows = conn.execute("SELECT author, body FROM messages ORDER BY id DESC LIMIT 50").fetchall()
    return jsonify([{"author": a, "body": b} for a, b in rows])

@app.post("/api/messages")
def add_message():
    data = request.get_json(force=True)
    with db() as conn:
        conn.execute("INSERT INTO messages (author, body) VALUES (%s, %s)",
                     (data["author"][:50], data["body"][:500]))   # requête paramétrée : pas d'injection SQL
    return {"status": "created"}, 201