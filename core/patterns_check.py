# patterns_check.py

common_patterns = [
    "123", "1234", "12345", "123456",
    "qwerty", "asdf", "password", "admin",
    "letmein", "welcome", "login", "abc",
    "111", "000", "iloveyou"
]

def check_patterns(password):
    """Проверяет пароль на известные человеческие паттерны"""
    found = []

    for pattern in common_patterns:
        if pattern in password.lower():
            found.append(pattern)

    return found