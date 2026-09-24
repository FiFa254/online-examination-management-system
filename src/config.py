"""
Centralized configuration for OEMS.

All secrets are read from environment variables (or a local .env file, which
must never be committed to git). See .env.example for the required keys.

The application connects to Microsoft SQL Server via pyodbc.
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
    SERVER = os.getenv("OEMS_DB_SERVER", "localhost")
    NAME = os.getenv("OEMS_DB_NAME", "oems")
    USER = os.getenv("OEMS_DB_USER")  # leave unset to use Windows/trusted auth
    PASSWORD = os.getenv("OEMS_DB_PASSWORD")  # no insecure default on purpose
    DRIVER = os.getenv("OEMS_DB_DRIVER", "{ODBC Driver 17 for SQL Server}")
    # "yes" to use Windows Authentication instead of a SQL login
    TRUSTED_CONNECTION = os.getenv("OEMS_DB_TRUSTED_CONNECTION", "no")

    @classmethod
    def connection_string(cls) -> str:
        use_trusted = cls.TRUSTED_CONNECTION.strip().lower() in ("yes", "true", "1")

        if use_trusted:
            return (
                f"DRIVER={cls.DRIVER};SERVER={cls.SERVER};DATABASE={cls.NAME};"
                f"Trusted_Connection=yes;"
            )

        if not cls.USER or not cls.PASSWORD:
            raise RuntimeError(
                "OEMS_DB_USER / OEMS_DB_PASSWORD are not set. Copy .env.example to "
                ".env and fill them in, or set OEMS_DB_TRUSTED_CONNECTION=yes to use "
                "Windows Authentication instead."
            )
        return (
            f"DRIVER={cls.DRIVER};SERVER={cls.SERVER};DATABASE={cls.NAME};"
            f"UID={cls.USER};PWD={cls.PASSWORD};"
        )


OEMS_LINK_PREFIX = "https://www.oems://"
GOOGLE_CLASSROOM_SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.rosters.readonly",
    "https://www.googleapis.com/auth/classroom.coursework.me",
    "https://www.googleapis.com/auth/classroom.coursework.students",
]
