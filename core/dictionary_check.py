def load_dictionary():

    weak_passwords = set()

    try:
        with open("D:/Password Analyzer Z+ 1.3.7/data/rockyou.txt", "r", encoding="latin-1") as file:
            for line in file:
                weak_passwords.add(line.strip())
    except FileNotFoundError:
        print("Файл rockyou.txt не найден")

    return weak_passwords


def check_weak_password(password):

    weak_passwords = load_dictionary()

    return password in weak_passwords