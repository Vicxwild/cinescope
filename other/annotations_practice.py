def multiply(a: int, b: int) -> int:
    return a * b

multiply("bla", "bla")

def sum_numbers(numbers: list[int]) -> int:
    return sum_numbers(numbers)

sum_numbers(["one", "two", "three"])

from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Пользователь найден"
    return None

find_user(2)

from typing import Union

def process_input(value: Union[int, str]):
    return f"Ты передал: {value}"

process_input('bla')

class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Привет, меня зовут {self.name}!"

User("Артем", 25).greet()

def get_even_numbers(numbers: list[int]) -> list[int]:
    return [num for num in numbers if num % 2 == 0]

get_even_numbers([1,2,3])
