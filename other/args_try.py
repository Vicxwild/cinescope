def add_numbers(*args):
    return sum(args)

print(add_numbers(1, 2, 3))  # 6
print(add_numbers(10, 20, 30, 40))  # 100

def create_list(*args):
    new_list = list()
    for arg in args:
        new_list.append(arg)

    return new_list

print(create_list(1, "apple", True, 3.14))

def pass_arguments(*args):
    print_args(*args)

def print_args(*args):
    for arg in args:
        print(arg)

pass_arguments("Hello", 42, False)

def find_max(*args):
    return max(args)

print(find_max(10, 20, 5, 100, 50))

def join_strings(*args):
    return " ".join(args)

print(join_strings("Hello", "world", "!"))