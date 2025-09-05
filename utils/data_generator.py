import random
import string
from faker import Faker
faker = Faker()

class DataGenerator:
    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        # Гарантируем наличие хотя бы одной буквы и одной цифры
        letter_lc = random.choice(string.ascii_lowercase)  # Одна буква в нижнем регистре
        letters_uc = random.choice(string.ascii_uppercase)  # Одна буква в верхнем регистре
        digits = random.choice(string.digits)  # Одна цифра

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 17)  # Остальная длина пароля
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters_uc + letter_lc + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_random_film_title():
        return f"{faker.word().capitalize()} {faker.word()}"

    @staticmethod
    def generate_random_film_description():
        return faker.text(max_nb_chars=50)

    @staticmethod
    def generate_random_str(chars: int):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(chars))
