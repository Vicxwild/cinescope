def squares(n):
    for i in range(n):
        yield i ** 2

for square in squares(5):
    print(square)  # Выводит квадраты чисел от 0 до 4


def generate_numbers():
    for i in range(5):
        yield i  # Возвращает значение и приостанавливает выполнение

gen = generate_numbers()
print(next(gen))  # Выводит: 0
print(next(gen))  # Выводит: 1
