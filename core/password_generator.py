import random
import string


def generate_password(length, use_upper, use_lower, use_digits, use_special):

    characters = ""
    password = []

    if use_lower:
        characters += string.ascii_lowercase
        password.append(random.choice(string.ascii_lowercase))

    if use_upper:
        characters += string.ascii_uppercase
        password.append(random.choice(string.ascii_uppercase))

    if use_digits:
        characters += string.digits
        password.append(random.choice(string.digits))

    if use_special:
        characters += string.punctuation
        password.append(random.choice(string.punctuation))

    remaining_length = length - len(password)

    for _ in range(remaining_length):
        password.append(random.choice(characters))

    random.shuffle(password)

    return ''.join(password)