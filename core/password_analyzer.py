import string


def analyze_password(password):
    result = {}
    result["length"] = len(password)
    result["lowercase"] = any(c.islower() for c in password)
    result["uppercase"] = any(c.isupper() for c in password)
    result["digits"] = any(c.isdigit() for c in password)
    result["special"] = any(c in string.punctuation for c in password)
    result["unique_chars"] = len(set(password))
    result["is_passphrase"] = " " in password or "-" in password or "_" in password
    result["has_long_repeat"] = _has_long_repeat(password)
    return result


def _has_long_repeat(password, threshold=4):
    current_run = 1
    for index in range(1, len(password)):
        if password[index] == password[index - 1]:
            current_run += 1
            if current_run >= threshold:
                return True
        else:
            current_run = 1
    return False
