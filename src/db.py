"""
Small helper around mysql.connector so callers never hardcode credentials
and always close their connections, even on error.
"""
from contextlib import contextmanager

import mysql.connector

from .config import DatabaseConfig


@contextmanager
def get_connection():
    """Yield a MySQL connection built from DatabaseConfig, always closing it."""
    connection = mysql.connector.connect(**DatabaseConfig.as_kwargs())
    try:
        yield connection
    finally:
        if connection.is_connected():
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
