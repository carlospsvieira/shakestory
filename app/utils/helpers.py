import re


def validate_story_content(content):
    if len(re.findall(r"[a-zA-Z]", content)) < 10:
        return False

    if "." not in content or "," not in content:
        return False

    return True
