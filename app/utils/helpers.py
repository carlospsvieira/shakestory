import re


def validate_story_content(content: str):
    if len(re.findall(r"[a-zA-Z]", content)) < 10:
        return False

    if "." not in content or "," not in content:
        return False

    return True


def validate_password_format(password: str):
    if len(password) < 6:
        return False

    if not re.search(r"[a-zA-Z]", password) or not re.search(r"\d", password):
        return False

    return True
