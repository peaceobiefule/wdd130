# Password Strength Checker 
# Enhancement: Added feedback system to guide users on how to improve their passwords
# and added a feature to suggest a strong password if the entered one is weak.

import random

LOWER = list("abcdefghijklmnopqrstuvwxyz")
UPPER = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
DIGITS = list("0123456789")
SPECIAL = list("!@#$%^&*()-_=+[]{}|;:'\",.<>?/~")

def word_in_file(word, filename, case_sensitive=False):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line_word = line.strip()
                if not case_sensitive:
                    if word.lower() == line_word.lower():
                        return True
                else:
                    if word == line_word:
                        return True
        return False
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return False

def word_has_character(word, character_list):
    for char in word:
        if char in character_list:
            return True
    return False

def word_complexity(word):
    complexity = 0
    if word_has_character(word, LOWER):
        complexity += 1
    if word_has_character(word, UPPER):
        complexity += 1
    if word_has_character(word, DIGITS):
        complexity += 1
    if word_has_character(word, SPECIAL):
        complexity += 1
    return complexity

def suggest_strong_password(length=16):
    all_chars = LOWER + UPPER + DIGITS + SPECIAL
    return ''.join(random.choices(all_chars, k=length))

def give_feedback(password):
    feedback = []
    if not word_has_character(password, LOWER):
        feedback.append("add lowercase letters")
    if not word_has_character(password, UPPER):
        feedback.append("add uppercase letters")
    if not word_has_character(password, DIGITS):
        feedback.append("add digits")
    if not word_has_character(password, SPECIAL):
        feedback.append("add special characters")
    if len(password) < 10:
        feedback.append("make it at least 10 characters long")
    elif len(password) < 16:
        feedback.append("consider using 16 or more characters for stronger protection")
    return feedback

def password_strength(password, min_length=10, strong_length=16):
    if word_in_file(password, "wordlist.txt", case_sensitive=False):
        print("Password is a dictionary word and is not secure.")
        return 0

    if word_in_file(password, "topPasswords.txt", case_sensitive=True):
        print("Password is a commonly used password and is not secure.")
        return 0

    if len(password) < min_length:
        print("Password is too short and is not secure.")
        return 1

    if len(password) >= strong_length:
        print("Password is long, length trumps complexity this is a good password.")
        return 5

    complexity = word_complexity(password)
    strength = 1 + complexity

    return strength

def main():
    while True:
        password = input("Enter a password to check (or 'q' to quit): ")
        if password.lower() == "q":
            print("Goodbye!")
            break

        strength = password_strength(password)
        print(f"Password strength: {strength}/5")

        if strength < 5:
            print("Suggestions to improve your password:")
            tips = give_feedback(password)
            for tip in tips:
                print(f"- {tip}")
            print(f"Example of a strong password: {suggest_strong_password()}")
        print()

if __name__ == "__main__":
    main()
