def evaluate_strength(analysis, is_weak):

    score = 0

    length = analysis["length"]

    if length >= 8:
        score += 1

    if length >= 12:
        score += 1

    if analysis["lowercase"]:
        score += 1

    if analysis["uppercase"]:
        score += 1

    if analysis["digits"]:
        score += 1

    if analysis["special"]:
        score += 1

    if is_weak:
        return "СЛАБЫЙ пароль"

    if score <= 2:
        return "СЛАБЫЙ пароль"
    elif score <= 4:
        return "СРЕДНИЙ пароль"
    else:
        return "СИЛЬНЫЙ пароль"