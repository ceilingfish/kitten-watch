import os
import psycopg2

def get_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")

def ensure_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS seen_guids (
                    guid TEXT PRIMARY KEY,
                    seen_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)
        conn.commit()

def is_seen(guid: str) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM seen_guids WHERE guid = %s", (guid,))
            return cur.fetchone() is not None

def mark_seen(guid: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO seen_guids (guid) VALUES (%s) ON CONFLICT DO NOTHING", (guid,))
        conn.commit()
