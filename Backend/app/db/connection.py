import psycopg2
from app.config import settings

def get_db():
    return psycopg2.connect(settings.DB_DSN)
