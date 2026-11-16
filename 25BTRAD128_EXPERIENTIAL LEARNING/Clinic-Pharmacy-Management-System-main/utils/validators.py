import re
from datetime import datetime

def is_valid_email(email):
    
    pattern = r"\w+@\w+\.\w+$"

    return bool(re.fullmatch(pattern, email))

def is_valid_phone(phone):

    pattern = r"^01[01235]\d{8}$"

    return bool(re.fullmatch(pattern, phone))

def is_valid_id(id):
    
    pattern = r"^(2(6[1-9]|[7-9]\d)|3\d{2})\d{11}$"

    return bool(re.fullmatch(pattern, id))
