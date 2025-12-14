import psycopg2
import psycopg2.extras
from app.db.connection import get_db
from decimal import Decimal
from app.config import settings

def _normalize(row):
    for k, v in row.items():
        if isinstance(v, Decimal):
            row[k] = float(v)
    return row

def fetch_all(query, params=None):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(query, params or ())
    rows = cur.fetchall()
    conn.close()
    return [_normalize(dict(row)) for row in rows]   # 🔥 convert every row

def fetch_one(query, params=None):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(query, params or ())
    row = cur.fetchone()
    conn.close()
    return _normalize(dict(row)) if row else None   # 🔥 convert one row