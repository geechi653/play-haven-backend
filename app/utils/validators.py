import re


def is_valid_email(email):
    PATTERN = re.compile(r"^[^@]+@[^@]+\.[^@]+$")
    return bool(PATTERN.fullmatch(email))

def is_valid_username(username):
    return isinstance(username, str) and username != "" and not any(ch.isspace() for ch in username)

def is_valid_first_name(first_name):
    return isinstance(first_name, str) and first_name != "" and not any(ch.isspace() for ch in first_name)

def is_valid_last_name(last_name):
    return isinstance(last_name, str) and last_name != "" and not any(ch.isspace() for ch in last_name)

def is_valid_country(country):
    return isinstance(country, str) and country != ""

def is_valid_password(pwd):
    return 5 <= len(pwd) <= 16 and any(ch.isdigit() for ch in pwd) and any(ch.isalpha() for ch in pwd)
