import secrets
import string
from functools import lru_cache
from pathlib import Path


PASSPHRASE_WORDS_PATH = Path(__file__).resolve().parent.parent / "data" / "passphrase_words.txt"
DEFAULT_SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{};:,.?/|"


def _shuffle(items):
    shuffled = list(items)
    for index in range(len(shuffled) - 1, 0, -1):
        swap_index = secrets.randbelow(index + 1)
        shuffled[index], shuffled[swap_index] = shuffled[swap_index], shuffled[index]
    return shuffled


def generate_password(length, use_upper, use_lower, use_digits, use_special):
    charsets = []
    password = []

    if use_lower:
        charsets.append(string.ascii_lowercase)
    if use_upper:
        charsets.append(string.ascii_uppercase)
    if use_digits:
        charsets.append(string.digits)
    if use_special:
        charsets.append(DEFAULT_SPECIAL_CHARACTERS)

    if not charsets:
        raise ValueError("Не выбран ни один набор символов.")

    if length < len(charsets):
        raise ValueError(
            f"Для {len(charsets)} выбранных наборов минимальная длина — {len(charsets)}"
        )

    for charset in charsets:
        password.append(secrets.choice(charset))

    all_characters = "".join(charsets)
    for _ in range(length - len(password)):
        password.append(secrets.choice(all_characters))

    return "".join(_shuffle(password))


@lru_cache(maxsize=1)
def load_passphrase_words():
    if PASSPHRASE_WORDS_PATH.exists():
        words = [
            line.strip().lower()
            for line in PASSPHRASE_WORDS_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        if words:
            return words

    return [
        "anchor", "autumn", "bamboo", "beacon", "birch", "breeze", "canyon", "cedar",
        "comet", "coral", "crystal", "dawn", "ember", "falcon", "forest", "frost",
        "garden", "glacier", "harbor", "horizon", "island", "jungle", "lantern",
        "maple", "meadow", "meteor", "midnight", "mist", "mountain", "oasis", "ocean",
        "orchid", "panda", "pepper", "phoenix", "planet", "prairie", "quartz", "raven",
        "river", "saffron", "shadow", "signal", "silver", "sparrow", "summit", "sunset",
        "thunder", "valley", "violet", "voyage", "willow", "winter",
    ]


def generate_passphrase(word_count, separator="-"):
    words = load_passphrase_words()
    if word_count < 2:
        raise ValueError("Passphrase должна содержать минимум 2 слова.")

    selected_words = [secrets.choice(words) for _ in range(word_count)]
    return separator.join(selected_words)
