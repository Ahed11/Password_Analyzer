import math


def calculate_entropy(password, analysis):
    charset_size = 0

    if analysis["is_passphrase"]:
        word_count = len([part for part in password.replace("_", " ").replace("-", " ").split() if part])
        if word_count > 0:
            return word_count * math.log2(7776)

    if analysis["lowercase"]:
        charset_size += 26
    if analysis["uppercase"]:
        charset_size += 26
    if analysis["digits"]:
        charset_size += 10
    if analysis["special"]:
        charset_size += 32

    length = len(password)
    if charset_size == 0:
        return 0

    return length * math.log2(charset_size)
