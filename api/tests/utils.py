import string
import random


def generate_random_string(length: int, email: bool = False) -> str:
    alpha = list(string.ascii_lowercase)
    generated_string = ""
    for _ in range(length):
        generated_string += alpha[random.randint(0, len(alpha)-1)]
    return generated_string+"@default.com" if email else generated_string
