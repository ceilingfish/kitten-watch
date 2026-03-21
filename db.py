import os, ssl
from urllib.parse import urlparse
import pg8000.dbapi

def get_connection():
    url = urlparse(os.environ["DATABASE_URL"])
    if os.environ.get("DB_SSL", "true") == "true":
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
    else:
        ssl_context = None
    return pg8000.dbapi.connect(
        host=url.hostname,
        port=url.port or 5432,
        database=url.path.lstrip("/"),
        user=url.username,
        password=url.password,
        ssl_context=ssl_context,
    )

def ensure_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS seen_guids (
            guid TEXT PRIMARY KEY,
            seen_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    conn.commit()
    conn.close()

def is_seen(guid: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM seen_guids WHERE guid = %s", (guid,))
    result = cur.fetchone() is not None
    conn.close()
    return result

def mark_seen(guid: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO seen_guids (guid) VALUES (%s) ON CONFLICT DO NOTHING", (guid,))
    conn.commit()
    conn.close()
