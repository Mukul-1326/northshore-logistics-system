import sqlite3

DB_NAME = "northshore.db"


def open_link():
    connection = sqlite3.connect(DB_NAME, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def fetch_cursor(conn):
    return conn.cursor()


def close_link(conn):
    if conn:
        conn.close()