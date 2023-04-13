"""
@author: Kuro
"""

import secrets
import string


def generate_password(length=12):
    """
    This Python function generates a random string of specified length using a
    combination of letters, digits, and special characters.

    :param length: The length parameter is an optional argument that specifies the
    length of the generated string. If no value is provided for length, the default value of 12 will be
    used, defaults to 12 (optional)
    :return: a randomly generated string of characters with a default length of 12.
    The string includes letters (both uppercase and lowercase), digits, and special characters. The
    `secrets.choice()` function is used to randomly select characters from the `alphabet`
    string, and the `join()` method is used to concatenate the selected characters into a single string.
    """

    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation
    alphabet = letters + digits + special_chars

    def filter_chars():
        random_char = secrets.choice(alphabet)
        return random_char if random_char not in ['<', '>', '^'] else filter_chars()

    return ''.join(''.join(filter_chars()) for _ in range(length))
