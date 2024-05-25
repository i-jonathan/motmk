def validate_password(password: str) -> tuple[bool, str]:
    conditions = {
        "1 uppercase": lambda c: any(x.isupper() for x in c),
        "1 lowercase": lambda c: any(x.islower() for x in c),
        "1 number": lambda c: any(x.isdigit() for x in c),
        "8 characters": lambda c: len(c) >= 8,
    }

    for name, condition in conditions.items():
        if not condition(password):
            return False, f"Password must contain at least {name}."

    return True, ""
