import math

def calculate_entropy(password, analysis):

    charset_size = 0

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

    entropy = length * math.log2(charset_size)

    return entropy