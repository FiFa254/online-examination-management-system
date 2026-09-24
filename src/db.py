"""
Small helper around pyodbc (Microsoft SQL Server) so callers never hardcode
credentials and always close their connections, even on error.

Requires the "ODBC Driver 17 for SQL Server" (or whichever driver name is set
via OEMS_DB_DRIVER) to be installed on the machine running this code.
"""
from contextlib import contextmanager

import pyodbc

from .config import DatabaseConfig


@contextmanager
def get_connection():
    """Yield a SQL Server connection built from DatabaseConfig, always closing it."""
    connection = pyodbc.connect(DatabaseConfig.connection_string())
    try:
        yield connection
    finally:
        connection.close()


def fetch_one(query: str, params: tuple = ()):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchone()
        finally:
            cursor.close()


def fetch_all(query: str, params: tuple = ()):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()


def execute(query: str, params: tuple = (), commit: bool = True):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            if commit:
                conn.commit()
        finally:
            cursor.close()
