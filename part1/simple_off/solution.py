def off(x):
    def wrapper():
        print("функция отключена")

    return wrapper


