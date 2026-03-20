import math

def calculate_bruteforce_time(password, analysis):

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

    combinations = charset_size ** length

    attempts_per_second = 1_000_000_000  # 1 миллиард попыток

    seconds = combinations / attempts_per_second

    return seconds

def format_time(seconds):

    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    years = days / 365

    if years >= 1:
        return f"{years:.2f} лет"
    elif days >= 1:
        return f"{days:.2f} дней"
    elif hours >= 1:
        return f"{hours:.2f} часов"
    elif minutes >= 1:
        return f"{minutes:.2f} минут"
    else:
        return f"{seconds:.2f} секунд"