from functools import lru_cache
from pathlib import Path


DICTIONARY_PATH = Path(__file__).resolve().parent.parent / "data" / "rockyou.txt"


@lru_cache(maxsize=1)
def load_dictionary():
    if not DICTIONARY_PATH.exists():
        return set()

    with DICTIONARY_PATH.open("r", encoding="latin-1", errors="ignore") as file:
        return {line.strip() for line in file if line.strip()}


def dictionary_available():
    return DICTIONARY_PATH.exists()


def check_weak_password(password):
    return password in load_dictionary()
