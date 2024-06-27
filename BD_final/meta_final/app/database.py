import psycopg2
from flask import current_app, g

from config import Config

GLOBAL_CONNECTION_NAME = 'conn'


def get_connection():
    if GLOBAL_CONNECTION_NAME not in g:
        g.conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )

    return g.conn


def close_connection(e=None):
    db = g.pop(GLOBAL_CONNECTION_NAME, None)

    if db is not None:
        db.close()
