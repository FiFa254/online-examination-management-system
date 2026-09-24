"""
Centralized configuration for OEMS.

All secrets are read from environment variables (or a local .env file, which
must never be committed to git). See .env.example for the required keys.
"""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv is optional; if it's not installed, values must already
    # be present in the process environment.
    pass


class DatabaseConfig:
    HOST = os.getenv("OEMS_DB_HOST", "127.0.0.1")
    USER = os.getenv("OEMS_DB_USER", "root")
    PASSWORD = os.getenv("OEMS_DB_PASSWORD")  # no insecure default on purpose
    NAME = os.getenv("OEMS_DB_NAME", "oems")

    @classmethod
    def as_kwargs(cls) -> dict:
        if not cls.PASSWORD:
            raise RuntimeError(
                "OEMS_DB_PASSWORD is not set. Copy .env.example to .env and "
                "fill in your database password before running the app."
            )
        return {
            "host": cls.HOST,
            "user": cls.USER,
            "password": cls.PASSWORD,
            "database": cls.NAME,
        }


OEMS_LINK_PREFIX = "https://www.oems://"
GOOGLE_CLASSROOM_SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.rosters.readonly",
    "https://www.googleapis.com/auth/classroom.coursework.me",
    "https://www.googleapis.com/auth/classroom.coursework.students",
]
