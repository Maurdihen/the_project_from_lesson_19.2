def called(x):
    def wrapper():
        print("функция вызвана")
        x()
    return wrapper
