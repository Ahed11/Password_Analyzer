import hashlib
from urllib import error, request


HIBP_ENDPOINT = "https://api.pwnedpasswords.com/range/"
HIBP_USER_AGENT = "PasswordAnalyzerZ/1.4"


def check_pwned_password(password, timeout=5):
    sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    req = request.Request(
        f"{HIBP_ENDPOINT}{prefix}",
        headers={
            "Add-Padding": "true",
            "User-Agent": HIBP_USER_AGENT,
        },
    )

    try:
        with request.urlopen(req, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except (error.URLError, TimeoutError):
        return {
            "checked": False,
            "count": None,
            "message": "Не удалось проверить HIBP: сервис недоступен или нет сети.",
        }

    for line in body.splitlines():
        leaked_suffix, _, leaked_count = line.partition(":")
        if leaked_suffix == suffix:
            return {
                "checked": True,
                "count": int(leaked_count),
                "message": f"Пароль найден в известных утечках: {int(leaked_count)} раз.",
            }

    return {
        "checked": True,
        "count": 0,
        "message": "Пароль не найден в известных утечках HIBP.",
    }
