def greet(**kwargs):
    if "name" and "age" in kwargs:
        print(f"Hello, {kwargs['name']}! You are {kwargs['age']} years old.")
    else:
        print("Hello, stranger!")

greet(name="Alice", age=25)

def create_dict(**kwargs):
    new_dict = dict()

    for key, value in kwargs.items():
        new_dict[key] = value

    return new_dict

print(create_dict(a=1, b=2, c=3))

def update_settings(settings, **kwargs):
    for key, value in kwargs.items():
        settings[key] = value

    return settings

default_settings = {"theme": "light", "notifications": True}
print(update_settings(default_settings, theme="dark", volume=80))

def filter_kwargs(**kwargs):
    filter_dict = dict()

    for key, value in kwargs.items():
        if value > 10:
            filter_dict[key] = value

    return filter_dict

print(filter_kwargs(a=5, b=20, c=15, d=3))

def log_kwargs(func):
    def wrapper(*args, **kwargs):
        print(f"Called with kwargs: {kwargs}")
        return func(*args, **kwargs)

    return wrapper

@log_kwargs
def my_function(a, b, **kwargs):
    return a + b

my_function(5, 10, debug=True, verbose=False)
