def fibonacci(n: int):
    if n < 0:
        return 'Incorrect parameter passed!'
    elif n == 0:
        return 0
    elif n in (1, 2):
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


if __name__ == '__main__':
    n = -1
    for n in range(-1, 8):
        print(f'fibonacci({n})  ->  {fibonacci(n)}')
        n += 1
