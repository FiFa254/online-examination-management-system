"""
Shared logic for the OEMS "obfuscated exam link" scheme:
a real link is base64-encoded behind a fake https://www.oems:// URL, and can
only be unlocked with a 6-character unique code that is checked against the
`link_log` table. Both the student app (form2 / ClassroomApp) and the
teacher app (form3 / MainGUI) use this.
"""
import base64
import random
import string

from .config import OEMS_LINK_PREFIX
from . import db


def encode_link(original_link: str) -> str:
    encoded_bytes = base64.urlsafe_b64encode(original_link.encode("utf-8"))
    return f"{OEMS_LINK_PREFIX}{encoded_bytes.decode('utf-8')}"


def decode_link(transformed_link: str) -> str:
    if not transformed_link.startswith(OEMS_LINK_PREFIX):
        raise ValueError("The link does not start with the correct prefix.")
    encoded_str = transformed_link[len(OEMS_LINK_PREFIX):]
    decoded_bytes = base64.urlsafe_b64decode(encoded_str)
    return decoded_bytes.decode("utf-8")


def is_code_unique(code: str) -> bool:
    row = db.fetch_one(
        "SELECT COUNT(*) FROM link_log WHERE unique_code = %s", (code,)
    )
    return row[0] == 0


def check_code_exists(code: str) -> bool:
    row = db.fetch_one(
        "SELECT COUNT(*) FROM link_log WHERE unique_code = %s", (code,)
    )
    return row[0] > 0


def generate_unique_code(length: int = 6) -> str:
    while True:
        code = "".join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(length)
        )
        if is_code_unique(code):
            return code


def save_converted_link(original_link: str, transformed_link: str, unique_code: str) -> None:
    db.execute(
        "INSERT INTO link_log (original_link, transformed_link, unique_code) "
        "VALUES (%s, %s, %s)",
        (original_link, transformed_link, unique_code),
    )


def fetch_login_history():
    return db.fetch_all("SELECT ID, NAME, Email, Role, Time FROM login_log")
