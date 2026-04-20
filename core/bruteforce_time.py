import math


ATTACK_SCENARIOS = {
    "online_rate_limited": ("Online attack (rate limiting)", 10),
    "offline_cpu": ("Offline CPU", 100_000_000),
    "offline_gpu": ("Offline GPU", 100_000_000_000),
}


def _charset_size(analysis):
    size = 0
    if analysis["is_passphrase"]:
        return 7776
    if analysis["lowercase"]:
        size += 26
    if analysis["uppercase"]:
        size += 26
    if analysis["digits"]:
        size += 10
    if analysis["special"]:
        size += 32
    return size


def calculate_bruteforce_time(password, analysis):
    charset_size = _charset_size(analysis)
    length = len(password)

    if analysis["is_passphrase"]:
        length = len([part for part in password.replace("_", " ").replace("-", " ").split() if part])

    if charset_size == 0 or length == 0:
        return {}

    combinations = math.pow(charset_size, length)
    return {
        scenario_key: combinations / attempts_per_second
        for scenario_key, (_, attempts_per_second) in ATTACK_SCENARIOS.items()
    }


def format_time(seconds):
    if seconds < 1:
        return "< 1 секунды"

    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    years = days / 365

    if years >= 1_000_000_000:
        return f"{years:.2e} лет"
    if years >= 1:
        return f"{years:.2f} лет"
    if days >= 1:
        return f"{days:.2f} дней"
    if hours >= 1:
        return f"{hours:.2f} часов"
    if minutes >= 1:
        return f"{minutes:.2f} минут"
    return f"{seconds:.2f} секунд"
