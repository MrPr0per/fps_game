def factor(n):
    return eval('*'.join(list(str(i) for i in range(1, n + 1))))


print(factor(10000))
