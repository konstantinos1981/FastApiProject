import re

def confirm_field_match(v, values, field_to_match, error_message):
    if field_to_match in values and v != values[field_to_match]:
        raise ValueError(error_message)
    return v

def validate_password_field(password: str):
    rules = [
        (r'.{8,16}', 'Password must be between 8 and 16 characters long.'),
        (r'[A-Z]', 'Password must contain at least one uppercase letter.'),
        (r'[a-z]', 'Password must contain at least one lowercase letter.'),
        (r'[0-9]', 'Password must contain at least one digit.'),
        (r'[!@#$%^&*(),.?":{}|<>]', 'Password must contain at least one special character.')
    ]

    errors = [msg for pattern, msg in rules if not re.search(pattern, password)]
    if errors:
        raise ValueError("\n".join(errors))
    return password
    
def normalize_email_field(v):
    return v.strip().lower()

def capitalize_name_fields(v):
    return v.strip().title()

def validate_username_field(v):
    if v and not re.match(r"^[A-Za-z0-9_]+$", v):
        raise ValueError("Username must contain only letters, numbers, and underscores.")
    return v