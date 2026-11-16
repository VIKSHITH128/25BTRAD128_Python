"""
Glue helpers used only by the UI layer.
None of this touches persistence/database.py or core/models.py logic -
it just calls what already exists there.
"""

from datetime import datetime, date

from utils.utils import get_birth_date_from_id
from utils.validators import is_valid_email, is_valid_phone, is_valid_id
from config import DATE_FORMAT


def next_id(existing_items):
    """Simple incremental id generator based on the current in-memory list."""
    if not existing_items:
        return 1
    return max(item.id for item in existing_items) + 1


def calc_age_from_national_id(national_id: str):
    """
    Returns the age (int) derived from an Egyptian national ID, or None
    if the id doesn't match the expected format. This wires up
    utils.get_birth_date_from_id / utils.is_valid_id, which existed in
    the project but weren't actually called anywhere.
    """
    if not national_id or not is_valid_id(national_id):
        return None
    try:
        birth = get_birth_date_from_id(national_id)
    except (ValueError, IndexError):
        return None

    today = date.today()
    age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    return age if 0 <= age <= 120 else None


def validate_email_field(value):
    return None if is_valid_email(value) else "Invalid email address (e.g. name@mail.com)"


def validate_phone_field(value):
    return None if is_valid_phone(value) else "Invalid phone number (11 digits required)"


def validate_national_id_field(value):
    return None if is_valid_id(value) else "Invalid national ID (must be 14 digits)"


def parse_date(value: str):
    return datetime.strptime(value, DATE_FORMAT)


def validate_date_field(value):
    try:
        parse_date(value)
        return None
    except ValueError:
        return f"Date format must be {DATE_FORMAT}"


def expiry_status(expiry_date_str: str):
    """
    Returns one of: 'expired', 'soon' (<=30 days), 'ok'.
    Used to color-code medicine rows in the tables.
    """
    try:
        expiry = parse_date(expiry_date_str)
    except (ValueError, TypeError):
        return "ok"

    days_left = (expiry - datetime.now()).days
    if days_left < 0:
        return "expired"
    if days_left <= 30:
        return "soon"
    return "ok"
