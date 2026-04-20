def evaluate_strength(analysis, is_weak_dictionary, patterns_found, pwned_count):
    length = analysis["length"]
    score = 0

    if pwned_count and pwned_count > 0:
        return "СЛАБЫЙ пароль"

    if is_weak_dictionary:
        return "СЛАБЫЙ пароль"

    if length >= 20:
        score += 4
    elif length >= 16:
        score += 3
    elif length >= 12:
        score += 2
    elif length >= 8:
        score += 1

    category_count = sum(
        (
            analysis["lowercase"],
            analysis["uppercase"],
            analysis["digits"],
            analysis["special"],
        )
    )
    if category_count >= 3:
        score += 1
    if category_count == 4:
        score += 1

    if analysis["unique_chars"] >= max(8, length // 2):
        score += 1

    if analysis["is_passphrase"] and length >= 20:
        score += 1

    if patterns_found:
        score -= min(2, len(patterns_found))

    if analysis["has_long_repeat"]:
        score -= 2

    if length < 8:
        return "СЛАБЫЙ пароль"
    if score <= 2:
        return "СЛАБЫЙ пароль"
    if score <= 5:
        return "СРЕДНИЙ пароль"
    return "СИЛЬНЫЙ пароль"
