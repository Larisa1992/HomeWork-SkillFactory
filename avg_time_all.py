import time

# ОСНОВНОЕ ЗАДАНИЕ
def time_this(num_runs):        #это обычная функция, которая передает параметр num_runs в декоратор и возвращает его
    def decorator(func):
        def wrapper(*args, **kwargs):
            avg_time = 0
            for _ in range(num_runs):
                start = time.time()
                func(*args, **kwargs)
                end = time.time()
                avg_time += (end - start)
            avg_time /= num_runs
            print("Выполнение заняло %.5f секунд" % avg_time)
        return wrapper
    return decorator

@time_this(num_runs=10)
def f():
    for j in range(1000000):
        pass

print('Основное задание')
f()

# ЗАДАНИЕ СО ЗВЕЗДОЧКОЙ
class Seconds():
    def __init__(self, num_runs = 10):
        self.num_runs = num_runs
        self.avg_time = 0

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            for _ in range(self.num_runs):
                start = time.time()
                func(*args, **kwargs)
                end = time.time()
                self.avg_time += (end - start)
            self.avg_time /= self.num_runs
            print("Выполнение заняло %.5f секунд" % self.avg_time)      
        return wrapper

# проверяю на функции с одним аргументом: f(n)
@Seconds()
def ff(n):
    for j in range(1000000):
        j + n

print('задание со звездочкой')
ff(7)

# ЗАДАНИЕ С ДВУМЯ ЗВЕЗДОЧКАМИ
class Decorator():
    def __init__(self, num_runs = 10):
        self.num_runs = num_runs
        self.avg_time = 0

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        return wrapper

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, type, value, traceback):
        self.end = time.time()
        self.avg_time = (self.end - self.start)/self.num_runs
        print("Выполнение заняло %.5f секунд" % self.avg_time)

print('задание с двумя звездочками')
def fff(n):
    for j in range(1000000):
        n + j

with Decorator() as dec:
    for i in range(dec.num_runs):
        dec(fff(8))
