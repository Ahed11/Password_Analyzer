import string

def analyze_password(password):

    result = {}

    result["length"] = len(password)

    result["lowercase"] = any(c.islower() for c in password)
    result["uppercase"] = any(c.isupper() for c in password)
    result["digits"] = any(c.isdigit() for c in password)

    special_chars = string.punctuation
    result["special"] = any(c in special_chars for c in password)

    return result